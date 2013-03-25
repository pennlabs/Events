from __future__ import absolute_import
import json

from pymongo import MongoClient

from app import app


class TestUsersAPI(object):
    ENDPOINT = '/api/users/'

    def setup(self):
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'test'
        self.app = app.test_client()

    def teardown(self):
        connection = MongoClient()
        connection.drop_database('test')
        connection.close()

    def create(self, name, password, email):
        return self.app.post(self.ENDPOINT, data=dict(
            name=name,
            password=password,
            confirm=password,
            email=email,
        ), follow_redirects=True)

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password,
        ), follow_redirects=True)

    def subscribe(self, f_id):
        return self.app.post(self.ENDPOINT + f_id + '/subscriptions',
                             follow_redirects=True)

    def create_event(self, name, description):
        return self.app.post('/api/events/', data=dict(
            name=name,
            description=description
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def get_user(self, _id):
        return self.app.get(self.ENDPOINT + _id)

    def get_events(self, ids):
        return self.app.get('/api/events/', data=dict(
            ids=ids
        ), follow_redirects=True)

    @property
    def users(self):
        rv = self.app.get(self.ENDPOINT)
        return json.loads(rv.data)

    def test_empty(self):
        assert len(self.users) == 0, len(self.users)

    def test_create(self):
        self.create("user1", "pw1", 'email1')
        assert len(self.users) == 1, len(self.users)

    def test_login(self):
        self.create("user1", "pw1", 'email1')
        rv = self.login("email1", "pw1")
        user = json.loads(rv.data)
        assert user['name'] == 'user1', user

    def test_subscriptions(self):
        self.create("user1", "pw1", "email1")
        user2 = self.create("user2", "pw2", "email2")
        u2 = json.loads(user2.data)
        self.login("email1", "pw1")
        r = self.subscribe(u2["_id"])
        sub = json.loads(r.data)
        assert "success" in sub

    def test_event_create(self):
        user1 = self.create("user1", "pw1", "email1")
        u1 = json.loads(user1.data)
        user2 = self.create("user2", "pw2", "email2")
        u2 = json.loads(user2.data)
        # log first user in
        self.login("email1", "pw1")
        # have the first user subscribe to the second
        self.subscribe(u2["_id"])
        # log the first user out
        self.logout()
        # log in as the second user
        self.login("email2", "pw2")
        # create an event
        rv = self.create_event("event1", "best event ever")
        e = json.loads(rv.data)
        assert e["name"] == "event1", e
        new_user1 = self.get_user(u1["_id"])
        new_u1 = json.loads(new_user1.data)
        assert len(new_u1["event_queue"]) == 1
        new_user2 = self.get_user(u2["_id"])
        new_u2 = json.loads(new_user2.data)
        assert len(new_u2["events"]) == 1

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
