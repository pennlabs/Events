from __future__ import absolute_import

import json

from bson.objectid import ObjectId

from .auth import PASSWORD_FIELDNAME


class BSONEncoder(json.JSONEncoder):
    """
    JSON encoder for BSON data.
    """
    # TODO: Strip hashed passwords
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super(BSONEncoder, self).default(self, obj)


def jsonify(entity):
    """
    Convenience wrapper for turning BSON entities into JSON.

    Strips sensitive data from entities.
    """
    # Do not serialize hashed_passwords
    try:
        del entity[PASSWORD_FIELDNAME]
    except KeyError:
        pass
    return json.dumps(entity, cls=BSONEncoder)
