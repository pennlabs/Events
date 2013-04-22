from __future__ import absolute_import
import json

from flask import request, g, Blueprint

from app.forms.login import LoginForm
from app.lib.auth import authenticate, login_user, logout_user
from app.lib.json import jsonify


UNKNOWN_EMAIL = 'Unknown email'
INCORRECT_EMAIL_PASSWORD = 'Incorrect email/password'

auth = Blueprint('auth', __name__)


@auth.after_request
def after_request(response):
    response.mimetype = 'text/json'
    return response


@auth.route('/login', methods=['POST'])
def login():
    if LoginForm(request.form).validate():
        user = g.db.users.find_one({'email': request.form['email']})
        if user is not None:
            if authenticate(user, request.form['password']):
                login_user(user)

                # abstract into pre-serialize user
                user['logged_in'] = True
                return jsonify(user)
            else:
                return json.dumps({'error': INCORRECT_EMAIL_PASSWORD})
        else:
            return json.dumps({'error': UNKNOWN_EMAIL})
    else:
        return json.dumps({'error': INCORRECT_EMAIL_PASSWORD})


@auth.route('/logout', methods=['POST', 'PUT'])
def logout():
    user_id = logout_user()
    return json.dumps(user_id)
