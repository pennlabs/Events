from flask import render_template, session, request
import json
from bson.objectid import ObjectId
from app import app, db
import bcrypt


INCORRECT_EMAIL_PASSWORD = 'Incorrect email/password'
PASSWORDS_DO_NOT_MATCH = 'Passwords do not match'
NO_PASSWORD_PROVIDED = 'No password provided'


class APIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


@app.route('/login', methods=['GET'])
@app.route('/')
def index():
    user_id = session.get('user', None)
    user = {}
    if user_id:
        user = db.users.find_one({'_id': ObjectId(user_id)})
        del user['hashed_password']
        user['logged_in'] = True
    return render_template('index.html',
                           user=json.dumps(user, cls=APIEncoder))


@app.route('/events', methods=['GET'])
def events():
    # find the events based on the user
    # grab subscriptions then get events
    # returns a cursor
    # db.events.find()[:]
    # pass in shit and get a list of paginated events?
    # should be infin-scroll!!
    return json.dumps([])


@app.route('/users/logout', methods=['POST'])
def logout():
    user_id = session.pop('user', -1)
    return json.dumps(user_id)


@app.route('/users/login', methods=['POST'])
def login():
    email = request.form.get('email', None)
    password = request.form.get('password', None)
    if not email or not password:
        return json.dumps({'error': INCORRECT_EMAIL_PASSWORD})
    # grab user from database based on credentials
    user = db.users.find_one({'email': email})
    if not user:
        return json.dumps({'error': INCORRECT_EMAIL_PASSWORD})
    hashed_password = user['hashed_password']
    if bcrypt.hashpw(password, hashed_password) == hashed_password:
        # abstract into pre-serialize user
        del user['hashed_password']
        user['logged_in'] = True
        session['user'] = str(user['_id'])
        # return user object dump
        return json.dumps(user, cls=APIEncoder)
    else:
        return json.dumps({'error': INCORRECT_EMAIL_PASSWORD})


@app.route('/users/create', methods=['POST'])
def create_user():
    user = request.form.to_dict()
    # get password and hash it
    password = request.form.get('password', None)
    confirm = request.form.get('confirm', None)
    if password:
        if password == confirm:
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            user['hashed_password'] = hashed_password
            del user['password']
            del user['confirm']
            # insert returns an ObjectId
            user_id = str(db.users.insert(user))
            # abstract into pre-serialize user
            del user['hashed_password']
            user['logged_in'] = True
            session['user'] = user_id
            return json.dumps(user, cls=APIEncoder)
        else:
            # password != confirm
            return json.dumps({'error': PASSWORDS_DO_NOT_MATCH})
    else:
        # no password was entered
        return json.dumps({'error': NO_PASSWORD_PROVIDED})
