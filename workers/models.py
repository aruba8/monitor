__author__ = 'erik'

from mongoengine import Document, URLField, StringField, ObjectIdField, IntField, DateTimeField, ListField


class Htmls(Document):
    INT_CHOICE = (0, 1)
    url = URLField()
    html = StringField()
    urlType = ObjectIdField()
    time = StringField()
    date = StringField()
    checked = IntField(choices=INT_CHOICE)
    div = StringField()
    datetime = DateTimeField()


class UserTest(Document):
    username = StringField()
    surname = StringField()
    age = IntField()

    def __unicode__(self):
        return self.username


class Results(Document):
    url = None
    INT_CHOICE = (0, 1)
    areIdentical = IntField(choices=INT_CHOICE)
    compared_objs = ListField(ObjectIdField())
    date = StringField()
    time = StringField()
    datetime = DateTimeField()
    urlType = ObjectIdField()

    def set_url(self, url):
        self.url = url


class Urls(Document):
    INT_CHOICE = (0, 1)
    url = URLField()
    datetime = DateTimeField()
    host = URLField()
    active = IntField(choices=INT_CHOICE)
    path = StringField()
    host_id = ObjectIdField()


class Xpath(Document):
    INT_CHOICE = (0, 1)
    active = IntField(choices=INT_CHOICE)
    xpath = StringField()
    added_datetime = DateTimeField()
    host = URLField()
    host_id = ObjectIdField()




