from flask import Flask
from pymongo import MongoClient

app = Flask(__name__)
app.config.from_object('config')

connection = MongoClient()
db = connection.events

from app import views
