#-*- coding=utf-8 -*-
import os
from datetime import timedelta
basedir = os.path.abspath(os.path.dirname(__file__))
import pymysql


SECRET_KEY = 'SSDFDSFDFD'
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:password@localhost/db' # user,password,db换成你的
SQLALCHEMY_TRACK_MODIFICATIONS = True
debug = True
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = ''
MAIL_PASSWORD = ''
#payjs信息
PAYJS_ID=''
PAYJS_KEY=''
