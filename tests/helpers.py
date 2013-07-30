import time
import datetime
import json

from pymongo import MongoClient
from faker import Factory

from app import create_app


fake = Factory.create()


def password(n=10):
    word = ""
    while len(word) < n:
        word += fake.word()
    return word
fake.password = password


class TestCase(object):
    def setup(self):
        app = create_app('test')
        app.testing = True
        self.app = app.test_client()

    def teardown(self):
        connection = MongoClient()
        connection.drop_database('test')
        connection.close()

    def subscribe(self, f_id):
        return self.app.post('/api/users/%s/subscriptions' % f_id,
                             follow_redirects=True)

    def get_user(self, _id):
        return self.app.get('/api/users/%s' % _id)

    @property
    def users(self):
        response = self.app.get('/api/users/')
        return json.loads(response.data)

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password,
        ), follow_redirects=True)

    def logout(self):
        return self.app.post('/logout', follow_redirects=True)

    def create_user(self, name=None, email=None, password=None, confirm=None):
        if name is None:
            name = fake.name()
        if email is None:
            email = fake.email()
        if password is None:
            password = fake.password()
        if confirm is None:
            confirm = password
        return self.app.post('/api/users/', data=dict(
            name=name,
            email=email,
            password=password,
            confirm=confirm,
        ), follow_redirects=True)

    def create_event(self,
                     name,
                     description,
                     date=None,
                     time_start=None,
                     time_end=None,
                     ):
        if date is None:
            date = "12/31/2013"
        if time_start is None:
            time_start = "12:30 pm"
        if time_end is None:
            time_end = "1:30 pm"
        return self.app.post('/api/events/', data=dict(
            name=name,
            description=description,
            date=date,
            time_start=time_start,
            time_end=time_end,
        ), follow_redirects=True)

    def get_events(self, ids):
        return self.app.get('/api/events/', data=dict(
            ids=ids
        ), follow_redirects=True)
