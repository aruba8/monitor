from flask import request, redirect, jsonify, render_template, g, url_for, flash
from bson.objectid import ObjectId
from app import app, db, lm
from forms import LoginForm, SignUpForm
from flask_login import login_user, logout_user, current_user, login_required
from datetime import datetime

from utils.logerconf import Logger


logger = Logger()
log = logger.get_logger()

from workers.comparing import Comparator
from workers.session import Sessions
from db.diffdb import HtmlDAO
from workers.admin import Admin

html_dao = HtmlDAO()
sessions = Sessions()
from models import User


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()


@app.route('/')
@app.route('/index')
def index():
    is_authenticated = g.user.is_authenticated()
    results = get_all_results()
    change_results = get_all_changed_results()
    return render_template('index.html', results=results, change_results=change_results,
                           is_authenticated=is_authenticated)


@app.route('/diff', methods=['GET'])
def diffs():
    f_param = request.args['f']
    s_param = request.args['s']
    old, new = html_dao.get_html_by_ids(f_param, s_param)
    result = Comparator.show_diff(old['html'], new['html'])
    return render_template('diffc.html', result=result)


@app.route('/diffc', methods=['GET'])
def diffs_c():
    f_param = request.args['f']
    s_param = request.args['s']
    old, new = html_dao.get_html_by_ids(f_param, s_param)
    result = Comparator.show_diff(old['div'], new['div'])
    return render_template('diffc.html', result=result)


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
    return render_template('p.html', results=results, ut=url_type, url=url, short_url=url[32:], p=page)


@app.route('/cp', methods=['GET'])
def all_changes():
    args = request.args
    page = 0
    if 'p' in args:
        page = int(args['p'])
    if page < 0:
        page = 0
    results = get_changed_results(page)

    return render_template('cp.html', results=results, p=page)


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin_page():
    admin_worker = Admin()
    if request.method == 'GET':
        urls = admin_worker.get_all_active_urls()
        hosts = admin_worker.get_active_hosts()
        hosts = {"count": hosts.count(), "hosts": hosts}
        return render_template('admin/admin.html', urls=urls, hosts=hosts)
    elif request.method == 'POST':
        url_id = request.form.get('url_to_delete')
        if url_id is not None:
            admin_worker.remove_url(url_id)
            return redirect('/admin')
        url = request.form['url']
        host = request.form['host_id']
        if url is None or url == '':
            return redirect('/admin')
        admin_worker.add_url(url, host)
        return redirect('/admin')


@app.route('/hosts', methods=['GET', 'POST'])
@login_required
def admin_hosts():
    admin_worker = Admin()
    if request.method == 'GET':
        xpaths = admin_worker.get_xpaths()
        return render_template('admin/hosts.html', xpaths=xpaths)
    elif request.method == 'POST':
        host = request.form.get('host')
        xpath = request.form.get('xpath')
        host_id_to_delete = request.form.get('host_to_delete')
        host_id = request.form.get('getHostId')
        edit = request.form.get("edit")
        if edit is not None:
            host_id_to_edit = request.form.get("edit")
            host_to_edit = request.form.get("host-to-edit")
            xpath_to_edit = request.form.get("xpath-to-edit")
            admin_worker.edit_host(host_id_to_edit, host_to_edit, xpath_to_edit)

        if host_id is not None:
            host_to_edit = admin_worker.get_host_by_id(host_id)

            if host_to_edit.count() == 1:
                return jsonify(xpath=host_to_edit[0]['xpath'], host=host_to_edit[0]['host'])

        if host_id_to_delete is not None:
            admin_worker.remove_host(host_id_to_delete)
            return redirect(url_for('admin_hosts'))

        if host == '' or host is None or xpath == '' or xpath is None:
            return redirect(url_for('admin_hosts'))
        else:
            admin_worker.add_xpath(host, xpath)
            return redirect(url_for('admin_hosts'))


@lm.user_loader
def user_loader(login):
    return User.objects(username=login).first()


@app.route('/login', methods=['GET', 'POST'])
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(username=form.login.data).first()
        if sessions.validate_login(form.login.data, form.password.data, {}):
            sessions.start_session(form.login.data)
            login_user(user)
            flash("Logged in successfully.")
            return redirect(request.args.get('next') or url_for('index'))

    return render_template('login.html', form=form)


@app.route('/logout', methods=['GET'])
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/signup', methods=['GET', 'POST'])
def signup_page():
    form = SignUpForm()
    if request.method == 'GET':
        return render_template('signup.html', form=form)
    if request.method == 'POST' and form.validate() and sessions.validate_new_user(form.login.data, form.password.data,
                                                                                   form.confirm.data, form.secret.data):
        if sessions.new_user(form.login.data, form.password.data):
            user = User.objects(username=form.login.data).first()
            login_user(user)
            return redirect(url_for('index'))
        else:
            return redirect(url_for('signup_page'))
    else:
        return redirect(url_for('signup_page'))


def get_all_results():
    results = []
    for item in html_dao.get_all_active_results():
        url = html_dao.get_url_by_url_type(item['urlType'])['url']
        item.set_url(url)
        results.append(item)
    return results


def get_all_changed_results():
    results = []
    for item in html_dao.get_all_not_identical():
        url = html_dao.get_url_by_url_type(item['urlType'])['url']
        item.set_url(url)
        results.append(item)
    return results


def get_changed_results(pages_to_skip):
    results = []
    for i in html_dao.get_all_changed_skip(pages_to_skip):
        item = i
        item['url'] = html_dao.get_url_by_url_type(i['urlType'])['url']
        results.append(item)
    return results