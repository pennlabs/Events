from __future__ import absolute_import
from flask import Flask, g
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('config')
app.config['DATABASE'] = 'events'


@app.before_request
def before_request():
    g._connection = connection = MongoClient()
    g.db = getattr(connection, app.config['DATABASE'])


@app.teardown_request
def teardown_request(exception):
    g._connection.close()

from events.views import auth, general, events, users
