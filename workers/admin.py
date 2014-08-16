from mongoengine import ValidationError

__author__ = 'erik'

import sys
from datetime import datetime

from bson.objectid import ObjectId

from utils.logerconf import Logger


logger = Logger()
log = logger.get_logger()
from workers.models import Urls, Xpath


class Admin:

    def add_url(self, url, host_id):
        from utils.urlutil import prepare_url

        host = self.get_host_by_id(host_id)[0]
        purl = prepare_url(url)
        try:
            Urls(url=purl['url'], host_id=ObjectId(host_id), host=host['host'], path=purl['path'],
                 datetime=datetime.now(), active=1).save()
        except ValidationError:
            log.error('Error inserting url')

    def remove_host(self, host_id_to_delete):
        Xpath.objects(id=ObjectId(host_id_to_delete)).update_one(set__active=0)
        Urls.objects(host_id=ObjectId(host_id_to_delete)).update_one(set__active=0)

    def get_host_by_id(self, host_id):
        return Xpath.objects(id=ObjectId(host_id))

    def get_all_active_urls(self):
        return Urls.objects(active=1)

    def remove_url(self, url_id):
        Urls.objects(id=ObjectId(url_id)).update_one(set__active=0)

    def get_all_active_url_ids(self):
        urls = self.get_all_active_urls()
        urls_list = []
        for url in urls:
            urls_list.append(url['id'])
        return urls_list

    def add_xpath(self, host, xpath):
        try:
            Xpath(host=host, xpath=xpath, added_datetime=datetime.now(), active=1).save()
        except:
            log.error('Error inserting xpath' + sys.exc_info()[0])

    def get_xpaths(self):
        return Xpath.objects(active=1)

    def get_active_hosts(self):
        return Xpath.objects(active=1)

    def edit_host(self, host_id, host, xpath):
        Xpath.objects(id=ObjectId(host_id)).update_one(set__host=host, set__xpath=xpath)