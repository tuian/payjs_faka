#-*- coding=utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField, DateTimeField, IntegerField, DecimalField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, DataRequired
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_admin.contrib.fileadmin import FileAdmin
from .models import *
from datetime import datetime, timedelta
from flask_login import current_user


class UserForm(FlaskForm):
    email = StringField(u'邮箱')
    username = StringField(u'用户名')
    isvip = StringField(u'是否vip')
    vip_expired = DateTimeField(
        u'vip过期时间', format='%Y-%m-%d %H:%M:%S', default=datetime.now())
    jifen = IntegerField(u'积分')
    status = BooleanField(u'状态')
    role = StringField(u'角色')


class UserView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "admin":
            return True
        return False
    # 这三个变量定义管理员是否可以增删改，默认为True
    can_delete = True
    can_edit = True
    can_create = True

    # 这里是为了自定义显示的column名字
    column_labels = dict(
        username=u'用户名',
        last_seen=u'最近登录',
    )

    # 如果不想显示某些字段，可以重载这个变量
    column_exclude_list = (
        'password_hash', 'role', 'avatar_hash', 'role_id', 'password', 'regip', 'lastip', 'viewtimes'
    )
    column_descriptions = dict(
        status=u'状态：1：正常；0：限制状态')
    column_searchable_list = ('username', 'email')
    form = UserForm


class CateForm(FlaskForm):
    cate_name = StringField(u'类别名')
    cate_info = StringField(u'类别描述')


class CateView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "admin":
            return True
        return False
    # 这三个变量定义管理员是否可以增删改，默认为True
    can_delete = True
    can_edit = True
    can_create = True

    form = CateForm


class GoodForm(FlaskForm):
    cate_id = IntegerField(u'绑定类别')
    good_name = StringField(u'商品名')
    good_info = StringField(u'商品介绍')
    good_price = DecimalField(u'价格')
    good_status = BooleanField(u'状态-上线/下线')


class GoodView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "admin":
            return True
        return False
    # 这三个变量定义管理员是否可以增删改，默认为True
    can_delete = True
    can_edit = True
    can_create = True

    #form = GoodForm


class KMForm(FlaskForm):
    km_value = StringField(u'卡密值')
    km_status = BooleanField(u'使用状态')
    good = StringField(u'对于商品')


class KMView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "admin":
            return True
        return False
    # 这三个变量定义管理员是否可以增删改，默认为True
    can_delete = True
    can_edit = True
    can_create = True

    form = KMForm


class OrderView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "admin":
            return True
        return False
    # 这三个变量定义管理员是否可以增删改，默认为True
    can_delete = True
    can_edit = False
    can_create = False


class OtherView(ModelView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.username == "admin":
            return True
        return False
    # 这三个变量定义管理员是否可以增删改，默认为True
    can_delete = True
    can_edit = True
    can_create = True


class MyView(BaseView):
    @expose('/')
    def index(self):
        return self.render('index.html')
