from __future__ import absolute_import

from flask import render_template, session, g
from bson.objectid import ObjectId

from app import app
from app.views.helpers import jsonify


@app.route('/all', methods=['GET'])
@app.route('/login', methods=['GET'])
@app.route('/create', methods=['GET'])
@app.route('/')
def index():
    user_id = session.get('user', None)
    if user_id:
        user = g.db.users.find_one({'_id': ObjectId(user_id)})
    else:
        user = {}
    if user:
        del user['hashed_password']
        user['logged_in'] = True
    return render_template('index.html', user=jsonify(user))


@app.route('/event/<event_id>', methods=['GET'])
def event(event_id):
    current_id = session.get('user', None)
    if current_id:
        user = g.db.users.find_one({'_id': ObjectId(current_id)})
    else:
        user = {}
    event_to_render = g.db.events.find_one({'_id': ObjectId(event_id)})
    return render_template('index.html',
                           user=jsonify(user),
                           event_to_render=jsonify(event_to_render))


@app.route('/user/<user_id>', methods=['GET'])
def user(user_id):
    current_id = session.get('user', None)
    if current_id:
        user = g.db.users.find_one({'_id': ObjectId(current_id)})
    else:
        user = {}
    if user:
        del user['hashed_password']
        user['logged_in'] = True
    user_to_render = g.db.users.find_one({'_id': ObjectId(user_id)})
    del user_to_render['hashed_password']
    return render_template('index.html',
                           user=jsonify(user),
                           user_to_render=jsonify(user_to_render))
