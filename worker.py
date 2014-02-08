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


if __name__ == '__main__':
    htm = get_page_as_string(url1[1])
    htm = get_page_as_string(url2[1])
    htm = get_page_as_string(url3[1])
    comparator.compare(url1[0])
    comparator.compare(url2[0])
    comparator.compare(url3[0])
    comparator.check(url1[0])
    comparator.check(url2[0])
    comparator.check(url3[0])




