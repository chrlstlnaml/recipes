from flask import session, redirect, url_for, request, jsonify
from db_models import Users, Files
from py_files.render_template import render_template_my
from werkzeug.security import check_password_hash, generate_password_hash
from py_files.tools import Tools
import os

key_salt = 'super_secret_key_for_recipes'


class User:
    def __init__(self):
        self.dir_resources = 'app/static/images/user_img'

    def view(self, param):
        if param == 'login' and request.method == 'GET':
            return self.show_login_page()
        if param == 'login' and request.method == 'POST':
            return jsonify(self.login(request.values.to_dict()))
        elif param == 'registration' and request.method == 'GET':
            return self.show_registration_page()
        elif param == 'sign_up' and request.method == 'POST':
            return jsonify(self.sign_up(request.values.to_dict()))
        elif param == 'logout' and request.method == 'GET':
            return self.logout()
        elif param == 'profile' and request.method == 'GET':
            return self.show_profile_page()
        elif param == 'update_photo' and request.method == 'POST':
            return jsonify(self.update_photo(request.files['photo']))
        elif param == 'delete_photo' and request.method == 'DELETE':
            return jsonify(self.delete_photo())

    def show_login_page(self):
        return render_template_my('user/login.html')

    def login(self, post_data):
        user = Users.select(Users.id, Users.password)\
            .where((Users.email == post_data.get('login_or_email')) | (Users.login == post_data.get('login_or_email')))
        if len(user) == 0:
            return {'result_code': 404, 'error': 'Пользователь с таким логином или почтой не найден'}
        if not check_password_hash(user[0].password, key_salt + post_data.get('password')):
            return {'result_code': 400, 'error': 'Неверные логин или пароль'}
        session['user_id'] = str(user[0].id)
        return {'result_code': 200}

    @staticmethod
    def show_registration_page():
        return render_template_my('user/registration.html')

    @staticmethod
    def is_unique_email(email):
        user = Users().select(Users.id).where(Users.email == email)
        return len(user) == 0

    @staticmethod
    def is_unique_login(login):
        user = Users().select(Users.id).where(Users.login == login)
        return len(user) == 0

    @staticmethod
    def gen_pass_hash(password):
        return generate_password_hash(key_salt + password)

    def sign_up(self, post_data):
        if not self.is_unique_email(post_data.get('email')):
            return {'result_code': 400, 'error': 'Аккаунт с такой почтой уже существует!'}
        if not self.is_unique_login(post_data.get('login')):
            return {'result_code': 400, 'error': 'Аккаунт с таким логином уже существует!'}
        user = Users(email=post_data.get('email'), login=post_data.get('login'),
                     password=self.gen_pass_hash(post_data.get('password')))
        user.save()
        session['user_id'] = str(user.id)
        return {'result_code': 200, 'message': 'Вы успешно зарегистрировались!'}

    @staticmethod
    def logout():
        session['user_id'] = None
        return redirect(url_for('blueprint.main_page'))

    @Tools.check_session
    def show_profile_page(self):
        data = {
            'user': Users.select().where(Users.id == session.get('user_id')).dicts(),
            'photo': Files.select().where(Files.users_id == session.get('user_id')).dicts(),
            'max_file_size': Tools.get_max_size_for_files()
        }
        return render_template_my('user/profile.html', data=data)

    def mkdir_if_it_need(self):
        if not os.path.exists(self.dir_resources):
            os.mkdir(self.dir_resources)

    def save_file(self, file):
        type_file = file.filename.rsplit('.', 1)[1].lower()
        if type_file not in Tools.get_accept_for_files():
            return {"result_code": 403, 'error': f'Допустимые типы файлов: {", ".join(Tools.get_accept_for_files())}'}
        file_ = Files(file_name=file.filename, users_id=session.get('user_id'), type_file=type_file)
        file_.save()
        filename = str(file_.id)
        self.mkdir_if_it_need()
        file.save(self.dir_resources+'/'+filename+'.'+type_file)
        size = float(os.path.getsize(self.dir_resources+'/'+filename+'.'+type_file))/1024
        q = (Files.update({Files.size_file: size}).where(Files.id == file_.id))
        q.execute()
        return {'result_code': 200}

    @Tools.try_except
    def update_photo(self, photo):
        if photo.filename:
            self.delete_photo()
            return self.save_file(photo)
        else:
            return {'result_code': 200, 'error': 'Необходимо прикрепить фотографию.'}

    @Tools.try_except
    def delete_photo(self):
        file = Files.select().where(Files.users_id == session.get('user_id')).dicts()
        if len(file) > 0:
            file_id = str(file[0]['id']) + '.' + file[0]['type_file']
            q = Files.delete().where(Files.users_id == session.get('user_id'))
            q.execute()
            try:
                os.remove(self.dir_resources + '/' + file_id)
            except Exception as ex:
                print(ex)
        return {'result_code': 200}
