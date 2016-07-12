import feedparser

from flask import Flask
from flask import render_template
from flask import request

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml', 'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest', 'abc': 'http://www.abc.net.au/local/rss/hobart/news.xml'}

app = Flask(__name__)

@app.route("/",methods=['GET','POST'])
def get_news():
    try:
        query = request.form.get("publication")
        if not query or query.lower() not in RSS_FEEDS:
            publication = "abc"
        else:
            publication = query.lower()
        feed = feedparser.parse(RSS_FEEDS[publication])
        return render_template("home.html",articles=feed['entries'], header=publication.upper())
    except:
        return "no news is good news - try /bbc, /cnn, /fox or /abc for the bad"


if __name__ == '__main__':
    app.run(port=5001, debug=True)
