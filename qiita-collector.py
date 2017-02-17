# -*- coding: utf-8 -*-
from flask import Flask, render_template, request
import urllib.request
import json

app = Flask(__name__)
app.config.from_object(__name__)


# get qiita article
with urllib.request.urlopen("https://qiita.com/api/v2/items") as res:
    json_articles = res.read().decode("utf-8")
    dict_articles = json.loads(json_articles)


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

    return render_template('search_result.html',
                           articles_title=articles_title,
                           articles_user_id=articles_user_id)


if __name__ == '__main__':
    app.run(debug=True)
