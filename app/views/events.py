from __future__ import absolute_import
from flask import g, request, session
from blinker import Namespace
from bson.objectid import ObjectId
from conmongo.views import BSONAPI

from app import app


signals = Namespace()

#creates a signal to be called when an event is made
new_event_signal = signals.signal('new-event-signal')


@app.resource('/api/events/')
class EventAPI(BSONAPI):
    @property
    def collection_name(self):
        return 'events'

    def post(self):
        print "posting event works"
        entity = request.form.to_dict()
        self.collection.insert(entity)
        #signals that a new event was made
        new_event_signal.send(self, entity=entity, u_id=session['user'])
        return entity


@new_event_signal.connect
def new_event_triggered(sender=None, **kwargs):
    """
    On the signalling of a new event, add the event to its creator's
    event list.
    """
    print "event triggerd"
    u_id = ObjectId(kwargs['u_id'])
    e_id = ObjectId(kwargs['entity']['_id'])
    # insert the event into the creator's event list
    g.db.users.update({'_id': u_id}, {'$push': {'events': e_id}}, upsert=True)
    # insert e_id into followers' event queues
    # TODO: write tests to ensure that all followers' event queues are updated
    g.db.users.update({'following': u_id},
                      {'$push': {'event_queue': e_id}},
                      upsert=True, multi=True)
