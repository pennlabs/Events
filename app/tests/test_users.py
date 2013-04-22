import json

from app.tests import TestCase


class TestUsers(TestCase):
    ENDPOINT = '/api/users/'

    def test_empty(self):
        assert len(self.users) == 0, len(self.users)

    def test_create(self):
        self.create("user1", "pw1", 'email1')
        assert len(self.users) == 1, len(self.users)

    def test_subscriptions(self):
        self.create("user1", "pw1", "email1")
        user2 = self.create("user2", "pw2", "email2")
        u2 = json.loads(user2.data)
        self.login("email1", "pw1")
        r = self.subscribe(u2["_id"])
        sub = json.loads(r.data)
        assert sub == []

    def test_event_create(self):
        user1 = self.create("user1", "pw1", "email1")
        u1 = json.loads(user1.data)
        user2 = self.create("user2", "pw2", "email2")
        u2 = json.loads(user2.data)
        # log the second user in
        self.login("email2", "pw2")
        # create an event
        self.create_event("event1", "event1 description")
        # log the second user out
        self.logout()
        # log first user in
        self.login("email1", "pw1")
        # have the first user subscribe to the second
        self.subscribe(u2["_id"])
        # log the first user out
        self.logout()
        # log in as the second user
        self.login("email2", "pw2")
        # create another event
        rv = self.create_event("event2", "event2 description")
        e = json.loads(rv.data)
        # ensure that the event has the correct name
        assert e["name"] == "event2", e
        # ensure that both events are in the first user's event queue
        new_user1 = self.get_user(u1["_id"])
        new_u1 = json.loads(new_user1.data)
        assert len(new_u1["event_queue"]) == 2
        # ensure that both events are in the second user's events
        new_user2 = self.get_user(u2["_id"])
        new_u2 = json.loads(new_user2.data)
        assert len(new_u2["events"]) == 2
    
    def test_get_events(self):
        self.create("user1", "pw1", "email1")
        self.login("email1", "pw1")
        # create an event
        e1 = self.create_event("event1", "best event ever")
        event1 = json.loads(e1.data)
        e2 = self.create_event("event2", "second best")
        event2 = json.loads(e2.data)
        e3 = self.create_event("event3", "third best")
        event3 = json.loads(e3.data)
        ids = [event1["_id"], event2["_id"], event3["_id"]]
        rv = self.get_events(ids)
        rv = json.loads(rv.data)
        assert len(rv) == 3
