__author__ = 'erik'

import sys
from datetime import datetime

from bson.objectid import ObjectId
from lxml import html


class HtmlDAO:
    def __init__(self, database_diffs):
        self.htmls = database_diffs.htmls
        self.results = database_diffs.results

    def get_html_by_ids(self, old, new):
        query = {'_id': {'$in': [ObjectId(old), ObjectId(new)]}}
        return self.htmls.find_one({'_id': ObjectId(old)}), self.htmls.find_one({'_id': ObjectId(new)})

    def insert_html(self, html_string, url, url_type):
        query = {'html': html_string,
                 'datetime': datetime.now(),
                 'url': url,
                 'urlType': url_type,
                 'checked': 0,
                 'div': self.get_div_content(html_string)}
        try:
            self.htmls.insert(query)
        except:
            print "Error inserting post"
            print "Unexpected error:", sys.exc_info()[0]

    def get_div_content(self, html_string):
        htm = html.document_fromstring(html_string)
        elem = htm.xpath('//div[@id="content"]')
        return elem[0].text_content().strip()

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
        query_to_insert = {'areIdentical': are_identical,
                           'compared_objs': [obj_id1, obj_id2],
                           'datetime': datetime.now(),
                           'urlType': url_type}
        self.results.insert(query_to_insert)

    def get_results(self, url_type):
        query = {'urlType': url_type}
        return self.results.find(query).sort('datetime', -1).limit(10)

if __name__ == '__main__':
    from pymongo import MongoClient

    client = MongoClient('mongodb://localhost')
    hdb = client.diffs
    html_dao = HtmlDAO(hdb)
    print html_dao.get_next_lower_entry('52f5caa08e3c113528214b85')