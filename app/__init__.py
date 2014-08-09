__author__ = 'erik'
from pymongo import MongoClient
from flask import Flask
from flask_login import LoginManager
from flask_mongoengine import MongoEngine

app = Flask(__name__, static_folder='static')
app.config.from_object('config')

dbm = MongoEngine(app)
from app.models import User

lm = LoginManager()
lm.init_app(app)
lm.login_view = 'login'

from app import views


