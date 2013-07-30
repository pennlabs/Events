from flask import Flask, g
from pymongo import MongoClient

import lib
import views.auth
import views.general
import views.events
import views.users


def get_db(mongo_client, name):
    db = getattr(mongo_client, name)
    db.events.create_index([
        ("description", "text"),
    ])
    return db


def create_app(config="app.config"):
    db = get_db(MongoClient(), config)

    app = Flask(__name__)

    app.config.from_object(config)

    # Override config here
    try:
        app.config.from_envvar('EVENTS_SETTINGS')
    except RuntimeError:
        pass

    # TODO: Do not set anything on g
    @app.before_request
    def before_request():
        g.db = db

        g.current_user = lib.auth.get_current_user()
        if g.current_user:
            g.current_user['logged_in'] = True

    app.register_blueprint(views.auth.auth)
    app.register_blueprint(views.general.general)

    # TODO: Turn these lines into a single blueprint
    lib.views.register_api(app, views.events.EventAPI, 'event_api',
                           'events')
    lib.views.register_api(app, views.users.UserAPI, 'user_api', 'users')
    app.add_url_rule('/api/users/<f_id>/subscriptions',
                     view_func=views.users.subscriptions,
                     methods=['POST', 'DELETE'])
    return app
