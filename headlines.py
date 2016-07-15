import feedparser

from flask import Flask
from flask import render_template
from flask import request
import json
import urllib
import urllib.request
import urllib.parse

RSS_FEEDS = {'Best of abc.net.au': 'http://abc.net.au/bestof/bestofabc.xml', 'Radio Australia: Asia Pacific': 'http://abc.net.au/ra/rss/asiapacific.rss',
             'ABC iView Programs': 'http://tvmp.abc.net.au/iview/rss/category/abc1.xml', 'ABC Hobart': 'http://www.abc.net.au/local/rss/hobart/news.xml',
             'First Dog on the Moon': 'http://www.abc.net.au/radionational/feed/5086350/rss.xml'}
app = Flask(__name__)

# openweathermap.org key 6e5115bf81e4d8257d80a79bb67db7a5
@app.route("/")
@app.route("/<publication>")
def get_news():
    try:
        query = urllib.parse.unquote_plus(request.args.get("publication"))
        if not query or query not in RSS_FEEDS:
            query = "ABC Hobart"
        feed = feedparser.parse(RSS_FEEDS[query])
        weather = get_weather("Hobart,Australia")
        return render_template("home.html", articles=feed['entries'], header=query, rssFeeds= RSS_FEEDS, weather=weather)
    except:
        return "no news is good news"

def get_weather(query):
    api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=6e5115bf81e4d8257d80a79bb67db7a5"
    query = urllib.parse.quote(query)
    url = api_url.format(query)
    data = urllib.request.urlopen(url).read()
    parsed = json.loads(data.decode("utf-8"))
    weather = None
    if parsed.get("weather"):
        weather = {"description":
                       parsed["weather"][0]["description"],
                   "temperature": parsed["main"]["temp"],
                   "city": parsed["name"]
                   }
    return weather

if __name__ == '__main__':
    app.run(port=5000, debug=True)
