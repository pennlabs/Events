import bcrypt
from flask import g, session

from bson.objectid import ObjectId


PASSWORD_FIELDNAME = 'hashed_password'


def _hash_password(raw_password):
    return bcrypt.hashpw(raw_password, bcrypt.gensalt())


def create_user(email, password):
    return {'email': email, PASSWORD_FIELDNAME: _hash_password(password)}


def authenticate(user, raw_password):
    hashed_password = user[PASSWORD_FIELDNAME]
    return bcrypt.hashpw(raw_password, hashed_password) == hashed_password


def get_current_user():
    user_id = session.get('user', None)
    if user_id:
        return g.db.users.find_one({'_id': ObjectId(user_id)})
    else:
        return None


def login_user(user):
    session['user'] = str(user['_id'])


def logout_user():
    user_id = session.pop('user', -1)
    return user_id
