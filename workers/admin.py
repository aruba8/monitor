from bson.objectid import ObjectId

__author__ = 'erik'

import sys

from datetime import datetime
from utils.logerconf import Logger

logger = Logger()
log = logger.get_logger()


class Admin:
    def __init__(self, diffs_db):
        self.urls = diffs_db.urls

    def add_url(self, url):
        from utils.urlutil import prepare_url

        purl = prepare_url(url)
        query = {'url': purl['url'],
                 'host': purl['host'],
                 'path': purl['path'],
                 'datetime': datetime.now(),
                 'active': 1}
        try:
            self.urls.insert(query)
        except:
            log.error('Error inserting url' + sys.exc_info()[0])

    def get_all_active_urls(self):
        query = {'active': 1}
        return self.urls.find(query)

    def remove_url(self, url_id):
        query = {'_id': ObjectId(url_id)}
        upd_query = {'$set': {'active': 0}}
        self.urls.update(query, upd_query)

    def get_all_active_url_ids(self):
        query = {'active': 1}
        show_query = {'_id': True}
        urls = self.urls.find(query, show_query)
        urls_list = []
        for url in urls:
            urls_list.append(url['_id'])
        return urls_list