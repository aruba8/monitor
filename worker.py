#!/usr/bin/python

__author__ = 'erik'

from urllib2 import urlopen

from pymongo import MongoClient


connection_string = "mongodb://localhost"
connection = MongoClient(connection_string)
database = connection.diffs

url1 = (1, 'http://www.immigratemanitoba.com/how-to-immigrate/apply/recruitment-missions/')
url2 = (2, 'http://www.immigratemanitoba.com/how-to-immigrate/apply/exploratory-visits/')
url3 = (3, 'http://www.immigratemanitoba.com/how-to-immigrate/mpnp-resources/')

urls = [url1, url2, url3]


def get_page_as_string(url):
    return urlopen(url).read().strip()


from comparing import Comparator
from diffdb import HtmlDAO

dao = HtmlDAO(database)
comparator = Comparator(database)


def do_work():
    for url in urls:
        htm = get_page_as_string(url[1])
        dao.insert_html(htm, url[1], url[0])
        comparator.compare(url[0])
        comparator.check(url[0])


if __name__ == '__main__':
    do_work()




