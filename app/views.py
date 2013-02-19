from flask import render_template, session, request
import json
from bson.objectid import ObjectId
from app import app, db
import bcrypt


class APIEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


@app.route('/login', methods=['GET'])
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/current')
def current():
    user_id = session.get('user', None)
    if user_id:
        user = db.users.find_one({'_id': ObjectId(user_id)})
        return json.dumps(user, cls=APIEncoder)
    else:
        return json.dumps({})


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
    if not email:
        return "No email was entered."
    if not password:
        return "No password was entered."
    # grab user from database based on credentials
    user = db.users.find_one({'email': email})
    if not user:
        return "There is no user with that email."
    hashed_password = user['hashed_password']
    if bcrypt.hashpw(password, hashed_password) == hashed_password:
        session['user'] = str(user['_id'])
        # return user object dump
        return json.dumps(user, cls=APIEncoder)
    else:
        return "Incorrect password."


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
            session['user'] = user_id
            return json.dumps(user, cls=APIEncoder)
        else:
            # password != confirm
            return "Password does not match confirm."
    else:
        # no password was entered
        return "No password was entered."
