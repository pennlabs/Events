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

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

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
        user1 = self.create("user1", "pw1", "email1")
        user2 = self.create("user2", "pw2", "email2")
        u2 = json.loads(user2.data)
        rv = self.login("email1", "pw1")
        r = self.subscribe(u2["_id"])
        sub = json.loads(r.data)
        assert "success" in sub
