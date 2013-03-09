import json

from bson.objectid import ObjectId


# ObjectID can't be serialized so we have our own encoder.
class APIEncoder(json.JSONEncoder):
    # TODO: Strip hashed passwords
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return json.JSONEncoder.default(self, obj)
