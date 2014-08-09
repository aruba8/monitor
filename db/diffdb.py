__author__ = 'erik'

import sys
from datetime import datetime

from bson.objectid import ObjectId
from lxml import html

from utils.logerconf import Logger
from workers.models import Htmls, Results, Urls, Xpath

logger = Logger()
log = logger.get_logger()


class HtmlDAO:
    def get_html_by_ids(self, old, new):
        return Htmls.objects.get(id=ObjectId(old)), Htmls.objects.get(id=ObjectId(new))

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
        try:
            html = Htmls(html=html_string, datetime=dt, urlType=url_id, checked=0,
                         date=dt.strftime("%d.%m.%Y"), time=dt.strftime("%X"), url=url, div=div)
            html.save()
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
        return Results.objects(areIdentical=0).order_by('-datetime')[:10]

    def get_two_last_entries(self, url_type):
        return Htmls.objects(urlType=url_type).order_by('-datetime')[:2]

    def get_unchecked_by_type(self, url_type):
        return Htmls.objects(urlType=url_type, checked=0).order_by('+datetime')

    def set_as_checked(self, object_id):
        Htmls.objects(id=object_id).update_one(set__checked=1)

    def get_next_lower_entry(self, object_id):
        cur_entry = Htmls.objects.get(id=ObjectId(object_id))

        result_set = Htmls.objects(datetime__lt=cur_entry['datetime'], urlType=cur_entry['urlType']).order_by(
            '-datetime')[:1]

        if result_set.count() == 0:
            return None
        else:
            return result_set[0]

    def insert_result(self, are_identical, obj_id1, obj_id2, url_type):
        dt = datetime.now()
        Results(areIdentical=are_identical, compared_objs=[obj_id1, obj_id2], date=dt.strftime("%d.%m.%Y"),
                time=dt.strftime("%X"), datetime=dt, urlType=url_type).save()

    def get_results(self, url_type):
        query = {'urlType': url_type}
        return Results.objects(urlType=url_type).order_by('-datetime')[:10]

    def get_results_skip(self, url_type, limit_number, number_to_skip):
        if url_type is not ObjectId:
            url_type = ObjectId(url_type)
        return Results.objects(urlType=url_type).order_by('-datetime').limit(limit_number).skip(number_to_skip)

    def get_url_by_url_type(self, url_type):
        if url_type is not ObjectId:
            url_type = ObjectId(url_type)

        return Urls.objects.get(id=url_type)

    def get_all_active_results(self):
        from workers.admin import Admin

        admin_worker = Admin()
        url_list = admin_worker.get_all_active_url_ids()
        return Results.objects(urlType__in=url_list).order_by('-datetime').limit(len(url_list))

    def get_all_changed_skip(self, number_to_skip):
        return Results.objects(areIdentical=0).order_by('-datetime').limit(10).skip(number_to_skip)

    def get_xpath_by_url_id(self, url_id):
        host_id = Urls.objects.get(id=ObjectId(url_id))
        return Xpath.objects.get(id=host_id['host_id'])['xpath']