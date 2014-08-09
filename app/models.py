from app import dbm

ROLE_USER = 0
ROLE_ADMIN = 1


class User(dbm.Document):
    login = dbm.StringField(max_length=80, min_length=3, unique=True)
    password = dbm.StringField()
    active = dbm.BooleanField()

    def is_authenticated(self):
        return True

    def is_active(self):
        return self.active

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.login)

    def get_password(self):
        return str(self.password)

    def __unicode__(self):
        return self.login


class Html(dbm.Document):
    INT_CHOICE = (0, 1)
    url = dbm.URLField()
    html = dbm.StringField()
    url_type = dbm.ObjectIdField()
    time = dbm.StringField()
    date = dbm.StringField()
    checked = dbm.IntField(choices=INT_CHOICE)
    div = dbm.StringField()
    datetime = dbm.DateTimeField()