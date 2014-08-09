__author__ = 'erik'

import hmac
import random
import string
import hashlib

from bson.objectid import ObjectId
from utils.logerconf import Logger

logger = Logger()
log = logger.get_logger()
from app.models import User


class Sessions:
    def __init__(self, database_diffs):
        self.sessions = database_diffs.sessions
        self.users = database_diffs.users

    def get_session(self, session_id):

        # this may fail because the string may not be a valid bson objectid
        try:
            _id = ObjectId(session_id)
        except:
            log.info("bad sessionid passed in")
            return None

        session = self.sessions.find_one({'_id': _id})

        log.info("returning a session or none")
        return session

    def start_session(self, user_id):
        session = {'username': user_id}

        try:
            self.sessions.insert(session, safe=True)
        except:
            log.error("Unexpected error on start_session:")
            return -1

        return str(session['_id'])

    # will send a new user session by deleting from sessions table
    def end_session(self, session_id):
        # this may fail because the string may not be a valid bson objectid
        try:
            _id = ObjectId(session_id)
            self.sessions.remove({'_id': _id})
        except:
            return

            # validates the login, returns True if it's a valid user login. false otherwise

    def validate_login(self, username, password, user_record):
        user = User.objects(username=username).first()
        if user is None:
            log.warn("User not in database")
            return False

        salt = user['password'].split(',')[1]
        if user['password'] != self.make_pw_hash(password, salt):
            log.warn("user password is not a match")
            return False

        # looks good

        for key in user:
            user_record[key] = user[key]  # perform a copy

        return True

    # implement the function make_pw_hash(name, pw) that returns a hashed password
    # of the format:
    # HASH(pw + salt),salt
    # use sha256

    def make_pw_hash(self, pw, salt=None):
        if salt is None:
            salt = self.make_salt()
        return hashlib.sha256(pw + salt).hexdigest() + "," + salt

    # makes a little salt
    def make_salt(self):
        salt = ""
        for i in range(5):
            salt = salt + random.choice(string.ascii_letters)
        return salt

    def login_check(self, cookie):

        if cookie is None:
            log.info("no cookie...")
            return None

        else:
            session_id = self.check_secure_val(cookie)

            if session_id is None:
                log.info("no secure session_id")
                return None

            else:
                # look up username record
                session = self.get_session(session_id)
                if session is None:
                    return None

        return session['username']

    def check_secure_val(self, h):
        val = h.split('|')[0]
        if h == self.make_secure_val(val):
            return val

    def make_secure_val(self, s):
        return "%s|%s" % (s, self.hash_str(s))

    SECRET = 'VerySecret'

    def hash_str(self, s):
        return hmac.new(self.SECRET, s).hexdigest()

    # creates a new user in the database
    def new_user(self, username, password):
        password_hash = self.make_pw_hash(password)

        try:
            User(username=username, password=password_hash, active=True).save()
        except:
            log.error("oops, username: " + username + " is already taken")
            return False
        return True

    def validate_new_user(self, username, password, confirm, secret_word):
        from utils.configparser import Parser

        config = Parser()
        if username is None or username == '':
            return False
        if password != confirm:
            return False
        if secret_word != config.get_secret_word():
            return False
        return True