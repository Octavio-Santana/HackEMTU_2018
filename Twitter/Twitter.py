import json
from requests_oauthlib import OAuth1Session
import requests

class MyTwitter(object):
    # preencha com os dados do seu app
    BASE_URL = "https://api.twitter.com/1.1/search/tweets.json"
    API_KEY = 'EI41mMUkf4FROyZLe3cSdjZ0U'
    API_SECRET = 'GsczTIDDDX84IJtz6cMuwwJLJF7NjNODlULOH5GwxL8vKfMa81'
    ACCESS_TOKEN = '982701662300262401-8rQan7ZvODoxLnamqiOIjrZjbWmK6iN'
    ACCESS_TOKEN_SECRET = 'X9rYT3cyGxBlW0KAHhaNJBnlWBur0qdN3xqTDimHqVuVi'

    session = OAuth1Session(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    def get_tweets(self, keyword, n=100):
        url = self.BASE_URL + ("?q=%s&count=%d" % (requests.utils.quote(keyword), n))
        response = self.session.get(url)
        tweets = json.loads(response.content.decode("utf-8"))
        return tweets['statuses']

    def retweet_count(self, keyword, n=100):
        tweet = self.get_tweets(keyword, n)
        return [t['text'] for t in sorted(tweet, key=lambda x: x['retweet_count'], reverse=True)]