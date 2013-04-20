from wtforms import Form, TextField, PasswordField, validators


class LoginForm(Form):
    email = TextField('Email', [
        validators.Length(min=6, max=35),
        validators.Email()
    ])
    password = PasswordField('Password')
