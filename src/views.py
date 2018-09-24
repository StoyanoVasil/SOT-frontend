from flask import render_template, request, session, redirect, url_for, json
from src import app
import requests
from src.utils import authorized, admin, get_role, clear_session


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
            token = r.text
            session['token'] = token
            session['role'] = get_role(token)
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
                          data={'email': data['email'].lower(), 'name': data['name'],
                                'password': data['password'], 'role': data['role'].lower()})
        if r.status_code == 201:
            session['token'] = r.text
            return redirect('/')
        elif r.status_code == 409:
            return render_template('register.html', message=r.text)


@app.route('/logout')
@authorized
def logout():
    clear_session()
    return redirect(url_for('login'))


@app.route('/users')
@admin
def all_users():
    r = requests.get(f'{BASE_URL}user/all', headers={'Authorization': session['token']})
    if r.status_code == 200:
        return render_template('all_users.html', users=json.loads(r.text))
    else:
        return redirect('/login')


@app.route('/delete/user/<id>')
@admin
def delete_user(id):
    r = requests.delete(f'{BASE_URL}delete/user/{id}', headers={'Authorization': session['token']})
    if r.status_code == 204:
        return redirect('/users')


@app.route('/rooms/all')
@admin
def all_rooms():
    r = requests.get(f'{BASE_URL}room/all', headers={'Authorization': session['token']})
    if r.status_code == 200:
        return render_template('all_rooms.html', rooms=json.loads(r.text))


@app.route('/delete/room/<id>')
@admin
def delete_room(id):
    r = requests.delete(f'{BASE_URL}delete/room/{id}', headers={'Authorization': session['token']})
    if r.status_code == 204:
        return redirect('/rooms/all')


@app.route('/rooms/free')
@authorized
def get_free_rooms():
    r = requests.get(f'{BASE_URL}room/free', headers={'Authorization': session['token']})
    if r.status_code == 200:
        return render_template('free_rooms.html', rooms=json.loads(r.text))


@app.route('/book/room/<id>')
@authorized
def book_room(id):
    r = requests.get(f'{BASE_URL}book/room/{id}', headers={'Authorization': session['token']})
    if r.status_code == 204:
        return redirect('/') #redirect to my bookings
