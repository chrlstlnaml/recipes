from py_files.render_template import render_template_my
from flask import session
from db_models import Directory, NameDirectory
from Config import Config
from datetime import datetime as dt


class Tools:

    def __init__(self):
        pass

    @staticmethod
    def check_session(foo):
        def is_session(*args, **kwargs):
            if session.get('user_id'):
                return foo(*args, **kwargs)
            return render_template_my('errors/page_401.html')
        return is_session

    @staticmethod
    def get_measure():
        return Directory.select().join(NameDirectory)\
                        .where((NameDirectory.tech_name == 'measure') | (Directory.is_published is True)).dicts()

    @staticmethod
    def get_complexity():
        return Directory.select().join(NameDirectory) \
                        .where((NameDirectory.tech_name == 'complexity') | (Directory.is_published is True)).dicts()

    @staticmethod
    def get_category():
        return Directory.select().join(NameDirectory) \
                        .where((NameDirectory.tech_name == 'category') | (Directory.is_published is True)).dicts()

    @staticmethod
    def get_accept_for_files():
        return Config().get_param('FILES')["type"].split(',')

    @staticmethod
    def get_max_size_for_files():
        return eval(Config().get_param('FILES')["size"])

    @staticmethod
    def try_except(foo):
        def ex(*args, **kwargs):
            try:
                res = foo(*args, **kwargs)
                return res
            except Exception as ex:
                print(f"{dt.strftime(dt.now(), '%d.%m.%Y %H:%M:%S')}: Ошибка {ex} в функции {foo.__name__}")
                return {'result_code': 500, 'error': 'Сохранить не удалось!'}
        return ex
