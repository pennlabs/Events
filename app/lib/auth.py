import bcrypt
from flask import g, session

from bson.objectid import ObjectId


def hash_password(raw_password):
    return bcrypt.hashpw(raw_password, bcrypt.gensalt())


def authenticate(user, raw_password):
    hashed_password = user['hashed_password']
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
