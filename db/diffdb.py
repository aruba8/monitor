__author__ = 'erik'

import sys
from datetime import datetime

from bson.objectid import ObjectId
from lxml import html

from utils.logerconf import Logger

logger = Logger()
log = logger.get_logger()


class HtmlDAO:
    def __init__(self, database_diffs):
        self.htmls = database_diffs.htmls
        self.results = database_diffs.results
        self.database_diffs = database_diffs
        self.urls = database_diffs.urls
        self.xpath = database_diffs.xpath

    def get_html_by_ids(self, old, new):
        return self.htmls.find_one({'_id': ObjectId(old)}), self.htmls.find_one({'_id': ObjectId(new)})

    def insert_html(self, html_string, url, url_id):
        xpath = self.get_xpath_by_url_id(url_id)
        try:
            if xpath != '':
                div = self.get_div_content_by_xpath(html_string, xpath)
            else:
                div = self.get_div_content(html_string)
        except Exception as ex:
            log.error(ex.message)
            return

        if html_string == "could not open page":
            return
        dt = datetime.now()
        query = {'html': html_string,
                 'datetime': dt,
                 'urlType': url_id,
                 'checked': 0,
                 'date': dt.strftime("%d.%m.%Y"),
                 'time': dt.strftime("%X"),
                 'url': url,
                 'div': div}
        try:
            self.htmls.insert(query)
        except:
            log.error('Error inserting data' + sys.exc_info()[0])

    @staticmethod
    def get_div_content(html_string):
        htm = html.document_fromstring(html_string)
        xpath = '//div[@id="container"]'
        elem = htm.xpath(xpath)
        if len(elem) == 0:
            raise Exception("Couldn't find anything using this xpath: " + xpath)
        else:
            return elem[0].text_content().strip()

    @staticmethod
    def get_div_content_by_xpath(html_string, xpath):
        htm = html.document_fromstring(html_string)
        elem = htm.xpath(xpath)
        if len(elem) == 0:
            raise Exception("Couldn't find anything using this xpath: " + xpath)
        else:
            return elem[0].text_content().strip()

    def get_all_not_identical(self):
        query = {'areIdentical': 0}
        return self.results.find(query).sort('datetime', -1).limit(10)

    def get_two_last_entries(self, url_type):
        query = {'urlType': url_type}
        cursor = self.htmls.find(query).sort('datetime', -1).limit(2)
        return cursor

    def get_unchecked_by_type(self, url_type):
        query = {'urlType': url_type,
                 'checked': 0}
        return self.htmls.find(query).sort('datetime', 1)

    def set_as_checked(self, object_id):
        query = {'_id': ObjectId(object_id)}
        upd_query = {'$set': {'checked': 1}}
        self.htmls.update(query, upd_query)

    def get_next_lower_entry(self, object_id):
        query_current = {'_id': ObjectId(object_id)}
        cur_entry = self.htmls.find_one(query_current)
        query_next = {'datetime': {'$lt': cur_entry['datetime']}, 'urlType': cur_entry['urlType']}
        result_set = self.htmls.find(query_next).sort('datetime', -1).limit(1)
        if result_set.count() == 0:
            return None
        else:
            return result_set[0]

    def insert_result(self, are_identical, obj_id1, obj_id2, url_type):
        dt = datetime.now()
        query_to_insert = {'areIdentical': are_identical,
                           'compared_objs': [obj_id1, obj_id2],
                           'date': dt.strftime("%d.%m.%Y"),
                           'time': dt.strftime("%X"),
                           'datetime': dt,
                           'urlType': url_type}
        self.results.insert(query_to_insert)

    def get_results(self, url_type):
        query = {'urlType': url_type}
        return self.results.find(query).sort('datetime', -1).limit(10)

    def get_results_skip(self, url_type, limit_number, number_to_skip):
        if url_type is not ObjectId:
            url_type = ObjectId(url_type)
        query = {'urlType': url_type}
        return self.results.find(query).sort('datetime', -1).limit(limit_number).skip(number_to_skip)

    def get_url_by_url_type(self, url_type):
        if url_type is not ObjectId:
            url_type = ObjectId(url_type)

        query = {'_id': url_type}
        return self.urls.find_one(query)

    def get_all_active_results(self):
        from workers.admin import Admin

        admin_worker = Admin(self.database_diffs)
        url_list = admin_worker.get_all_active_url_ids()
        query = {'urlType': {'$in': url_list}}
        return self.results.find(query).sort('datetime', -1).limit(len(url_list))

    def get_all_changed_skip(self, number_to_skip):
        query = {'areIdentical': 0}
        return self.results.find(query).sort('datetime', -1).limit(10).skip(number_to_skip)

    def get_xpath_by_url_id(self, url_id):
        find_query = {'_id': ObjectId(url_id)}
        projection = {'host_id': True}
        host_id = self.urls.find_one(find_query, projection)
        return self.xpath.find_one({'_id': host_id['host_id']})['xpath']

