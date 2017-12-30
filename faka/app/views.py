#-*- coding=utf-8 -*-
from app import app, db, admin
from app.models import *
from .forms import *
from auth.forms import *
from flask import render_template, make_response, redirect, request, url_for, flash, session, jsonify, g, current_app, send_from_directory
from flask_login import login_user, logout_user, login_required, \
    current_user
from app.email import send_email
from app.decorators import admin_required, permission_required
from flask_wtf import FlaskForm
from wtforms.validators import URL
import urllib
import re
import os


admin.add_view(UserView(User, db.session, name=u'用户', category=u'用户管理'))
admin.add_view(OtherView(Role, db.session, name=u'角色', category=u'用户管理'))
admin.add_view(CateView(Category, db.session, name=u'类别', category=u'商品管理'))
admin.add_view(GoodView(Good, db.session, name=u'商品', category=u'商品管理'))
admin.add_view(KMView(KM, db.session, name=u'管理卡密', category=u'商品管理'))
admin.add_view(
    MyView(name=u'添加卡密', endpoint='add_code', category=u'商品管理'))
admin.add_view(OrderView(Order, db.session, name=u'订单'))


@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    """Generate sitemap.xml. Makes a list of urls and date modified."""
    pages = []
    ten_days_ago = (datetime.now() - timedelta(days=10)
                    ).strftime('%Y-%m-%d %H:%M:%S')
    # static pages
    for rule in current_app.url_map.iter_rules():
        if "GET" in rule.methods and len(rule.arguments) == 0:
            pages.append([rule.rule, ten_days_ago])

    sitemap_xml = render_template('sitemap_template.xml', pages=pages)
    response = make_response(sitemap_xml)
    response.headers["Content-Type"] = "application/json"

    return response


@app.route('/robots.txt', methods=['GET'])
def robots():
    robots = render_template('robots.txt')
    response = make_response(robots)
    response.headers["Content-Type"] = "text/plain"
    return response


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')
