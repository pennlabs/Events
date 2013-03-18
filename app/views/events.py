from __future__ import absolute_import
from app.views.helpers import BSONAPI, register_api


class EventAPI(BSONAPI):
    @property
    def collection_name(self):
        return 'events'

register_api(EventAPI, 'event_api', 'events')
