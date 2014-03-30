__author__ = 'erik'

from urllib2 import urlopen, URLError
import time

from pymongo import MongoClient
import schedule

from utils.logerconf import Logger
from utils.configparser import Parser
from admin import Admin


config_parser = Parser()
logger = Logger()
log = logger.get_logger()

connection_string = "mongodb://localhost"
connection = MongoClient(connection_string)
database = connection.diffs

admin_worker = Admin(database)


def do_job():
    log.info('Job started')
    urls = admin_worker.get_all_active_urls()
    for url in urls:
        _id = url['_id']
        dao.insert_html(get_page_as_string(url['url']), url['url'], _id)
        comparator.compare(_id)
        comparator.check(_id)
    log.info('Job ended')

# schedule.every(1).minutes.do(do_job)
schedule.every(1).hours.do(do_job)


def get_page_as_string(url):
    try:
        return urlopen(url).read().strip()
    except URLError:
        log.error(' could not open page : ' + url)
        return "could not open page"


from workers.comparing import Comparator
from db.diffdb import HtmlDAO

dao = HtmlDAO(database)
comparator = Comparator(database)

if __name__ == '__main__':
    while True:
        schedule.run_pending()
        time.sleep(5)