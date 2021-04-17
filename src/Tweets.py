import key
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
import src.Mongodb as db
import src.PreProcess as preProcess
import src.Translate as trans
import src.SentimentAnalysis as senti


# Listen to stream and return it
class StdOutListener(StreamListener):
    def __init__(self):
        super().__init__()
        self.__count = 0
        self.__max_tweets = key._tweet_max_count
        self.__pre = preProcess.PreProcess()
        self.__db = db.MongoDB(key._db_name, key._db_document)

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
            __lang = data['lang']
            __tweet = data['extended_tweet']['full_text']
        except:
            pass
        if(__tweet == ''):
            return True
        # Data Cleaning
        __tweet = self.__pre._clean(__tweet)
        __tweet = self.__pre._emojis(__tweet, True)
        # Object of data
        _obj = {"tweet": __tweet, "lang": __lang}
        print(_obj)
        self.__db._insert(_obj)
        self.__count += 1
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
        # Final Polarity
        self.__polarity = 0

    def _fetch(self, _track=["Modi", "Covid", "IPL", "Stock Market"]):
        __stream = Stream(self.__auth, StdOutListener())
        __stream.filter(track=_track)
        print("Tweets Collected.")

    def _model(self):
        # Mongo Instance
        __db = db.MongoDB(key._db_name, key._db_document)
        tweets = __db._find()        
        sa = senti.SentimentAnalysis()
        # Translator Instance
        trans_module = trans.Translate()        
        # result
        _db = db.MongoDB(key._db_name, key._db_result)
        _count = 0
        # Data Loop
        for data in tweets:
            polarity = sa._score(data['tweet'])
            trans_text = trans_module._translate(data['tweet'], data['lang'])
            trans_polarity = sa._score(trans_text)
            set_data = {"$set": {"trans_text": trans_text,"polarity": polarity, "trans_polarity": trans_polarity}}
            print(set_data)
            __db._update({"_id": data['_id']}, set_data)
            self.__polarity = self.__polarity + trans_polarity
            _count += 1            
            if _count // key._tweet_set == 0:
                self.__polarity = self.__polarity / key._tweet_set
                print(self.__polarity)
                _db._insert({"final_score": self.__polarity})
                self.__polarity = 0