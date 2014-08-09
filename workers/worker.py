__author__ = 'erik'

from urllib2 import urlopen, URLError
import time

import schedule

from utils.logerconf import Logger
from utils.configparser import Parser
from admin import Admin


config_parser = Parser()
logger = Logger()
log = logger.get_logger()

from workers.comparing import Comparator
from db.diffdb import HtmlDAO

dao = HtmlDAO()
comparator = Comparator()

admin_worker = Admin()


def do_job():
    log.info('Job started')
    urls = admin_worker.get_all_active_urls()
    for url in urls:
        id = url['id']
        dao.insert_html(get_page_as_string(url['url']), url['url'], id)
        comparator.compare(id)
        comparator.check(id)
    log.info('Job ended')

period = config_parser.get_period()
schedule.every(period).minutes.do(do_job)

def get_page_as_string(url):
    try:
        return urlopen(url).read().strip()
    except URLError:
        log.error(' could not open page : ' + url)
        return "could not open page"


def start():
    while True:
        schedule.run_pending()
        time.sleep(5)