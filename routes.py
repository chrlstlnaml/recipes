from flask import session, redirect, url_for
from py_files.recipes import Recipes_
from py_files.user import User
from py_files.render_template import render_template_my
from flask import Blueprint

blueprint = Blueprint(
    'blueprint',
    __name__,
    url_prefix='',
    template_folder='app/templates',
    static_folder='app/static'
)


def check_response(foo):
    def response_wrap(*args, **kwargs):
        res = foo(*args, **kwargs)
        return res if res else render_template_my('errors/page_404.html')
    return response_wrap


def get_param(commands, index):
    try:
        return commands[index]
    except:
        return None


@blueprint.route('/<path:command>', methods=['GET', 'POST', 'PUT', 'DELETE'])
@check_response
def routes(command):
    try:
        command = command.split("/")
        route = get_param(command, 0)
        param1 = get_param(command, 1)
        param2 = get_param(command, 2)
        if route == 'recipes':
            return Recipes_().view(param1)
        if route == 'user':
            return User().view(param1)
        else:
            return render_template_my('errors/page_404.html')
    except Exception as ex:
        print(ex)


@blueprint.route('/', methods=['GET', 'POST'])
def main_page():
    return render_template_my('main_page.html')


@blueprint.app_errorhandler(404)
def page_error_404(e):
    return render_template_my('errors/page_404.html'), 404


@blueprint.app_errorhandler(500)
def page_error_500(e):
    return render_template_my('errors/page_500.html'), 500
