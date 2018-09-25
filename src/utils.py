from flask import request, redirect, url_for, session, render_template
from functools import wraps
from jose import jwt


def authorized(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' in session:
            if __decode_token(session['token']):
                return f(*args, **kwargs)
        return redirect(url_for('index', message='Not authorized!'))
    return decorated_function


def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' in session:
            decoded = __decode_token(session['token'])
            if decoded and decoded['sub'] == 'admin':
                return f(*args, **kwargs)
        return redirect(url_for('index', message='Not authorized!'))
    return decorated_function


def __decode_token(token):
    try:
        return jwt.decode(token, 'rest_sot_assignment', algorithms=['HS256'])
    except jwt.JWTError:
        clear_session()
        return None


def get_role(token):
    decoded = __decode_token(token)
    return decoded['sub']


def clear_session():
    session.pop('token', None)
    session.pop('role', None)
