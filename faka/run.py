#-*- coding=utf-8 -*-
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand
from app import app, db, login_manager
from app.models import *
from sqlalchemy import func as SQLfunc
import logging
import re
import hashlib
from datetime import datetime
from werkzeug.contrib.profiler import ProfilerMiddleware


def md5(text):
    m = hashlib.md5()
    m.update(text)
    return m.hexdigest()


def faka_db(sql):
    cur = db2.cursor()
    cur.execute(sql)
    return cur.fetchall()


manager = Manager(app)
migrate = Migrate(app, db)
app.jinja_env.globals['datetime'] = datetime
app.jinja_env.globals['qq'] = '10001'
app.jinja_env.globals['domain'] = 'http://www.baidu.com'
app.jinja_env.globals['User'] = User
app.jinja_env.globals['Order'] = Order
app.jinja_env.globals['Category'] = Category
app.jinja_env.globals['Good'] = Good
app.jinja_env.globals['db'] = db


def make_shell_context():
    return dict(app=app, db=db, IP=IP, ID=ID, Context=Context, Post=Post, clPost=clPost, Role=Role, User=User, FriendUrl=FriendUrl)


@manager.command
def deploy():
    db.drop_all()
    db.create_all()
    Role.insert_roles()
    print("please input admin's email:")
    email = raw_input()
    print("please input admin's password:")
    password = raw_input()
    User.insert_admin(email=email, password=password)
    print('insert admin success!')


manager.add_command('Shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)

if __name__ == '__main__':
    manager.run()
    #app.wsgi_app = ProfilerMiddleware(app.wsgi_app)
    # app.run(host='0.0.0.0',port=36666,debug=True)
