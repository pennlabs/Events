import json

from flask import render_template, session
from bson import ObjectId

from app import app, db
from encoder import APIEncoder


def get_current_user():
    """Get the current user."""
    user_id = session.get('user', None)
    if user_id:
        return db.users.find_one({'_id': ObjectId(user_id)})
    else:
        return {}


@app.route('/login', methods=['GET'])
@app.route('/')
def index():
    user = get_current_user()
    if user:
        del user['hashed_password']
        user['logged_in'] = True
    return render_template('index.html',
                           user=json.dumps(user, cls=APIEncoder))
