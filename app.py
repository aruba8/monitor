import os

from flask import Flask, request, redirect, session
from jinja2 import Environment, PackageLoader


app = Flask(__name__)
app.secret_key = os.urandom(24)

env = Environment(loader=PackageLoader('app', 'templates'))
template_home = env.get_template('home.html')
template_diff = env.get_template('diff.html')
template_diff_c = env.get_template('diffc.html')
template_paging = env.get_template('p.html')
template_admin_page = env.get_template('admin.html')
template_login = env.get_template('login.html')
template_signup = env.get_template('signup.html')

from pymongo import MongoClient
from workers.comparing import Comparator
from workers.session import Sessions
from db.diffdb import HtmlDAO
from utils.configparser import Parser

client = MongoClient('mongodb://localhost')
db = client.diffs
html_dao = HtmlDAO(db)

config = Parser()


@app.route('/')
def home_1():
    results = get_all_results()
    change_results = html_dao.get_all_not_identical()
    return template_home.render(results=results, change_results=change_results)


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


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if 'username' not in session:
        return redirect('/login')
    username_cookies = session['username']
    print(username_cookies)
    sessions = Sessions(db)
    username = sessions.login_check(username_cookies)
    if username is None:
        return redirect('/login')

    return template_admin_page.render()


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    sessions = Sessions(db)

    if request.method == 'GET':
        return template_login.render()
    else:
        username = request.form['username']
        password = request.form['password']
        user_record = {}
        validation = sessions.validate_login(username, password, user_record)
        if validation:
            session_id = sessions.start_session(username)
            print(session_id)
            if session_id == -1:
                return redirect('/internal_error')

            cookie = sessions.make_secure_val(session_id)
            session['username'] = cookie
            print(cookie)
            return redirect('/admin')
        else:
            return template_login.render(error='User not in database')


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    if request.method == 'GET':
        return template_signup.render()
    if request.method == 'POST':
        sessions = Sessions(db)
        username = request.form['username']
        password = request.form['password']
        password2 = request.form['password2']
        secret_word = request.form['verify']
        if sessions.validate_new_user(username, password, password2, secret_word):
            if sessions.new_user(username, password):
                session_id = sessions.start_session(username)
                cookie = sessions.make_secure_val(session_id)
                session['username'] = cookie
                return redirect('/admin')
            else:
                return redirect('/signup')
        else:
            return template_signup.render()


def get_all_results():
    results = []
    for i in range(len(config.get_urls_as_list())):
        item = html_dao.get_results_skip(i + 1, 1, 0)[0]
        item['url'] = html_dao.get_url_by_url_type(i + 1)
        results.append(item)
    return results


if __name__ == '__main__':
    #start server
    app.debug = True
    app.run()