#!/usr/bin/python
from comparing import Comparator

__author__ = 'erik'

from pymongo import MongoClient
from urllib2 import urlopen

connection_string = "mongodb://localhost"
connection = MongoClient(connection_string)
database = connection.diffs

url1 = 'http://www.immigratemanitoba.com/how-to-immigrate/apply/recruitment-missions/'

url2 = 'http://www.immigratemanitoba.com/how-to-immigrate/apply/exploratory-visits/'


def get_page_as_string(url):
    return urlopen(url).read().strip()



if __name__ == '__main__':
    from diffdb import HtmlDAO

    htm1 = get_page_as_string(url1)
    htm2 = get_page_as_string(url2)
    dao = HtmlDAO(database)
    dao.insert_html(htm1, url1, 1)
    dao.insert_html(htm2, url2, 2)

    comparator = Comparator(database)
    comparator.compare(1)
    comparator.compare(2)


