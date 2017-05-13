from flask import (
        render_template,
        request,
        redirect,
        flash,
        url_for,
        )
import json
import urllib.request
# import os
# from flask_sqlalchemy import SQLAlchemy
# from flask_redis import FlaskRedis

from .auth import _is_account_valid
from . import app, redis_store


# get qiita article
with urllib.request.urlopen("https://qiita.com/api/v2/items") as res:
    json_articles = res.read().decode("utf-8")
    dict_articles = json.loads(json_articles)


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
    return render_template('show_all_articles.html',
                           articles=articles,
                           user=redis_store.get('username').decode("utf-8"))


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
                           articles_user_id=articles_user_id,
                           user=redis_store.get('username').decode("utf-8"))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if _is_account_valid(request.form):
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


@app.errorhandler(404)
def not_found(e):
    return "Not found!!"
