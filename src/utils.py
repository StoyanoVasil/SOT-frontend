from flask import request, redirect, url_for, session
from functools import wraps
from jose import jwt


def authorized(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' in session:
            if checkToken(session['token']):
                return f(*args, **kwargs)
        return redirect(url_for('login'))
    return decorated_function


def checkToken(token):
    try:
        jwt.decode(token, 'rest_sot_assignment', algorithms=['HS256'])
        return True
    except jwt.JWTError:
        return False
