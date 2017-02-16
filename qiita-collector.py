from flask import Flask, render_template, request
import urllib.request
import json

app = Flask(__name__)
app.config.from_object(__name__)
articles = []  # empty list


# get qiita article
with urllib.request.urlopen("https://qiita.com/api/v2/items") as res:
    json_articles = res.read().decode("utf-8")
    dict_articles = json.loads(json_articles)


@app.route('/')
def get_articles():
    articles = [dict(title=article["title"],
                     user_id=article["user"]["id"],
                     user_image=article["user"]["profile_image_url"],
                     url=article["url"]
                     ) for article in dict_articles]
    print(articles)
    return render_template('show_articles.html', articles=articles)


@app.route('/', methods=['POST'])
def get_word_articles():
    query = request.form['query']
    print(articles)
    for article in dict_articles:
        if query in article["title"]:
            hit_article = dict(title=article["title"],
                               user_id=article["user"]["id"],
                               user_image=article["user"]["profile_image_url"],
                               url=article["url"])
            print("hit_article : ")
            print(hit_article)
            articles.append(hit_article)

    print(articles)
    return render_template('show_articles.html', articles=articles)


if __name__ == '__main__':
    app.run(debug=True)
