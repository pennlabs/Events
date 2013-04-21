from __future__ import absolute_import

from flask import Flask, g
from pymongo import MongoClient

from app.lib.auth import get_current_user

app = Flask(__name__)
app.config.from_object('config')

db = getattr(MongoClient(), app.config['DATABASE'])

@app.before_request
def before_request():
    g.db = db

    current_user = get_current_user()
    if current_user:
        current_user['logged_in'] = True
    g.current_user = current_user

from app.views import auth, general, events, users
