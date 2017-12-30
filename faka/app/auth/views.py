#-*- coding=utf-8 -*-
import datetime
from flask import jsonify, redirect, render_template, request, session, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import auth
from .. import db
from ..models import *
from .forms import *
from ..email import *
from ..verify_code import ImageChar
import cStringIO as StringIO
import urllib

# AUTH
@auth.route('/code', methods=['GET'])
def generate_code():
    """生成验证码
    """
    ic = ImageChar(fontColor=(100, 211, 90))
    strs, code_img = ic.randChinese(4)
    session['S_RECAPTCHA'] = strs
    buf = StringIO.StringIO()
    code_img.save(buf, 'JPEG', quality=80)
    buf_str = buf.getvalue()
    response = current_app.make_response(buf_str)
    response.headers['Content-Type'] = 'image/jpeg'
    return response


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            session['logged_in'] = True
            session['admin'] = False
            if user.id == 1:
                session['admin'] = True
            session.permanent = True
            flash(u'登陆成功')
            try:
                next_ = urllib.unquote(request.args.get('next'))
                return redirect(next_)
            except:
                return redirect(url_for('faka.index'))
        else:
            flash(u'邮箱或密码错误')
            return redirect(url_for('auth.login'))
    return render_template('auth/login.html', form=form)


@auth.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            db.session.commit()
            flash(u'修改密码成功！')
            return redirect(url_for('faka.index'))
        else:
            flash(u'无效密码')
            return redirect(url_for('auth.change_password'))
    return render_template("admin/change_password.html", form=form)

