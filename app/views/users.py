from __future__ import absolute_import
import json

import bcrypt
from flask import session, request, g
from bson.objectid import ObjectId

from app import app
from app.views.helpers import BSONAPI, register_api, jsonify


PASSWORDS_DO_NOT_MATCH = 'Passwords do not match'
NO_PASSWORD_PROVIDED = 'No password provided'
UNAUTHORIZED_REQUEST = 'User is not logged in'
SUBSCRIBED_SUCCESSFULLY = 'User has subscribed successfully'


class UserAPI(BSONAPI):
    @property
    def collection_name(self):
        return 'users'

    def post(self):
        user = request.form.to_dict()
        # get password and hash it
        password = request.form.get('password', None)
        confirm = request.form.get('confirm', None)
        if password:
            if password == confirm:
                hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
                user['hashed_password'] = hashed_password
                del user['password']
                del user['confirm']
                # insert returns an ObjectId
                user_id = g.db.users.insert(user)
                # all users follow themselves
                g.db.users.update({'_id': user_id},
                                  {'$set': {'following': [user_id]}})
                # abstract into pre-serialize user
                del user['hashed_password']
                user['logged_in'] = True
                session['user'] = str(user_id)
                return jsonify(user)
            else:
                return json.dumps({'error': PASSWORDS_DO_NOT_MATCH})
        else:
            return json.dumps({'error': NO_PASSWORD_PROVIDED})


register_api(UserAPI, 'user_api', 'users')


@app.route('/api/users/<f_id>/subscriptions', methods=['POST', 'DELETE'])
def subscriptions(f_id):
    u_id = session.get('user', None)
    if u_id:
        if request.method == 'POST':
            # TODO Merge the database requests (Supposedly no bulk upserts...)
            o_u_id = ObjectId(u_id)
            o_f_id = ObjectId(f_id)
            # add f_id to u_id's following
            g.db.users.update({'_id': o_u_id},
                              {'$push': {'following': o_f_id}},
                              upsert=True)
            # add u_id to f_id's followers
            g.db.users.update({'_id': o_f_id},
                              {'$push': {'followers': o_u_id}},
                              upsert=True)
            # Get f_id's events and add them to u_id's event queue
            f_events = g.db.users.find_one({'_id': o_f_id}).get('events', [])
            g.db.users.update({'_id': o_u_id},
                              {'$push': {'event_queue': {'$each': f_events}}},
                              upsert=True)
            return json.dumps([str(event_id) for event_id in f_events])
        else:
            # remove f_id from u_id's following
            # remove u_id from f_id's followers
            pass
    else:
        return json.dumps({'error': UNAUTHORIZED_REQUEST})
