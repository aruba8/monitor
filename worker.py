#!/usr/bin/python

__author__ = 'erik'

from urllib2 import urlopen

from pymongo import MongoClient


connection_string = "mongodb://localhost"
connection = MongoClient(connection_string)
database = connection.diffs

url1 = 'http://www.immigratemanitoba.com/how-to-immigrate/apply/recruitment-missions/'
url2 = 'http://www.immigratemanitoba.com/how-to-immigrate/apply/exploratory-visits/'
url3 = 'http://www.immigratemanitoba.com/how-to-immigrate/mpnp-resources/'

urls = [url1, url2, url3]


def get_page_as_string(url):
    return urlopen(url).read().strip()



if __name__ == '__main__':
    from comparing import Comparator
    from diffdb import HtmlDAO
    dao = HtmlDAO(database)
    comparator = Comparator(database)

    for url, i in zip(urls, range(len(urls))):
        htm = get_page_as_string(url)
        dao.insert_html(htm, url, i + 1)
        comparator.compare(i + 1)
        comparator.check(i + 1)




