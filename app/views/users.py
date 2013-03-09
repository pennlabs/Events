import json

import bcrypt
from flask import session, request

from app import db
from helpers import BSONView, register_api, jsonify


PASSWORDS_DO_NOT_MATCH = 'Passwords do not match'
NO_PASSWORD_PROVIDED = 'No password provided'


class UserAPI(BSONView):
    @property
    def collection_name(self):
        return 'users'

    def post(self):
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
                return jsonify(user)
            else:
                # password != confirm
                return json.dumps({'error': PASSWORDS_DO_NOT_MATCH})
        else:
            # no password was entered
            return json.dumps({'error': NO_PASSWORD_PROVIDED})


register_api(UserAPI, 'user_api', '/users/')
