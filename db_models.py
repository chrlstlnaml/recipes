from peewee import *
from datetime import datetime as dt
from Config import Config

db = SqliteDatabase(Config().get_param('SQLITE')['filename'])


class BaseModel(Model):
    class Meta:
        database = db


class Users(BaseModel):
    email = TextField()
    login = TextField()
    password = TextField()
    token = TextField(null=True)
    activation_datetime = DateTimeField(null=True)
    create_datetime = DateTimeField(default=dt.now)


class NameDirectory(BaseModel):
    tech_name = TextField()
    ru_name = TextField()


class Directory(BaseModel):
    name_directory = ForeignKeyField(NameDirectory, backref='name_directory')
    tech_name = TextField()
    ru_name = TextField()
    default = BooleanField(default=False, null=True)
    is_published = BooleanField(default=True, null=True)


class Recipes(BaseModel):
    name = TextField()
    create_datetime = DateTimeField(default=dt.now)
    users = ForeignKeyField(Users, backref='user')
    cooking_time = TimeField()
    complexity = ForeignKeyField(Directory, backref='complexity')
    description = TextField()
    number_of_servings = IntegerField()


class Ingredients(BaseModel):
    name = TextField()


class IngredientsInRecipes(BaseModel):
    recipes = ForeignKeyField(Recipes, backref='recipe')
    ingredients = ForeignKeyField(Ingredients, backref='ingredient')
    measure = ForeignKeyField(Directory, backref='measure')
    number = FloatField(null=True)


class RecipeCategories(BaseModel):
    recipes = ForeignKeyField(Recipes, backref='recipe')
    category = ForeignKeyField(Directory, backref='category')


class Rating(BaseModel):
    recipes = ForeignKeyField(Recipes, backref='recipe')
    users = ForeignKeyField(Users, backref='user')
    number = IntegerField()


class Files(BaseModel):
    file_name = TextField()
    users = ForeignKeyField(Users, backref='user', null=True)
    recipes = ForeignKeyField(Recipes, backref='recipe', null=True)
    type_file = CharField()
    size_file = FloatField(null=True)
    creat_datetime = DateTimeField(default=dt.now)


def drop_tables(list_of_tables):
    db.drop_tables(list_of_tables, safe=True)


def create_tables(list_of_tables):
    db.connect()
    db.create_tables(list_of_tables, safe=True)
    db.close()


# drop_tables([Users, Recipes, Ingredients, NameDirectory, Directory, IngredientsInRecipes, Rating])

# create_tables([Users, Recipes, Ingredients, NameDirectory, Directory, IngredientsInRecipes, Rating])

# create_tables([Files])
