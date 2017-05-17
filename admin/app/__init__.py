import os

from logging import getLogger
from flask.ext.sqlalchemy import SQLAlchemy
from flask import Flask, request, session
from flask import Flask, render_template
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babelex import Babel

LOG = getLogger(__name__)

app = Flask(__name__, static_url_path='/static')
db = SQLAlchemy(app)
babel = Babel(app)
admin = Admin(
    app, 
    name='Popular Plastic', 
    template_mode='bootstrap3',
    category_icon_classes={
        'color': 'glyphicon glyphicon-user',
    }
)


@babel.localeselector
def get_locale():
    """get locale from query param"""
    override = request.args.get('lang')

    if override:
        session['lang'] = override

    return session.get('lang', 'en')
