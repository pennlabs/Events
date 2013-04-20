import bcrypt
from flask import session


def hash_password(raw_password):
    return bcrypt.hashpw(raw_password, bcrypt.gensalt())


def authenticate(user, raw_password):
    hashed_password = user['hashed_password']
    return bcrypt.hashpw(raw_password, hashed_password) == hashed_password


def login_user(user):
    user['logged_in'] = True
    session['user'] = str(user['_id'])


def logout_user():
    user_id = session.pop('user', -1)
    return user_id
