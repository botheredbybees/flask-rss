import feedparser

from flask import Flask
from flask import render_template
from flask import request

import urllib.parse

RSS_FEEDS = {'Best of abc.net.au': 'http://abc.net.au/bestof/bestofabc.xml', 'Radio Australia: Asia Pacific': 'http://abc.net.au/ra/rss/asiapacific.rss',
             'ABC iView Programs': 'http://tvmp.abc.net.au/iview/rss/category/abc1.xml', 'ABC Hobart': 'http://www.abc.net.au/local/rss/hobart/news.xml'}
app = Flask(__name__)


@app.route("/")
@app.route("/<publication>")
def get_news():
    try:
        query = urllib.parse.unquote_plus(request.args.get("publication"))
        if not query or query not in RSS_FEEDS:
            query = "ABC Hobart"
        feed = feedparser.parse(RSS_FEEDS[query])
        return render_template("home.html", articles=feed['entries'], header=query, rssFeeds= RSS_FEEDS)
    except:
        return "no news is good news"


if __name__ == '__main__':
    app.run(port=5000, debug=True)
