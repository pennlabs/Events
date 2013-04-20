from __future__ import absolute_import

import json

from bson.objectid import ObjectId


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
