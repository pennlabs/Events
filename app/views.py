from flask import render_template, session
import json
from app import app


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/events', methods=['GET'])
def events():
    # pass in shit and get a list of paginated events?
    # should be infin-scroll!!
    return json.dumps([])


@app.route('/users/login', methods=['POST'])
def login():
    user = {'username': 'yefim323', 'id': 1}
    # grab user from database based on credentials
    session['user'] = user['id']
    # return user object dump
    return json.dumps(user)


@app.route('/users/create', methods=['POST'])
def create_user():
    user = {'username': 'yefim323', 'id': 1}
    return json.dumps(user)
