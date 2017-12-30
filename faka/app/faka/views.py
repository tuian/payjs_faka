#-*- coding=utf-8 -*-
import datetime
from flask import jsonify, redirect, render_template, request, session, flash, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import faka
from .. import db
from ..models import *
from .forms import *
from ..email import *
import requests
from ..payjs import getqr


@faka.route('/')
def index():
    return render_template('faka/index.html')


@faka.route('/getkm', methods=["POST", "GET"])
def getkm():
    if request.method == 'POST':
        lx = request.form.get('tqm', type=int)
        orders = Order.query.filter_by(lx=lx).all()
        if len(orders) == 0:
            return render_template('faka/getkm.html', orders=None)
        else:
            return render_template('faka/getkm.html', orders=orders)
    return render_template('faka/getkm.html')


@faka.route('/Selgo', methods=["POST"])
def Selgo():
    cateid = request.form.get('cateid')
    goods = db.session.query(Good).join(
        Category, Good.cate_id == Category.cateid).filter(Category.cateid == cateid,Good.good_status==True).all()
    base = u"<option id='{goodid}' imgs='assets/goodsimg/df.jpg' value='{goodid}' kc='{kc}' title='{price}' alt = '{info}'>{goodname}</option>"
    s = u'<option>请选择商品</option>'
    for good in goods:
        kc = db.session.query(KM).join(Good, KM.good_id == Good.good_id).filter(
            KM.km_status == True, Good.good_id == good.good_id).count()
        s += base.format(goodid=good.good_id,
                         goodname=good.good_name, price=good.good_price, kc=kc, info=good.good_info)
    return jsonify({'msg': s})


@faka.route('/Checkgo', methods=["POST"])
def Checkgo():
    goodid = request.form.get('goodid')
    kc = db.session.query(KM).join(Good, KM.good_id == Good.good_id).filter(
        KM.km_status == True, Good.good_id == goodid).count()
    if kc < 0:
        retdata = {'code': -1}
    else:
        retdata = {'code': 1}
    return jsonify(retdata)


@faka.route('/CreateOrder', methods=["POST"])
def CreateOrder():
    trade_id = request.form.get('out_trade_no')
    good_id = request.form.get('gid')
    lx = request.form.get('rel')
    feedback = request.scheme + '://' + request.host + '/check_order'
    try:
        order = Order(trade_id=trade_id, lx=lx, good_id=good_id)
        db.session.add(order)
        db.session.commit()
        good = Good.query.filter_by(good_id=good_id).first()
        qr = getqr(money=good.good_price, tradeid=trade_id, feedback=feedback)
        #qr="weixin://wxpay/"
        if qr == False:
            retdata = {'code': -1}
        else:
            retdata = {'code': 0, 'qr': qr}
    except Exception as e:
        print(e)
        retdata = {'code': -1}
    return jsonify(retdata)


@faka.route('/check_order', methods=["POST"])
def check_order():
    tradeid = request.form.get('out_trade_no')
    return_code = request.form.get('return_code', type=int)
    if return_code == 1:
        order = Order.query.filter_by(trade_id=tradeid).first()
        if order.trade_status == False:
            # 订单信息更新
            order.endtime = datetime.datetime.now()
            order.trade_status = True
            # 商品信息更新
            good = Good.query.filter_by(good_id=order.good_id).first()
            good.good_sales += 1  # 销量加1
            km = KM.query.filter_by(
                good_id=good.good_id, km_status=True).first()
            km.km_status = False  # 已售出
            # 订单绑定卡密
            order.km_id = km.km_id
            db.session.add(order)
            db.session.add(good)
            db.session.add(km)
            db.session.commit()
    return 'callback success'


# 添加卡密
@faka.route('/admin/add_code/', methods=['POST', 'GET'])
@login_required
def add_code():
    if request.method == 'POST':
        good_id = request.form.get('goodid')
        kms = eval(request.form.get('km'))
        success, fail = 0, 0
        for km in kms:
            km = km.replace(' ', '')
            try:
                if KM.query.filter_by(km_value=km,good_id=good_id).count() == 0:
                    newkm = KM(km_value=km, good_id=good_id)
                    db.session.add(newkm)
                    db.session.commit()
                    success += 1
            except Exception as e:
                print(e)
                fail += 1
        msg = '成功{}个，失败{}个'.format(success, fail)
        return jsonify({'msg': msg})
    return render_template('admin/add_code.html')
