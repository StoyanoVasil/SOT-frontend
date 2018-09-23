from flask import render_template, request, Response, json
from src import app

@app.route('/')
def index():
    return 'Hello sot'