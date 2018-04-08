from textblob import TextBlob
from Twitter import MyTwitter
twitter = MyTwitter()
#tweets = twitter.retweet_count('#vilaocultahacka', 100)

class Twitter_Sentiment(object):

    def analise_sentimento(keyword='#vilaocultahacka'):
        tweets = twitter.retweet_count(keyword, 100)
        sentiment = []
        for t in tweets:
            text = TextBlob(t)
            if text.detect_language() != 'en':
                traduction = TextBlob(str(text.translate(to='en')))
                sentiment.append(traduction.sentiment.polarity)
            else:
                sentiment.append(text.sentiment.polarity)

        return sum(sentiment)