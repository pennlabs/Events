from __future__ import absolute_import

from flask import Flask
from conmongo.app import MongoApp

app = MongoApp(Flask(__name__))
app.config.from_object('config')

from app.views import auth, general, events, users
