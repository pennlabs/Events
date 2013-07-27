#!/usr/bin/env python
from __future__ import absolute_import

from flask import Flask, g
from pymongo import MongoClient

import lib
import views.auth
import views.general
import views.events
import views.users


if __name__ == "__main__":
    app = Flask(__name__)

    app.config.from_object('config')

    # Override config here
    try:
        app.config.from_envvar('EVENTS_SETTINGS')
    except RuntimeError:
        pass

    db = getattr(MongoClient(), app.config['DATABASE'])
    db.events.create_index([
        ("description", "text"),
    ])

    @app.before_request
    def before_request():
        g.db = db

        g.current_user = lib.auth.get_current_user()
        if g.current_user:
            g.current_user['logged_in'] = True

    app.register_blueprint(views.auth.auth)
    app.register_blueprint(views.general.general)

    lib.views.register_api(app, views.events.EventAPI, 'event_api', 'events')
    lib.views.register_api(app, views.users.UserAPI, 'user_api', 'users')

    app.add_url_rule('/api/users/<f_id>/subscriptions',
                     view_func=views.users.subscriptions,
                     methods=['POST', 'DELETE'])

    app.run()
