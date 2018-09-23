from flask import render_template, request, session, redirect, url_for
from src import app
import requests
from src.utils import authorized


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        r = requests.post('http://localhost:8080/rental/api/user/authenticate',
                            data={'email': request.form['email'], 'password': request.form['password']})
        if r.status_code == 200:
            session['token'] = r.text
            return '' #TODO: home page
        elif r.status_code == 401:
            #TODO: unsuccessful login
            return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        data = request.form
        r = requests.post('http://localhost:8080/rental/api/new/user',
                          data={'email': data['email'], 'name': data['name'],
                                'password': data['email'], 'role': data['role']})
        if r.status_code == 201:
            session['token'] = r.text
            return '' #TODO: home page
        elif r.status_code == 409:
            #TODO: email in use
            return render_template('register.html')


@app.route('/logout')
def logout():
    session.pop('token', None)
    return redirect(url_for('login'))
