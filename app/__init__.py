__author__ = 'erik'
from pymongo import MongoClient
from flask import Flask
from flask.ext.login import LoginManager

app = Flask(__name__, static_folder='static')
app.config.from_object('config')

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

client = MongoClient('mongodb://localhost')
db = client.diffs
from app import views


