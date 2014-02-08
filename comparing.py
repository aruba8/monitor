__author__ = 'erik'

from diffdb import HtmlDAO

from lxml import html
from lxml.html.diff import htmldiff


class Comparator:
    def __init__(self, database_diffs):
        self.html_dao = HtmlDAO(database_diffs)

    def show_diff(self, old_diff, new_diff):
        return htmldiff(old_diff, new_diff)


    def compare(self, url_type):
        docs_to_compare = self.html_dao.get_unchecked_by_type(url_type)
        print "Started comparison. Docs to compare : ", docs_to_compare.count()
        for doc in docs_to_compare:
            prev_doc = self.html_dao.get_next_lower_entry(doc['_id'])
            if prev_doc == None:
                self.html_dao.set_as_checked(doc['_id'])
                continue

            d_content = doc['div']
            pd_content = prev_doc['div']

            if d_content.strip() == pd_content.strip():
                self.html_dao.insert_result(1, doc['_id'], prev_doc['_id'], url_type)
            else:
                self.html_dao.insert_result(0, doc['_id'], prev_doc['_id'], url_type)

            self.html_dao.set_as_checked(doc['_id'])

    def get_div_content(self, html_string):
        html_string = html.document_fromstring(html_string)
        elem = html_string.xpath('//div[@id="content"]')
        return elem[0].text_content().strip()

    def check(self, url_type):
        result = self.html_dao.get_results(url_type)[0]
        from emailworker import Emailer

        e = Emailer()
        if result['areIdentical'] == 0:
            text = '''
            Some changes are realized!!
            http://mmcp.zapto.org/
            '''
            message = e.init_msg('Attention!!', text)
            e.send_email(message)


if __name__ == '__main__':
    from pymongo import MongoClient

    client = MongoClient('mongodb://localhost')
    hdb = client.diffs
    html_dao = HtmlDAO(hdb)
    cp = Comparator(hdb)
    cp.check(3)
