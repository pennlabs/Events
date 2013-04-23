from __future__ import absolute_import

from flask import g, request
from bson.objectid import ObjectId
from datetime import datetime, timedelta

from app.lib.json import jsonify
from app.lib.views import BSONAPI, signals

#creates a signal to be called when an event is made
new_event_signal = signals.signal('new-event-signal')


class EventAPI(BSONAPI):
    collection_name = 'events'

    def index(self):
        """
        Either:
        -   Fetch a list of events (/events/)
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
                'filter': {
                    'date_start': {
                        '$gte':
                        datetime.strptime(request.args['date_start'],
                                           '%m/%d/%Y %I:%M %p')
                    }
                }
            }

            import sys
            sys.stderr.write(str(options) + "\n")

            if 'creator_name' in request.args:
                options['filter'] = {
                    'creator_name': request.args['creator_name'],
                }

            return jsonify(g.db.command("text", "events", **options))
        else:
            return super(EventAPI, self).index()

    def new(self):
        # it might either be in form data or request data
        event = request.form.to_dict() or request.json
        # validate date and time fields
        # http://docs.pyth(on.org/2/library/datetime.html#strftime-strptime-behavior
        # date pattern: "%m/%d/%Y", e.g. "12/31/2000"
        #   %m: Month as a decimal number [01,12].
        #   %d: Day of the month as a decimal number [01,31].
        #   %Y: Year with century as a decimal number.
        # time pattern: "%I:%M %p", e.g. "12:30 pm"
        #   %I: Hour (12-hour clock) as a decimal number [01,12].
        #   %M: Minute as a decimal number [00,59].
        #   %p: Locale's equivalent of either AM or PM.
        date_string = event['date'].strip()
        time_start_string = event['time_start'].strip()
        time_end_string = event['time_end'].strip()
        try:
            date = datetime.strptime(date_string, '%m/%d/%Y')
            time_start = datetime.strptime(time_start_string, '%I:%M %p')
            time_end = datetime.strptime(time_end_string, '%I:%M %p')
        except ValueError:
            return jsonify({'error': 'Invalid date or time.'})
        # if the end time is before the start time, assume it is on the next day
        if time_end < time_start:
            time_end += timedelta(days=1)
        # construct date_start and date_end datetime objects
        date_start = datetime(year=date.year,
                              month=date.month,
                              day=date.day,
                              hour=time_start.hour,
                              minute=time_start.minute)
        date_end = datetime(year=date.year,
                            month=date.month,
                            day=date.day,
                            hour=time_end.hour,
                            minute=time_end.minute)

        event['date_start'] = date_start
        event['date_end'] = date_end

        # add event to events collection
        self.collection.insert(event)
        # signals that a new event was made
        new_event_signal.send(self, event=event, u_id=g.current_user['_id'])
        return jsonify(event)


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
