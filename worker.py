#!/usr/bin/python

__author__ = 'erik'

from urllib2 import urlopen, URLError
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
    print(str(datetime.now()) + ' Job ended')


schedule.every(1).hours.do(do_job)

connection_string = "mongodb://localhost"
connection = MongoClient(connection_string)
database = connection.diffs

url1 = 'http://www.immigratemanitoba.com/how-to-immigrate/apply/recruitment-missions/'
url2 = 'http://www.immigratemanitoba.com/how-to-immigrate/apply/exploratory-visits/'
url3 = 'http://www.immigratemanitoba.com/how-to-immigrate/mpnp-resources/'

urls = [url1, url2, url3]


def get_page_as_string(url):
    try:
        return urlopen(url).read().strip()
    except URLError:
        print(str(datetime.now()) + ' could not open page : ' + url)
        return "could not open page"


from comparing import Comparator
from diffdb import HtmlDAO

dao = HtmlDAO(database)
comparator = Comparator(database)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(5)




