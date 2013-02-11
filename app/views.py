from flask import render_template
from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user/login', methods=['POST'])
def login():
    return 0


@app.route('/user/create', methods=['POST'])
def create_user():
    return 0
