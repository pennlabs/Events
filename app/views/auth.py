import json

import bcrypt
from flask import session, request

from app import app, db
from helpers import jsonify


INCORRECT_EMAIL_PASSWORD = 'Incorrect email/password'


@app.route('/users/login', methods=['POST'])
def login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if not email or not password:
        return json.dumps({'error': INCORRECT_EMAIL_PASSWORD})
    # grab user from database based on credentials
    user = db.users.find_one({'email': email})
    if not user:
        return json.dumps({'error': INCORRECT_EMAIL_PASSWORD})
    hashed_password = user['hashed_password']
    if bcrypt.hashpw(password, hashed_password) == hashed_password:
        # abstract into pre-serialize user
        del user['hashed_password']
        user['logged_in'] = True
        session['user'] = str(user['_id'])
        # return user object dump
        return jsonify(user)
    else:
        return json.dumps({'error': INCORRECT_EMAIL_PASSWORD})


@app.route('/users/logout', methods=['POST'])
def logout():
    user_id = session.pop('user', -1)
    return json.dumps(user_id)
