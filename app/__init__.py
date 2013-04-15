from __future__ import absolute_import
from flask import Flask, g
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('config')

db = getattr(MongoClient(), app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = db

from app.views import auth, general, events, users
