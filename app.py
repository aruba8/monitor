from flask import Flask, request
from jinja2 import Environment, PackageLoader


app = Flask(__name__)

env = Environment(loader=PackageLoader('app', 'templates'))
template_home = env.get_template('home.html')
template_diff = env.get_template('diff.html')
template_diff_c = env.get_template('diffc.html')
template_paging = env.get_template('p.html')

from pymongo import MongoClient
from comparing import Comparator


client = MongoClient('mongodb://localhost')
db = client.diffs
from diffdb import HtmlDAO

html_dao = HtmlDAO(db)


@app.route('/')
def home_1():
    results1 = html_dao.get_results_skip(1, 1, 0)
    results2 = html_dao.get_results_skip(2, 1, 0)
    results3 = html_dao.get_results_skip(3, 1, 0)
    results4 = html_dao.get_all_not_identical()
    return template_home.render(results1=results1, results2=results2, results3=results3, results4=results4)


@app.route('/diff', methods=['GET'])
def diffs():
    f_param = request.args['f']
    s_param = request.args['s']
    old, new = html_dao.get_html_by_ids(f_param, s_param)
    result = Comparator.show_diff(old['html'], new['html'])
    return template_diff.render(result=result)


@app.route('/diffc', methods=['GET'])
def diffs_c():
    f_param = request.args['f']
    s_param = request.args['s']
    old, new = html_dao.get_html_by_ids(f_param, s_param)
    result = Comparator.show_diff(old['div'], new['div'])
    return template_diff_c.render(result=result)


@app.route('/p', methods=['GET'])
def paging_table():
    args = request.args
    url_type = int(args['ut'])
    page = 0
    if 'p' in args:
        page = int(args['p'])
    if page < 0:
        page = 0

    results = html_dao.get_results_skip(url_type, 10, page)
    url = html_dao.get_url_by_url_type(url_type)
    return template_paging.render(results=results, ut=url_type, url=url, short_url=url[32:], p=page)


if __name__ == '__main__':
    #start server
    app.debug = True
    app.run()