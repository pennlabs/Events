import json

from app.tests import TestCase, fake


class TestAuth(TestCase):
    def test_create_user(self):
        name, email, password = fake.name(), fake.email(), fake.password()
        rv = self.create_user(name, email, password)
        user = json.loads(rv.data)
        assert 'name' in user, user

    def test_login(self):
        name, email, password = fake.name(), fake.email(), fake.password()
        self.create_user(name, email, password)
        rv = self.login(email, password)
        user = json.loads(rv.data)
        assert 'name' in user, user
        assert user['name'] == name, user['name']
