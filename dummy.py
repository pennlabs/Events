"""
Script to prepare dummy environment for local development.
"""
import sys
from collections import namedtuple

from app import db

Event = namedtuple('Event', [
    'name',
    'by',
    'date',
    'start',
    'end',
    'location',
    'description',
])

EVENTS = [
    Event('Semi-Annual Pastrami Fest',
          'MEAT Club',
          'Tuesday, January 28',
          '8:00pm',
          '9:00pm',
          'Kings Court English House',
          'Bacon ipsum dolor sit amet nulla ham qui sint exercitation eiusmod commodo, chuck duis velit. Aute in reprehenderit, dolore aliqua non est magna in labore pig pork biltong.',
          ),
    Event('Semi-Annual Vegan Fest',
          'VEG Club',
          'Tuesday, January 28',
          '8:00pm',
          '9:00pm',
          'Kings Court English House',
          'ipsum dolor sit amet nulla ham qui sint exercitation eiusmod commodo, chuck duis velit. Aute in reprehenderit, dolore aliqua non est magna in labore.',
          ),
]


def main():
    """
    Populate the local database with dummies.
    """
    db.events.drop()
    for event in EVENTS:
        db.events.insert(dict(event._asdict()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
