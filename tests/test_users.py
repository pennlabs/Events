import json

from helpers import TestCase, fake


class TestUsers(TestCase):
    ENDPOINT = '/api/users/'

    def test_empty(self):
        assert len(self.users) == 0, len(self.users)

    def test_create_user(self):
        self.create_user()
        assert len(self.users) == 1, self.users

    def test_subscriptions(self):
        self.create_user()
        user2 = json.loads(self.create_user().data)
        self.login("email1", "pw1")
        sub = json.loads(self.subscribe(user2["_id"]).data)
        assert sub == []

    def test_event_create(self):
        email1, password1 = fake.email(), fake.password()
        u1 = json.loads(self.create_user(email=email1,
                                         password=password1).data)
        email2, password2 = fake.email(), fake.password()
        u2 = json.loads(self.create_user(email=email2,
                                         password=password2).data)
        # log the second user in
        self.login(email2, password2)
        # create an event
        self.create_event("event1", "event1 description")
        # log the second user out
        self.logout()
        # log first user in
        self.login(email1, password1)
        # have the first user subscribe to the second
        self.subscribe(u2["_id"])
        # log the first user out
        self.logout()
        # log in as the second user
        self.login(email2, password2)
        # create another event
        e = json.loads(self.create_event("event2", "event2 description").data)
        # ensure that the event has the correct name
        assert e["name"] == "event2", e
        # ensure that both events are in the first user's event queue
        new_u1 = json.loads(self.get_user(u1["_id"]).data)
        assert len(new_u1["event_queue"]) == 2
        # ensure that both events are in the second user's events
        new_u2 = json.loads(self.get_user(u2["_id"]).data)
        assert len(new_u2["events"]) == 2

    def test_get_events(self):
        email, password = fake.email(), fake.password()
        self.create_user(email=email, password=password)
        self.login(email, password)
        # create an event
        e1 = self.create_event("event1", "best event ever")
        event1 = json.loads(e1.data)
        e2 = self.create_event("event2", "second best")
        event2 = json.loads(e2.data)
        e3 = self.create_event("event3", "third best")
        event3 = json.loads(e3.data)
        ids = [event1["_id"], event2["_id"], event3["_id"]]
        rv = json.loads(self.get_events(ids).data)
        assert len(rv) == 3
