import json

from helpers import TestCase, fake


class TestAuth(TestCase):
    def test_create_user(self):
        name, email, password = fake.name(), fake.email(), fake.password()
        rv = self.create_user(name, email, password)
        assert rv.mimetype == 'text/json', rv.mimetype
        user = json.loads(rv.data)
        assert 'name' in user, user
        assert 'email' in user, user
        assert 'password' not in user, user
        assert 'confirm' not in user, user

    def test_confirm_doesnt_match_password(self):
        name, email, password = fake.name(), fake.email(), fake.password()
        rv = self.create_user(name, email, password, password[1:])
        assert rv.mimetype == 'text/json', rv.mimetype
        assert 'error' in json.loads(rv.data), rv.data

    def test_bad_email(self):
        name, email, password = fake.name(), fake.name(), fake.password()
        rv = self.create_user(name, email, password)
        assert rv.mimetype == 'text/json', rv.mimetype
        assert 'error' in json.loads(rv.data), rv.data

    def test_short_password(self):
        name, email, password = fake.name(), fake.name(), "123"
        rv = self.create_user(name, email, password)
        assert rv.mimetype == 'text/json', rv.mimetype
        assert 'error' in json.loads(rv.data), rv.data

    def test_login(self):
        name, email, password = fake.name(), fake.email(), fake.password()
        self.create_user(name, email, password)
        rv = self.login(email, password)
        assert rv.mimetype == 'text/json', rv.mimetype
        user = json.loads(rv.data)
        assert 'name' in user, user
        assert 'email' in user, user
        assert 'password' not in user, user
        assert 'confirm' not in user, user

    def test_logout(self):
        name, email, password = fake.name(), fake.email(), fake.password()
        self.create_user(name, email, password)
        self.login(email, password).data
        rv = self.logout()
        assert rv.mimetype == 'text/json', rv.mimetype
        assert 'success' in json.loads(rv.data)
