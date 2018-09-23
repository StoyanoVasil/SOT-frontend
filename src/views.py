from flask import render_template, request, session, redirect, url_for, json
from src import app
import requests
from src.utils import authorized, admin


BASE_URL = 'http://localhost:8080/rental/api/'


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        r = requests.post(f'{BASE_URL}user/authenticate',
                          data={'email': request.form['email'], 'password': request.form['password']})
        if r.status_code == 200:
            session['token'] = r.text
            return redirect('/')
        elif r.status_code == 401:
            return render_template('login.html', message=r.text)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        data = request.form
        r = requests.post(f'{BASE_URL}new/user',
                          data={'email': data['email'], 'name': data['name'],
                                'password': data['email'], 'role': data['role']})
        if r.status_code == 201:
            session['token'] = r.text
            return redirect('/')
        elif r.status_code == 409:
            return render_template('register.html', message=r.text)


@app.route('/logout')
@authorized
def logout():
    session.pop('token', None)
    return redirect(url_for('login'))


@app.route('/users')
@admin
def all_users():
    r = requests.get(f'{BASE_URL}user/all', headers={'Authorization': session['token']})
    if r.status_code == 200:
        return render_template('all_users.html', users=json.loads(r.text))


@app.route('/delete/user/<id>')
@admin
def delete_user(id):
    r = requests.delete(f'{BASE_URL}remove/user/{id}', headers={'Authorization': session['token']})
    if r.status_code == 204:
        return redirect('/users')

@app.route('/protected')
@admin
def protected():
    return 'logged in'