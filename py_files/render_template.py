from flask import render_template, session


def render_template_my(template, **kwargs):
    kwargs['user_id'] = session.get('user_id', None)
    return render_template(template, **kwargs)
