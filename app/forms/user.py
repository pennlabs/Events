from wtforms import TextField, PasswordField, validators

from .login import LoginForm


class UserForm(LoginForm):
    name = TextField('Email', [
        validators.Length(min=6, max=35),
        validators.Required(),
    ])
    confirm = PasswordField('Confirm Password', [
        validators.EqualTo('password', message='Passwords must match')
    ])
