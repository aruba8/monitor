import os

from flask import Flask, request, redirect, session
from jinja2 import Environment, PackageLoader
from bson.objectid import ObjectId

from utils.logerconf import Logger


logger = Logger()
log = logger.get_logger()

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
template_all_changed = env.get_template('cp.html')
template_admin_hosts_page = env.get_template('hosts.html')

from pymongo import MongoClient
from workers.comparing import Comparator
from workers.session import Sessions
from db.diffdb import HtmlDAO
from utils.configparser import Parser
from workers.admin import Admin

client = MongoClient('mongodb://localhost')
db = client.diffs
html_dao = HtmlDAO(db)
config = Parser()


@app.route('/')
def home_1():
    results = get_all_results()
    change_results = get_all_changed_results()
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
    url_type = args['ut']
    page = 0
    if 'p' in args:
        page = int(args['p'])
    if page < 0:
        page = 0

    results = html_dao.get_results_skip(url_type, 10, page)
    url = html_dao.get_url_by_url_type(ObjectId(url_type))['url']
    return template_paging.render(results=results, ut=url_type, url=url, short_url=url[32:], p=page)


@app.route('/cp', methods=['GET'])
def all_changes():
    args = request.args
    page = 0
    if 'p' in args:
        page = int(args['p'])
    if page < 0:
        page = 0
    results = get_changed_results(page)

    return template_all_changed.render(results=results, p=page)


@app.route('/admin', methods=['GET', 'POST'])
def admin_page():
    if 'username' not in session:
        return redirect('/login')
    admin_worker = Admin(db)
    username_cookies = session['username']
    sessions_worker = Sessions(db)
    username = sessions_worker.login_check(username_cookies)
    if username is None:
        return redirect('/login')

    if request.method == 'GET':
        urls = admin_worker.get_all_active_urls()
        return template_admin_page.render(urls=urls)
    elif request.method == 'POST':
        url_id = request.form.get('url_to_delete')
        if url_id is not None:
            admin_worker.remove_url(url_id)
        url = request.form['url']
        if url is None or url == '':
            return redirect('/admin')
        admin_worker.add_url(url)
        return redirect('/admin')

@app.route('/admin/hosts', methods=['GET', 'POST'])
def admin_hosts():
    if 'username' not in session:
        return redirect('/login')
    admin_worker = Admin(db)
    username_cookies = session['username']
    sessions_worker = Sessions(db)
    username = sessions_worker.login_check(username_cookies)

    if username is None:
        return redirect('/login?r')

    if request.method == 'GET':
        xpaths = admin_worker.get_xpaths();
        return template_admin_hosts_page.render(xpaths=xpaths)
    elif request.method == 'POST':
        host = request.form['host']
        xpath = request.form['xpath']
        admin_worker.add_xpath(host, xpath)
        return redirect('/admin/hosts')
        pass


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
            if session_id == -1:
                return redirect('/internal_error')

            cookie = sessions.make_secure_val(session_id)
            session['username'] = cookie
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
    for i in html_dao.get_all_active_results():
        item = i
        item['url'] = html_dao.get_url_by_url_type(i['urlType'])['url']
        results.append(item)
    return results


def get_all_changed_results():
    results = []
    for i in html_dao.get_all_not_identical():
        item = i
        item['url'] = html_dao.get_url_by_url_type(i['urlType'])['url']
        results.append(item)
    return results


def get_changed_results(pages_to_skip):
    results = []
    for i in html_dao.get_all_changed_skip(pages_to_skip):
        item = i
        item['url'] = html_dao.get_url_by_url_type(i['urlType'])['url']
        results.append(item)
    return results


if __name__ == '__main__':
    #start server
    app.debug = True
    app.run()