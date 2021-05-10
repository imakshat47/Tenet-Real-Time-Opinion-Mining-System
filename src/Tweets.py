import key
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from src.Database import MongoDB
from src.PreProcess import PreProcess
from src.Translate import MTS
import var

# Listen to stream and return it
class StdOutListener(StreamListener):
    def __init__(self):
        super().__init__()
        self.__count = var._tweet_count
        self.__max_tweets = var._tweet_max_count
        self.__pre = PreProcess()
        self.__mts = MTS()
        self.__db = MongoDB(key._db_name, key._db_document)

    def on_timeout(self):
        print("TimeOut !!")

    def on_data(self, _data):
        # Check Condition
        if(self.__count == self.__max_tweets):
            return False
        # Defining Local Var
        __tweet = ''
        __lang = 'hi'
        raw_data = _data
        # Scratching data
        try:
            data = json.loads(raw_data)
            __tweet = data['extended_tweet']['full_text']
            if len(__tweet) <= var._min_text_len:
                raise("Smaller Text!!")
            __lang = data['lang']
            # Data Cleaning
            __tweet = self.__pre._clean(__tweet)
            __tweet = self.__pre._emojis(__tweet, True)
            _text = self.__mts._translator(__tweet)
            # Object of data
            self.__count += 1
            _obj = {"__text": __tweet, "lang": __lang, "_count": self.__count, "translated_text": _text}
            print(_obj)
            self.__db._insert(_obj)
        except Exception as e:
            print({e})            
        return True

    def on_error(self, status):
        print(status)
        return True

# Fetch Tweets from Tweepy


class Tweets(object):
    def __init__(self):
        # Variables that contain the user credentials to access Twitter API
        self.__consumer_key = key._consumer_key
        self.__consumer_secret = key._consumer_secret
        self.__access_token = key._auth_token
        self.__access_token_secret = key._auth_secret
        self.__auth = OAuthHandler(self.__consumer_key, self.__consumer_secret)
        self.__auth.set_access_token(
            self.__access_token, self.__access_token_secret)        

    def _fetch(self, _track=["Modi", "Covid", "IPL", "Stock Market"]):
        __stream = Stream(self.__auth, StdOutListener())
        __stream.filter(track=_track)
        print("Tweets Collected.")