from wtforms import TextField, PasswordField, validators

from .login import LoginForm


class UserForm(LoginForm):
    confirm = PasswordField('Confirm Password', [
        validators.EqualTo('password', message='Passwords must match')
    ])
