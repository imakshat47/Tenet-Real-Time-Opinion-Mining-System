from textblob import TextBlob


class SentimentAnalysis(object):

    def _score(self, text):
        return TextBlob(text).sentiment.polarity
