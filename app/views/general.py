from __future__ import absolute_import

from flask import render_template, g
from bson.objectid import ObjectId

from app import app
from app.lib.json import jsonify


@app.route('/all', methods=['GET'])
@app.route('/login', methods=['GET'])
@app.route('/create', methods=['GET'])
@app.route('/')
def index():
    return render_template('index.html', user=jsonify(g.current_user))


@app.route('/event/<event_id>', methods=['GET'])
def event(event_id):
    event_to_render = g.db.events.find_one({'_id': ObjectId(event_id)})
    return render_template('index.html',
                           user=jsonify(g.current_user),
                           event_to_render=jsonify(event_to_render))


@app.route('/user/<user_id>', methods=['GET'])
def user(user_id):
    user_to_render = g.db.users.find_one({'_id': ObjectId(user_id)})
    return render_template('index.html',
                           user=jsonify(g.current_user),
                           user_to_render=jsonify(user_to_render))
