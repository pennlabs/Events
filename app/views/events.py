from __future__ import absolute_import

from flask import g, request, session
from bson.objectid import ObjectId

from app import app, db
from app.lib.json import jsonify
from app.lib.views import BSONAPI, register_api, signals

db.events.create_index([("description", "text"),])

#creates a signal to be called when an event is made
new_event_signal = signals.signal('new-event-signal')


class EventAPI(BSONAPI):
    @property
    def collection_name(self):
        return 'events'

    def get(self, _id=None):
        """
        Either:
        -   Fetch a list of events (/events/)
        -   Fetch a single event (/events/<id>)
        -   Search all events for a keyword. (/events/?q=keyword)
            -   Results will limited to 10 unless 'limit' is specified
            -   If 'creator_name' is given, results will be filtered to be only
                those events created by 'creator_name'
        """
        if 'q' in request.args:
            options = {
                'search': request.args['q'],
                'limit': (int(request.args['limit'])
                          if 'limit' in request.args else 10),
            }

            if 'creator_name' in request.args:
                options['filter'] = {
                    'creator_name': request.args['creator_name'],
                }

            return jsonify(db.command("text", "events", **options))
        else:
            return super(EventAPI, self).get(_id)

    def post(self):
        # it might either be in form data or request data
        event = request.form.to_dict() or request.json
        self.collection.insert(event)
        # signals that a new event was made
        new_event_signal.send(self, event=event, u_id=session['user'])
        return jsonify(event)

register_api(app, EventAPI, 'event_api', 'events')


@new_event_signal.connect
def new_event_triggered(sender=None, **kwargs):
    """
    When an event is created, add the event to its creator's event list.
    """
    u_id = ObjectId(kwargs['u_id'])
    e_id = ObjectId(kwargs['event']['_id'])
    # insert the event into the creator's event list
    g.db.users.update({'_id': u_id}, {'$push': {'events': e_id}}, upsert=True)
    # insert e_id into followers' event queues
    g.db.users.update({'following': u_id},
                      {'$push': {'event_queue': e_id}},
                      upsert=True, multi=True)
