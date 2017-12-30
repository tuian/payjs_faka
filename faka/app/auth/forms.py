#-*- coding=utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo, DataRequired
from wtforms import ValidationError
from ..models import User
from flask import session


class LoginForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    password = PasswordField(u'密码', validators=[DataRequired()])
    remember_me = BooleanField(u'保持登录', default=True)
    recaptcha = StringField(
        u'验证码', validators=[DataRequired(message=u'验证码不能为空')])
    submit = SubmitField(u'登陆')


    # def validate_recaptcha(self, field):
    #     if session.get('S_RECAPTCHA') != field.data.upper():
    #         raise ValidationError(u'验证码错误')


class RegistrationForm(FlaskForm):
    invitecode = StringField(u'邀请码-可有可无')
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    username = StringField(u'用户名', validators=[
        DataRequired(), Length(1, 64), Regexp(u'^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                              '用户名由字母、数字、下划线组成')])
    password = PasswordField(u'密码', validators=[
        DataRequired(), EqualTo('password2', message=u'重复密码必须相同')])
    password2 = PasswordField(u'确认密码', validators=[DataRequired()])
    recaptcha = StringField(
        u'验证码', validators=[DataRequired(message=u'验证码不能为空')])
    submit = SubmitField(u'注册')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError(u'邮箱已经被注册')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError(u'用户名已经被注册')

    # def validate_recaptcha(self, field):
    #     if session.get('S_RECAPTCHA') != field.data.upper():
    #         raise ValidationError(u'验证码错误')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField(u'旧密码', validators=[DataRequired()])
    password = PasswordField(u'新密码', validators=[
        DataRequired(), EqualTo('password2', message=u'重复密码必须相同')])
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()])
    submit = SubmitField(u'更新密码')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64),
                                             Email()])
    recaptcha = StringField(
        u'验证码', validators=[DataRequired(message=u'验证码不能为空')])
    submit = SubmitField(u'重设密码')

    # def validate_recaptcha(self, field):
    #     if session.get('S_RECAPTCHA') != field.data.upper():
    #         raise ValidationError(u'验证码错误')


class PasswordResetForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    password = PasswordField(u'新密码', validators=[
        DataRequired(), EqualTo('password2', message=u'密码必须相同')])
    password2 = PasswordField(u'确认新密码', validators=[DataRequired()])
    recaptcha = StringField(
        u'验证码', validators=[DataRequired(message=u'验证码不能为空')])
    submit = SubmitField(u'重设密码')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'未知邮箱')

    # def validate_recaptcha(self, field):
    #     if session.get('S_RECAPTCHA') != field.data.upper():
    #         raise ValidationError(u'验证码错误')


class ConfirmForm(FlaskForm):
    email = StringField(u'邮箱', validators=[DataRequired(), Length(1, 64),
                                          Email()])
    recaptcha = StringField(
        u'验证码', validators=[DataRequired(message=u'验证码不能为空')])
    submit = SubmitField(u'提交')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError(u'未知邮箱')

    # def validate_recaptcha(self, field):
    #     if session.get('S_RECAPTCHA') != field.data.upper():
    #         raise ValidationError(u'验证码错误')
