# -*- coding: utf-8 -*-
from flask import Flask, render_template, request, url_for, redirect, session
import urllib.request
import json
import toml

from models import db

"""Initialize
- app
- load config
- get all article
- connect mysql
"""

# load config
with open("config.toml") as configfile:
    config = toml.loads(configfile.read())


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'secret_key'

# DB
app.config['SQLALCHEMY_DATABASE_URI'] = \
        'mysql+pymysql://' + \
        config["mysql"]["user"] + ':' + config["mysql"]["password"] + \
        '@' + config["mysql"]["server"] + \
        '/' + config["mysql"]["db_name"]
app.config['SQLALCHEMY_NATIVE_UNICODE'] = config["mysql"]["charset"]

db.init_app(app)
db.app = app
migrate = db.Migrate(app, db)
manager = db.Manager(app)
manager.add_command('db', db.MigrateCommand)
manager.add_command('runserver')

# get qiita article
with urllib.request.urlopen("https://qiita.com/api/v2/items") as res:
    json_articles = res.read().decode("utf-8")
    dict_articles = json.loads(json_articles)


@app.before_request
def before_request():
    # already login
    if session.get('username') is not None:
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
    if request.method == 'POST' and _is_account_valid():
            # registration to session
            session['username'] = request.form['username']
            return redirect('/')
    return render_template('login.html')


def _is_account_valid():
    if request.form.get('username') is None:
        return False
    return True


@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
