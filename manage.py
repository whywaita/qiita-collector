# -*- coding: utf-8 -*-
from flask import (
        Flask,
        render_template,
        request,
        url_for,
        redirect,
        flash
        )
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_redis import FlaskRedis

import urllib.request
import json
import os

import auth

from models import User, db
from sqlalchemy_utils import database_exists, create_database

"""Initialize
- app
- load config
- get all article
- connect mysql
"""

SQLALCHEMY_TRACK_MODIFICATIONS = True

app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'secret_key'

# set config
app.config.from_pyfile('config_file.cfg')
app.config['SQLALCHEMY_DATABASE_URI'] = \
    'mysql+pymysql://' + \
    os.getenv('QC_MYSQL_USER', app.config['MYSQL_USER']) + \
    ':' + os.getenv('QC_MYSQL_PASS', app.config['MYSQL_PASS']) + \
    '@' + os.getenv('QC_MYSQL_SERVER', app.config['MYSQL_SERVER']) + \
    '/' + os.getenv('QC_MYSQL_DBNAME', app.config['MYSQL_DB_NAME'])
app.config['SQLALCHEMY_NATIVE_UNICODE'] = app.config['MYSQL_CHAR']

# instance init
db.init_app(app)
db.app = app

# redis
if os.getenv('QC_REDIS_URL') is not None:
    # if set QC_REDIS_URL, overwrite REDIS URL
    app.config['REDIS_URL'] = os.getenv('QC_REDIS_URL')
redis_store = FlaskRedis(app)

# commands
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)
manager.add_command('runserver')

# get qiita article
with urllib.request.urlopen("https://qiita.com/api/v2/items") as res:
    json_articles = res.read().decode("utf-8")
    dict_articles = json.loads(json_articles)

# migrate (tmp)
if not database_exists(app.config['SQLALCHEMY_DATABASE_URI']):
    create_database(app.config['SQLALCHEMY_DATABASE_URI'])
db.create_all()
if len(User.query.filter(User.name == 'admin').all()) == 0:
    admin = User('admin', 'password')
    db.session.add(admin)
    db.session.commit()


@app.before_request
def before_request():
    # already login
    if redis_store.get('username') is not None:
        return
    # login page
    if request.path == '/login':
        return
    # staticファイルはリダイレクトしないように
    if request.path.count('/static'):
        return
    # user need login
    return redirect('/login')


@app.route('/')
def get_articles():
    """Get All Qiita Article
    """
    articles = [dict(title=article["title"],
                     user_id=article["user"]["id"],
                     user_image=article["user"]["profile_image_url"],
                     url=article["url"]
                     ) for article in dict_articles]
    return render_template('show_all_articles.html', articles=articles)


@app.route('/', methods=['POST'])
def get_word_articles():
    """Search Article
    """
    articles_title = []  # empty list
    articles_user_id = []  # empty list
    # Get form Info
    query = request.form['query']

    for article in dict_articles:
        hit_article = dict(title=article["title"],
                           user_id=article["user"]["id"],
                           user_image=article["user"]["profile_image_url"],
                           url=article["url"])
        if query in article["title"]:
            articles_title.append(hit_article)
        if query in article["user"]["id"]:
            articles_user_id.append(hit_article)

    return render_template('result.html',
                           articles_title=articles_title,
                           articles_user_id=articles_user_id)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if auth._is_account_valid(request.form):
            # registration to session
            redis_store.set('username', request.form['username'])
            return redirect('/')

        # if invaild account name
        flash('invaild login name!', 'error')
        return render_template('login.html')

    return render_template('login.html')


@app.route('/logout', methods=['GET'])
def logout():
    redis_store.set('username', '')
    return redirect(url_for('login'))


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run("0.0.0.0", port, debug=True)
