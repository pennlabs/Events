import json

from flask import request, session
from flask.views import MethodView
from bson.objectid import ObjectId
from blinker import Namespace

from app import app, db


my_signals = Namespace()
#creates a signal to be called when an event is made
new_event_signal = my_signals.signal('new-event-signal')


class BSONEncoder(json.JSONEncoder):
    """
    Custom encoder for BSON objects.

    (ObjectID can't be serialized so we have our own encoder.)
    """
    # TODO: Strip hashed passwords
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)


def jsonify(entity):
    """
    Convenience wrapper for turning BSON entities into JSON.
    """
    return json.dumps(entity, cls=BSONEncoder)


class BSONView(MethodView):
    """
    Convenience wrapper on MethodView for BSON entities.

    Provides default implementations of HTTP methods.

    To use, override `collection_name` appropriately.
    """
    @property
    def collection_name(self):
        raise NotImplementedError()

    @property
    def collection(self):
        return getattr(db, self.collection_name)

    def get(self, _id):
        """
        Show data about an entity.

        If `_id` is `None`, show data about the collection.
        """
        if _id is None:
            limit = int(request.args.get('limit', 10))
            offset = int(request.args.get('offset', 0))
            entities = list(self.collection.find(skip=offset, limit=limit))
            return jsonify(entities)
        else:
            entity = self.collection.find_one({"_id": ObjectId(_id)})
            return jsonify(entity)

    def post(self):
        """
        Create a new entity.
        """
        entity = request.form.to_dict()
        self.collection.insert(entity)
        #signals that a new event was made
        new_event_signal.send(self, entity=entity, u_id=session['user'])
        return jsonify(entity)


def register_api(view, endpoint, url, pk='_id', pk_type='string'):
    """
    Register a MethodView to the app.

    -   `view` should be the MethodView to register.
    -   `endpoint` will be the name of the of the endpoint that the view will
        have.
    -   `url` should be the base url for the entity. For a 'User' entity, it
        might be '/users/'.
    -   `pk` should be the name for the primary key. Defaults to '_id'.
    -   `pk_type` should be the type of the primary key. Defaults to string.
    """
    view_func = view.as_view(endpoint)
    app.add_url_rule(url,
                     defaults={pk: None},
                     view_func=view_func,
                     methods=['GET'])
    app.add_url_rule(url,
                     view_func=view_func,
                     methods=['POST'])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk),
                     view_func=view_func,
                     methods=['GET', 'PUT', 'DELETE'])
