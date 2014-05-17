__author__ = 'erik'

from lxml.html.diff import htmldiff

from db.diffdb import HtmlDAO
from utils.logerconf import Logger

logger = Logger()
log = logger.get_logger()


class Comparator:
    def __init__(self, database_diffs):
        self.html_dao = HtmlDAO(database_diffs)

    @staticmethod
    def show_diff(old_diff, new_diff):
        return htmldiff(old_diff, new_diff)

    def compare(self, url_type):
        docs_to_compare = self.html_dao.get_unchecked_by_type(url_type)
        log.info("Started comparison. Docs to compare : " + str(docs_to_compare.count()))
        for doc in docs_to_compare:
            prev_doc = self.html_dao.get_next_lower_entry(doc['_id'])
            if prev_doc is None:
                self.html_dao.set_as_checked(doc['_id'])
                continue

            d_content = doc['div']
            pd_content = prev_doc['div']

            if d_content.strip() == pd_content.strip():
                self.html_dao.insert_result(1, doc['_id'], prev_doc['_id'], url_type)
            else:
                self.html_dao.insert_result(0, doc['_id'], prev_doc['_id'], url_type)

            self.html_dao.set_as_checked(doc['_id'])

    def check(self, url_type):
        pres = self.html_dao.get_results(url_type)
        if pres.count() == 0:
            return
        result = pres[0]
        from workers.emailworker import Emailer

        e = Emailer()
        if result['areIdentical'] == 0:
            text = '''
            Some changes are realized!!
            http://mmcp.zapto.org/
            '''
            message = e.init_msg('Attention!!', text)
            e.send_email(message)