from __future__ import absolute_import
import json

from flask import request, g

from app import app
from app.lib.auth import authenticate, login_user, logout_user
from app.lib.json import jsonify


INCORRECT_EMAIL_PASSWORD = 'Incorrect email/password'


@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if not email or not password:
        return json.dumps({'error': INCORRECT_EMAIL_PASSWORD})

    # grab user from database based on credentials
    user = g.db.users.find_one({'email': email})
    if user:
        if authenticate(user, password):
            login_user(user)

            # abstract into pre-serialize user
            user['logged_in'] = True
            del user['hashed_password']
            return jsonify(user)
        else:
            return json.dumps({'error': INCORRECT_EMAIL_PASSWORD})
    else:
        return json.dumps({'error': INCORRECT_EMAIL_PASSWORD})


@app.route('/logout', methods=['POST', 'PUT'])
def logout():
    user_id = logout_user()
    return json.dumps(user_id)
