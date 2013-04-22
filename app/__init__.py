from flask import Flask, g
from pymongo import MongoClient

from app.lib.auth import get_current_user
from app.lib.views import register_api


def create_app(config_filename):
    app = Flask(__name__)
    app.config.from_object(config_filename)

    db = getattr(MongoClient(), app.config['DATABASE'])

    db.events.create_index([
        ("description", "text"),
    ])

    @app.before_request
    def before_request():
        g.db = db

        current_user = get_current_user()
        if current_user:
            current_user['logged_in'] = True
        g.current_user = current_user

    from app.views.general import general
    from app.views.auth import auth
    from app.views.events import EventAPI
    from app.views.users import UserAPI, subscriptions

    app.register_blueprint(auth)
    app.register_blueprint(general)

    register_api(app, EventAPI, 'event_api', 'events')
    register_api(app, UserAPI, 'user_api', 'users')

    app.add_url_rule('/api/users/<f_id>/subscriptions',
                     view_func=subscriptions,
                     methods=['POST', 'DELETE'])

    return app
