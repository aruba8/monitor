from flask import Flask, request
from jinja2 import Environment, PackageLoader


app = Flask(__name__)

env = Environment(loader=PackageLoader('app', 'templates'))
template_home = env.get_template('home.html')
template_diff = env.get_template('diff.html')
template_diff_c = env.get_template('diffc.html')
template_redirect = env.get_template('redirect.html')

from pymongo import MongoClient
from comparing import Comparator


client = MongoClient('mongodb://localhost')
db = client.diffs
from diffdb import HtmlDAO

html_dao = HtmlDAO(db)


@app.route('/')
def home_1():
    results1 = html_dao.get_results(1)
    results2 = html_dao.get_results(2)
    results3 = html_dao.get_results(3)
    return template_home.render(results1=results1, results2=results2, results3=results3)


@app.route('/diff', methods=['GET'])
def diffs():
    f_param = request.args['f']
    s_param = request.args['s']
    comparator = Comparator(db)
    old, new = html_dao.get_html_by_ids(f_param, s_param)
    result = comparator.show_diff(old['html'], new['html'])
    return template_diff.render(result=result)


@app.route('/diffc', methods=['GET'])
def diffs_c():
    f_param = request.args['f']
    s_param = request.args['s']
    comparator = Comparator(db)
    old, new = html_dao.get_html_by_ids(f_param, s_param)
    result = comparator.show_diff(old['div'], new['div'])
    return template_diff_c.render(result=result)


if __name__ == '__main__':
    app.debug = True
    app.run()