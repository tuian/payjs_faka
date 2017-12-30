# coding:utf-8
from functools import wraps
from flask import abort, redirect, url_for,g
from flask_login import current_user
from .models import Permission,User
from datetime import datetime
import time


def permission_required(permission):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.can(permission):
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


