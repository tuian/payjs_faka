# -*- coding=utf-8 -*-
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from app import login_manager
import datetime
from flask import current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import hashlib
import random
import string


class Permission:
    FOLLOW = 0x01
    COMMENT = 0X02
    WRITE_ARTICLES = 0x04
    MODERATE_COMMENTS = 0x08
    ADMINISTER = 0x80


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    default = db.Column(db.Boolean, default=False, index=True)
    permissions = db.Column(db.Integer)
    users = db.relationship('User', backref='role', lazy='dynamic')

    def __repr__(self):
        return self.name

    @staticmethod
    def insert_roles():
        roles = {
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
                role.permissions = roles[r][0]
                role.default = roles[r][1]
                db.session.add(role)
            db.session.commit()


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    password = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    last_seen = db.Column(db.DateTime(), default=datetime.datetime.utcnow)
    confirmed = db.Column(db.Boolean, default=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    isvip = db.Column(db.Boolean, default=False, index=True)
    vip_expired = db.Column(db.DateTime())
    avatar_hash = db.Column(db.String(32))
    jifen = db.Column(db.Integer, default=0)
    regip = db.Column(db.String(32))
    lastip = db.Column(db.String(32))
    coin = db.Column(db.Integer, default=500)
    invitecode = db.Column(db.String(64))
    status = db.Column(db.Boolean, default=1)

    def __repr__(self):
        return self.username

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.role is None:
            if self.username == 'admin':
                self.role = Role.query.filter_by(permissions=0xff).first()
            else:
                self.role = Role.query.filter_by(default=True).first()
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    @staticmethod
    def insert_admin(email, password, username='admin'):
        admin = User(email=email, password=password,
                     username=username, isvip=True, vip_expired=datetime.datetime.now() + datetime.timedelta(days=+99999))
        admin.role = Role.query.filter_by(permissions=0xff).first()
        db.session.add(admin)
        db.session.commit()

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def can(self, permissions):
        return self.role is not None and \
            (self.role.permissions & permissions) == permissions

    def is_administrator(self):
        return self.can(Permission.ADMINISTER)

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('reset') != self.id:
            return False
        self.password = new_password
        db.session.add(self)
        db.session.commit()
        return True

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        db.session.commit()
        return True

    def gravatar(self, size=40, default='identicon', rating='g'):
        # if request.is_secure:
        #     url = 'https://secure.gravatar.com/avatar'
        # else:
        #     url = 'http://www.gravatar.com/avatar'
        url = 'http://www.gravatar.com/avatar'
        hash = self.avatar_hash or hashlib.md5(
            self.email.encode('utf-8')).hexdigest()
        return '{url}/{hash}?s={size}&d={default}&r={rating}'.format(
            url=url, hash=hash, size=size, default=default, rating=rating)

    @staticmethod
    def insert_avatar():
        for user in User.query.all():
            if user.email is not None and user.avatar_hash is None:
                user.avatar_hash = hashlib.md5(
                    user.email.encode('utf-8')).hexdigest()
                db.session.add(user)
                db.session.commit()


class AnonymousUser(AnonymousUserMixin):
    def can(self, permissions):
        return False

    def is_administrator(self):
        return False

    def vip_(self):
        return False


login_manager.anonymous_user = AnonymousUser


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# category
class Category(db.Model):
    __tablename__ = 'categories'
    cateid = db.Column(db.Integer, primary_key=True)
    cate_name = db.Column(db.String(64), index=True)
    cate_info = db.Column(db.String(64))
    goods = db.relationship('Good', backref='category', lazy='dynamic')

    def __repr__(self):
        return self.cate_name


# goods
class Good(db.Model):
    __tablename__ = 'goods'
    good_id = db.Column(db.Integer, primary_key=True)
    good_name = db.Column(db.String(64), index=True)
    good_info = db.Column(db.Text(1000))
    good_price = db.Column(db.Float, default=0)
    good_sales = db.Column(db.Integer, default=0)
    good_status = db.Column(db.Boolean, default=True)
    cate_id = db.Column(db.Integer, db.ForeignKey('categories.cateid'))
    #kms = db.relationship('KM', backref='good', lazy='dynamic')
    #orders = db.relationship('Order', backref='good', lazy='dynamic')

    def __repr__(self):
        return self.good_name


# km
class KM(db.Model):
    __tablename__ = 'km'
    km_id = db.Column(db.Integer, primary_key=True)
    km_value = db.Column(db.String(64), index=True)
    km_status = db.Column(db.Boolean, default=True)
    good_id = db.Column(db.Integer, db.ForeignKey('goods.good_id'))
    orders = db.relationship('Order', backref='km', lazy='dynamic')

    def __repr__(self):
        return self.km_value

# order


class Order(db.Model):
    __tablename__ = 'orders'
    order_id = db.Column(db.Integer, primary_key=True)
    trade_id = db.Column(db.String(64), index=True)
    trade_status = db.Column(db.Boolean, default=False)
    starttime = db.Column(db.DateTime, default=datetime.datetime.now)
    endtime = db.Column(db.DateTime)
    lx = db.Column(db.Integer)
    good_id = db.Column(db.Integer, db.ForeignKey('goods.good_id'))
    km_id = db.Column(db.Integer, db.ForeignKey('km.km_id'))

    def __repr__(self):
        return self.trade_id
