from flask import session, redirect, url_for, request, jsonify
from db_models import Users
from py_files.render_template import render_template_my
from werkzeug.security import check_password_hash, generate_password_hash

key_salt = 'super_secret_key_for_recipes'


class User:
    def __init__(self):
        pass

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
