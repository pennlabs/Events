import json

import bcrypt
from flask import session, request

from app import app, db
from encoder import APIEncoder


PASSWORDS_DO_NOT_MATCH = 'Passwords do not match'
NO_PASSWORD_PROVIDED = 'No password provided'


@app.route('/users/create', methods=['POST'])
def create_user():
    """
    Create a new user from a form.

    If the user forget to supply a password or confirms incorrectly an error
    will be raised.
    """
    user = request.form.to_dict()
    # get password and hash it
    password = request.form.get('password', None)
    confirm = request.form.get('confirm', None)
    if password:
        if password == confirm:
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            user['hashed_password'] = hashed_password
            del user['password']
            del user['confirm']
            # insert returns an ObjectId
            user_id = str(db.users.insert(user))
            # abstract into pre-serialize user
            del user['hashed_password']
            user['logged_in'] = True
            session['user'] = user_id
            return json.dumps(user, cls=APIEncoder)
        else:
            # password != confirm
            return json.dumps({'error': PASSWORDS_DO_NOT_MATCH})
    else:
        # no password was entered
        return json.dumps({'error': NO_PASSWORD_PROVIDED})
