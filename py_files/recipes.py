from flask import request, jsonify, session, render_template
from db_models import Ingredients, Recipes, Rating, RecipeCategories, IngredientsInRecipes, Files, Directory
from py_files.render_template import render_template_my
from py_files.tools import Tools
from peewee import JOIN
import os


class Recipes_:

    def __init__(self):
        self.dir_resources = 'app/static/images/recipe_img'

    def view(self, param):
        if not param:
            pass
        elif param == 'search_for_recipes' and request.method == 'GET':
            return self.show_search_page()
        elif param == 'search_for_recipes' and request.method == 'POST':
            return jsonify(self.search_for_recipes(request.values.to_dict()))
        elif param == 'my_recipes' and request.method == 'GET':
            return self.my_recipes_list()
        elif param == 'recipe' and request.method == 'GET':
            return self.show_recipe_page(request.args.get('id'))
        elif param == 'get_ingredient_html' and request.method == 'GET':
            return self.get_ingredient_html(request.args.get('index', 0))
        elif param == 'add_ingredient' and request.method == 'POST':
            return jsonify(self.add_ingredient(request.values.to_dict().get('ingredient_name')))
        elif param == 'save_recipe' and request.method == 'POST':
            return jsonify(self.save_recipe(request.values.to_dict()))
        elif param == 'show_recipe' and request.method == 'GET':
            return self.show_recipe(request.args.get('id'))
        elif param == 'delete_photo' and request.method == 'DELETE':
            return self.delete_photo(request.values.to_dict())

    def show_search_page(self):
        data = {
            'ingredients': Ingredients.select(),
            'recipes': Recipes.select(Recipes.id, Recipes.name, Recipes.cooking_time, Recipes.number_of_servings,
                                      Directory.ru_name.alias('complexity'), Files.id.alias('file_name'),
                                      Files.type_file, Recipes.users_id.alias('user')
                                      ).join(Rating, JOIN.LEFT_OUTER)
                                       .join(Files, JOIN.LEFT_OUTER, on=(Files.recipes_id == Recipes.id))
                                       .join(Directory, on=(Recipes.complexity_id == Directory.id))
                                       .dicts()
        }
        return render_template_my('recipes/search_for_recipes.html', data=data)

    def search_for_recipes(self, post_data):
        ingredients = post_data['ingredients'].split(',')
        if ingredients != ['']:

            print(ingredients)
        return {'result_code': 200}

    @Tools.check_session
    def my_recipes_list(self):
        data = {
            'recipes': Recipes.select(Recipes.id, Recipes.users_id.alias('user'), Recipes.name, Recipes.cooking_time,
                                      Recipes.number_of_servings, Directory.ru_name.alias('complexity'),
                                      Files.id.alias('file_name'), Files.type_file
                                      ).join(Rating, JOIN.LEFT_OUTER)
                                       .join(Files, JOIN.LEFT_OUTER, on=(Files.recipes_id == Recipes.id))
                                       .join(Directory, on=(Recipes.complexity_id == Directory.id))
                                       .where(Recipes.users_id == session.get('user_id')).dicts()
        }
        return render_template_my('recipes/my_recipes.html', data=data)

    @staticmethod
    def get_data_for_selects():
        return {
            'ingredients': Ingredients.select().dicts(),
            'measure': Tools.get_measure(),
            'complexity': Tools.get_complexity(),
            'category': Tools.get_category(),
            'accept': Tools.get_accept_for_files(),
            'max_file_size': Tools.get_max_size_for_files()
        }

    @Tools.check_session
    def show_recipe_page(self, recipes_id):
        data = self.get_data_for_selects()
        if not recipes_id:
            index = 1
        else:
            data['recipe'] = Recipes.select(Recipes, Files.file_name, Files.type_file, Files.id.alias('file_id'))\
                                    .join(Files, JOIN.LEFT_OUTER, on=(Files.recipes_id == Recipes.id))\
                                    .where(Recipes.id == recipes_id).dicts()
            data['recipe_categories'] = RecipeCategories.select().where(RecipeCategories.recipes_id == recipes_id)\
                                                                 .dicts()
            data['recipe_ingredients'] = IngredientsInRecipes.select()\
                                                             .where(IngredientsInRecipes.recipes_id == recipes_id)\
                                                             .dicts()
            index = len(data['recipe_ingredients'])
        return render_template_my('recipes/recipe.html', data=data, index=index)

    @staticmethod
    def get_ingredient_html(index):
        data = {
            'ingredients': Ingredients.select(),
            'measure': Tools.get_measure()
        }
        return render_template('recipes/ingredient.html', data=data, index=index)

    @staticmethod
    def get_ingredients_from_post_data(post_data):
        ingredients = {}
        for key, val in post_data.items():
            if key[:12] == 'ingredients-':
                if ingredients.get(key[12]):
                    ingredients[key[12:]]['ingredients_id'] = val
                else:
                    ingredients[key[12:]] = {'ingredients_id': val}
            elif key[:8] == 'measure-':
                if ingredients.get(key[8:]):
                    ingredients[key[8:]]['measure_id'] = val
                else:
                    ingredients[key[8:]] = {'measure_id': val}
            elif key[:7] == 'number-':
                if ingredients.get(key[7:]):
                    ingredients[key[7:]]['number'] = val
                else:
                    ingredients[key[7:]] = {'number': val}
        return ingredients

    def mkdir_if_it_need(self):
        if not os.path.exists(self.dir_resources):
            os.mkdir(self.dir_resources)
        if not os.path.exists(self.dir_resources + '/' + session.get('user_id')):
            os.mkdir(self.dir_resources + '/' + session.get('user_id'))

    def save_file(self, recipes_id, file):
        type_file = file.filename.rsplit('.', 1)[1].lower()
        if type_file not in Tools.get_accept_for_files():
            return {"result_code": 403, 'error': f'Допустимые типы файлов: {", ".join(Tools.get_accept_for_files())}'}
        file_ = Files(file_name=file.filename, recipes_id=recipes_id, type_file=type_file)
        file_.save()
        filename = str(file_.id)
        self.mkdir_if_it_need()
        file.save(self.dir_resources+'/'+session.get('user_id')+'/'+filename+'.'+type_file)
        size = float(os.path.getsize(self.dir_resources+'/'+session.get('user_id')+'/'+filename+'.'+type_file))/1024
        q = (Files.update({Files.size_file: size}).where(Files.id == file_.id))
        q.execute()
        return {'result_code': 200}

    @staticmethod
    @Tools.try_except
    def add_ingredient(name):
        ingredient = Ingredients(name=name)
        ingredient.save()
        return {'result_code': 200, 'ingredient': {'name': name, 'id': ingredient.id}}

    @Tools.try_except
    def save_recipe(self, post_data):
        categories = post_data['categories'].split(',')
        ingredients = self.get_ingredients_from_post_data(post_data)
        info = {'result_code': 200}
        if post_data.get('recipes_id'):
            recipes_id = post_data.get('recipes_id')
            q = RecipeCategories.delete().where(RecipeCategories.recipes_id == recipes_id)
            q.execute()
            q = IngredientsInRecipes.delete().where(IngredientsInRecipes.recipes_id == recipes_id)
            q.execute()
            q = (Recipes.update({Recipes.name: post_data.get('name'),
                                 Recipes.cooking_time: post_data.get('cooking_time'),
                                 Recipes.description: post_data.get('description'),
                                 Recipes.number_of_servings: post_data.get('number_of_servings'),
                                 Recipes.complexity_id: post_data.get('complexity')
                                 }).where(Recipes.id == recipes_id))
            q.execute()
        else:
            recipe = Recipes(name=post_data.get('name'),
                             users_id=session.get('user_id'),
                             cooking_time=post_data.get('cooking_time'),
                             description=post_data.get('description'),
                             number_of_servings=post_data.get('number_of_servings'),
                             complexity_id=post_data.get('complexity')
                             )
            recipe.save()
            recipes_id = recipe.id
        for category_id in categories:
            category = RecipeCategories(recipes_id=recipes_id, category_id=category_id)
            category.save()
        for ingredient_data in ingredients.values():
            ingredient = IngredientsInRecipes(recipes_id=recipes_id,
                                              ingredients_id=ingredient_data.get('ingredients_id'),
                                              measure_id=ingredient_data.get('measure_id'),
                                              number=ingredient_data.get('number')
                                              )
            ingredient.save()
        if 'photo' in request.files and request.files['photo'].filename:
            info = self.save_file(recipes_id, request.files['photo'])
        return info

    def show_recipe(self, recipes_id):
        data = {
            'recipe': Recipes.select(Recipes, Files.id.alias('file_name'), Files.type_file,
                                     Directory.ru_name.alias('complexity_'), Recipes.users_id.alias('user'))
                             .join(Directory, JOIN.LEFT_OUTER, on=(Recipes.complexity_id == Directory.id))
                             .join(Files, JOIN.LEFT_OUTER, on=(Files.recipes_id == Recipes.id))
                             .where(Recipes.id == recipes_id).dicts(),
            'ingredients': IngredientsInRecipes.select(IngredientsInRecipes, Directory.ru_name.alias('measure_'),
                                                       Ingredients.name.alias('ingredient'))
                                               .join(Ingredients, JOIN.LEFT_OUTER,
                                                     on=(IngredientsInRecipes.ingredients_id == Ingredients.id))
                                               .join(Directory, JOIN.LEFT_OUTER,
                                                     on=(IngredientsInRecipes.measure_id == Directory.id))
                                               .where(IngredientsInRecipes.recipes_id == recipes_id).dicts()
        }
        return render_template_my('recipes/show_recipe.html', data=data)

    def delete_photo(self, post_data):
        q = Files.delete().where(Files.recipes_id == post_data['recipes_id'])
        q.execute()
        try:
            os.remove(self.dir_resources + '/' + session.get('user_id') + '/' + post_data['file'])
        except Exception as ex:
            print(ex)
        return {'result_code': 200}
