import feedparser

from flask import Flask
from flask import render_template

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml', 'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest', 'abc': 'http://www.abc.net.au/local/rss/hobart/news.xml'}

app = Flask(__name__)

@app.route("/")
@app.route("/<publication>")
def get_news(publication="bbc"):
    try:
        feed = feedparser.parse(RSS_FEEDS[publication])
        first_article = feed['entries'][0]
        return render_template("home.html",title=first_article.get("title"), published=first_article.get("published"), summary=first_article.get("summary"), header=publication.upper())
        # return """<html>
        # <body>
        #     <h1>{3} Headlines</h1>
        #     <b>{0}</b> <br>
        #     <i>{1}</i> <br>
        #     <p>{2}</p>
        # </body>
        # </html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"),
        #                   publication.upper())
    except:
        return "no news is good news - try /bbc, /cnn, /fox or /abc for the bad"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
