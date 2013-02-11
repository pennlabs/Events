from mongoengine import (connect, Document, EmbeddedDocument, StringField,
                         ReferenceField,
                         EmailField,
                         EmbeddedDocumentField,
                         DateTimeField,
                         GeoPointField,
                         URLField,
                         ListField)

import config


# Connect to the database or create it if it does not exist
connect(config.DB_NAME)


class Event(Document):
    """
    An event created by a group.
    """
    # NOTE: Picture can probably be grabbed from Facebook API
    # NOTE: Enforce uniqueness here?
    name = StringField(required=True)
    description = StringField()
    datetime = DateTimeField()
    location = GeoPointField()

    creators = ListField(ReferenceField('User'))


class User(Document):
    """
    Abstract user.
    """
    name = StringField(required=True, unique=True)
    email = EmailField(required=True, unique=True)


class Student(User):
    """
    A student.
    """
    subscriptions = ListField(EmbeddedDocumentField('Subscription'))


class Subscription(EmbeddedDocument):
    """
    Subscriptions can be created by filtering Events by User, Tag, and Type.
    """
    name = StringField(required=True)
    tags = ListField(ReferenceField('Tag'))


class Tag(Document):
    """
    Arbitrary tag for Events.
    """
    name = StringField(required=True)
