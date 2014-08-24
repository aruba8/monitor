__author__ = 'erik'

from lxml.html.diff import htmldiff

from db.diffdb import HtmlDAO
from utils.logerconf import Logger

logger = Logger()
log = logger.get_logger()


class Comparator:
    def __init__(self):
        self.html_dao = HtmlDAO()

    @staticmethod
    def show_diff(old_diff, new_diff):
        return htmldiff(old_diff, new_diff)

    def compare(self, url_type):
        docs_to_compare = self.html_dao.get_unchecked_by_type(url_type)
        log.info("Started comparison. Docs to compare : " + str(docs_to_compare.count()))
        for doc in docs_to_compare:
            prev_doc = self.html_dao.get_next_lower_entry(doc['id'])
            if prev_doc is None:
                self.html_dao.set_as_checked(doc['id'])
                continue

            d_content = doc['div']
            pd_content = prev_doc['div']

            if d_content.strip() == pd_content.strip():
                self.html_dao.insert_result(1, doc['id'], prev_doc['id'], url_type)
            else:
                self.html_dao.insert_result(0, doc['id'], prev_doc['id'], url_type)

            self.html_dao.set_as_checked(doc['id'])

    def check(self, url_type):
        pres = self.html_dao.get_results(url_type)
        url = self.html_dao.get_url_by_url_type(url_type)['url']
        if pres.count() == 0:
            log.info("Comparing finished")
            return
        result = pres[0]
        from workers.emailworker import Emailer

        e = Emailer()
        if result['areIdentical'] == 0:
            compared_objs = result['compared_objs']
            old, new = self.html_dao.get_html_by_ids(compared_objs[0], compared_objs[1])
            body = self.show_diff(old['div'], new['div'])
            message = e.init_msg('Attention!!', body, url)
            e.send_email(message)
            log.info("Comparing finished")
