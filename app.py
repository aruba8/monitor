from flask import Flask, request
from jinja2 import Environment, PackageLoader


app = Flask(__name__)

env = Environment(loader=PackageLoader('app', 'templates'))
template_home = env.get_template('home.html')
template_diff = env.get_template('diff.html')

from pymongo import MongoClient


client = MongoClient('mongodb://localhost')
db = client.diffs
from diffdb import HtmlDAO

html_dao = HtmlDAO(db)


@app.route('/')
def home():
    results = html_dao.get_results(1)
    return template_home.render(results=results)


@app.route('/diff', methods=['GET'])
def diffs():
    f_param = request.args['f']
    s_param = request.args['s']
    return template_diff.render(s=s_param, f=f_param)


if __name__ == '__main__':
    app.debug = True
    app.run()