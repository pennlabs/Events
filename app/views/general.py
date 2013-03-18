from __future__ import absolute_import

from flask import render_template, session, g
from bson.objectid import ObjectId

from events import app
from events.views.helpers import jsonify


@app.route('/login', methods=['GET'])
@app.route('/')
def index():
    user_id = session.get('user', None)
    if user_id:
        user = jsonify(g.db.users.find_one({'_id': ObjectId(user_id)}))
    else:
        user = {}
    if user:
        del user['hashed_password']
        user['logged_in'] = True
    return render_template('index.html', user=user)
