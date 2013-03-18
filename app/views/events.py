from helpers import BSONView, register_api, new_event_signal
from app import db
from bson.objectid import ObjectId


class EventAPI(BSONView):
    @property
    def collection_name(self):
        return 'events'

register_api(EventAPI, 'event_api', '/events/')

@new_event_signal.connect
def new_event_triggered(sender=None, **kwargs):
    """
    On the signalling of a new event, add the event to its creator's
    event list.
    """
    u_id = ObjectId(kwargs['u_id'])
    e_id = ObjectId(kwargs['entity']['_id'])
    #insert the event into the creator's event list
    db.users.update({'_id': u_id}, {'$push': {'events': e_id}}, upsert=True)
