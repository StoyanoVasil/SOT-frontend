from flask import request, redirect, url_for, session, render_template
from functools import wraps
from jose import jwt


def authorized(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' in session:
            if decodeToken(session['token']):
                return f(*args, **kwargs)
        return render_template('login.html', message="Please log in")
    return decorated_function


def admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'token' in session:
            decoded = decodeToken(session['token'])
            if decoded and decoded['sub'] == 'admin':
                return f(*args, **kwargs)
            return redirect('/')
    return decorated_function

def decodeToken(token):
    try:
        return jwt.decode(token, 'rest_sot_assignment', algorithms=['HS256'])
    except jwt.JWTError:
        return None
