from __future__ import absolute_import

from flask import request, g, Blueprint

from forms.login import LoginForm
from lib.auth import authenticate, login_user, logout_user
from lib.json import jsonify


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
                return jsonify({'error': INCORRECT_EMAIL_PASSWORD})
        else:
            return jsonify({'error': UNKNOWN_EMAIL})
    else:
        return jsonify({'error': INCORRECT_EMAIL_PASSWORD})


@auth.route('/logout', methods=['POST', 'PUT'])
def logout():
    logout_user()
    return jsonify({'success': 'Successfully logged out'})
