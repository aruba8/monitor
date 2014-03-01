#!/usr/bin/python

__author__ = 'erik'

from urllib2 import urlopen
import time
from datetime import datetime

from pymongo import MongoClient
import schedule


def do_job():
    print(str(datetime.now()) + ' Job started')
    dao.insert_html(get_page_as_string(url1), url1, 1)
    dao.insert_html(get_page_as_string(url2), url2, 2)
    dao.insert_html(get_page_as_string(url3), url3, 3)
    comparator.compare(1)
    comparator.compare(2)
    comparator.compare(3)
    comparator.check(1)
    comparator.check(2)
    comparator.check(3)
    print('Job ended')


schedule.every(1).hours.do(do_job)

connection_string = "mongodb://localhost"
connection = MongoClient(connection_string)
database = connection.diffs

url1 = 'http://www.immigratemanitoba.com/how-to-immigrate/apply/recruitment-missions/'
url2 = 'http://www.immigratemanitoba.com/how-to-immigrate/apply/exploratory-visits/'
url3 = 'http://www.immigratemanitoba.com/how-to-immigrate/mpnp-resources/'

urls = [url1, url2, url3]


def get_page_as_string(url):
    return urlopen(url).read().strip()


from comparing import Comparator
from diffdb import HtmlDAO

dao = HtmlDAO(database)
comparator = Comparator(database)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(5)




