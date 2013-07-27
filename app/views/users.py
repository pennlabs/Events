from __future__ import absolute_import
import json

from flask import request, g
from bson.objectid import ObjectId

from forms.user import UserForm
from lib.auth import create_user, login_user
from lib.json import jsonify
from lib.views import BSONAPI


PASSWORDS_DO_NOT_MATCH = 'Passwords do not match'
NO_PASSWORD_PROVIDED = 'No password provided'
UNAUTHORIZED_REQUEST = 'User is not logged in'
SUBSCRIBED_SUCCESSFULLY = 'User has subscribed successfully'


class UserAPI(BSONAPI):
    collection_name = 'users'
    form = UserForm

    def new(self):
        user = create_user(request.form['email'], request.form['password'])
        user.update(request.form.to_dict())

        # clean up user object
        user.pop('password')
        user.pop('confirm')
        if not user.get('name', None):
          user['name'] = ' '.join([request.form['first_name'],
                                   request.form['last_name']])

        user_id = g.db.users.insert(user)

        # TODO: find a cleaner way to hardcode the DP user_id
        # dp_user_id = ObjectId("5175d60a137a001de8c3fa6b")
        # dp_events = g.db.users.find_one({'_id': dp_user_id}).get('events', [])

        # all users follow themselves and the DP
        user['following'] = [user_id]
        # user['event_queue'] = dp_events
        user['event_queue'] = []

        g.db.users.update({'_id': user_id},
                          {'$set': {'following': user['following'],
                                    'event_queue': user['event_queue']}})

        login_user(user)

        user['logged_in'] = True
        return jsonify(user)


def subscriptions(f_id):
    if g.current_user is None:
        return json.dumps({'error': UNAUTHORIZED_REQUEST})
    else:
        if request.method == 'POST':
            # TODO Merge the database requests (Supposedly no bulk upserts...)
            o_u_id = ObjectId(g.current_user['_id'])
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
