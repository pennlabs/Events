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
        connection.drop_database(self.app.application.config['DATABASE'])
        connection.close()

    def subscribe(self, f_id):
        return self.app.post('/api/users/%s/subscriptions' % f_id,
                             follow_redirects=True)

    def get_user(self, _id):
        return self.app.get('/api/users/%s' % _id)

    @property
    def users(self):
        rv = self.app.get('/api/users/')
        return json.loads(rv.data)

    def login(self, email, password):
        return self.app.post('/login', data=dict(
            email=email,
            password=password,
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def create_user(self, name, email, password, confirm=None):
        if confirm is None:
            confirm = password
        return self.app.post('/api/users/', data=dict(
            name=name,
            email=email,
            password=password,
            confirm=confirm,
        ), follow_redirects=True)

    def create_event(self, name, description):
        return self.app.post('/api/events/', data=dict(
            name=name,
            description=description
        ), follow_redirects=True)

    def get_events(self, ids):
        return self.app.get('/api/events/', data=dict(
            ids=ids
        ), follow_redirects=True)
