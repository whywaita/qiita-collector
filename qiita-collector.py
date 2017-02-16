from flask import Flask, render_template
import urllib.request
import json

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

# get qiita article
with urllib.request.urlopen("https://qiita.com/api/v2/items") as res:
    json_articles = res.read().decode("utf-8")
    dict_articles = json.loads(json_articles)
    articles = [dict(title=article["title"], user_id=article["user"]["id"], user_image=article["user"]["profile_image_url"], url=article["url"]) for article in dict_articles]


@app.route('/')
def get_articles():
    # print(dict_articles["title"][0])
    return render_template('show_articles.html', articles=articles)


if __name__ == '__main__':
    app.run()
