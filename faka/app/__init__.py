#-*- coding=utf-8 -*-
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from flask_mail import Mail
from flask_pagedown import PageDown
from flask_admin import Admin
from flask_caching import Cache
from celery import Celery, platforms
import logging
import datetime
from datetime import timedelta
from redis import Redis


app = Flask(__name__)
app.config.from_object('config')
login_manager = LoginManager(app)
login_manager.session_protect = 'strong'
login_manager.login_view = 'auth.login'
#login_manager.login_message = u"请登录！"
admin = Admin(app)
bootstrap = Bootstrap(app)
mail = Mail(app)
pagedown = PageDown(app)
db = SQLAlchemy(app, use_native_unicode='utf8')

from .faka import faka as faka_blueprint
app.register_blueprint(faka_blueprint)

from .auth import auth as auth_blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')


from app import views
