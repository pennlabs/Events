import urlparse

from flask import request, Response, g
from flask.views import MethodView
from bson.objectid import ObjectId
from blinker import Namespace

from .json import jsonify

API_PREFIX = '/api/'


signals = Namespace()


class DocumentView(MethodView):
    """
    Convenience wrapper on MethodView for BSON entities.

    Provides default implementations of HTTP methods.

    To use, override `collection_name` appropriately.
    """
    collection_name = None

    @property
    def collection(self):
        return getattr(g.db, self.collection_name)

    def get(self, _id):
        """
        Show data about an entity.

        If `_id` is `None`, show data about the collection.
        """
        if _id is None:
            ids = request.args.getlist('ids[]')
            if len(ids) == 0:
                limit = int(request.args.get('limit', 10))
                offset = int(request.args.get('offset', 0))
                rv = list(self.collection.find(skip=offset, limit=limit))
            else:
                rv = list(self.collection.find(
                    {"_id": {"$in": [ObjectId(id) for id in ids]}}
                ))
        else:
            rv = self.collection.find_one({"_id": ObjectId(_id)})
        return Response(jsonify(rv), mimetype='text/json')

    def new(self):
        """Create a new entity."""
        entity = request.form.to_dict()
        self.collection.insert(entity)
        return Response(jsonify(entity), mimetype='text/json')

    def post(self):
        return self.new()


class BSONAPI(DocumentView):
    form = None

    def post(self):
        """Validate form data from a post request."""
        if self.form is not None:
            form = self.form(request.form)
            if not form.validate():
                return Response(jsonify({'error': form.errors}),
                                mimetype='text/json')
        return super(BSONAPI, self).post()


def register_api(app, view, endpoint, url, pk='_id', pk_type='string'):
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
    assert not url.startswith('/')
    url = urlparse.urljoin(API_PREFIX, url) + '/'
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
