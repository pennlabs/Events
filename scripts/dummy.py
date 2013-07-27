"""
Script to prepare dummy environment for local development.

Usage: python dummy.py [database_name] [num_dummy_events]

"""
import sys

from faker import Factory
from pymongo import MongoClient

fake = Factory.create()

def create_arbitrary_event():
    """Create a dummy event."""
    return {
        'name': "".join(fake.words()).title(),
        'creator_name': fake.company(),
        'date': "%s %s" % (fake.monthName(), fake.dayOfMonth()),
        'start': fake.time(),
        'end': fake.time(),
        'location': fake.address(),
        'description': fake.text(),
    }


def create_arbitrary_events(n):
    """Create a number of dummy events."""
    for _ in xrange(n):
        yield create_arbitrary_event()


def main(database, n=None):
    """
    Populate the local database with dummies.
    """
    if n is None:
        n = 20
    db = getattr(MongoClient(), database)
    db.events.drop()
    for event in create_arbitrary_events(n):
        db.events.insert(event)
    return 0


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
