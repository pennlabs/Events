from helpers import BSONView, register_api


class EventAPI(BSONView):
    @property
    def collection_name(self):
        return 'events'

register_api(EventAPI, 'event_api', '/events/')
