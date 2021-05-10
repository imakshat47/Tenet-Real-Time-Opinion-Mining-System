from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from src.Database import MongoDB
from src.PreProcess import PreProcess
from src.Translate import MTS
from time import sleep
import threading
import key
import var
import json

# Listen to stream and return it
class StdOutListener(StreamListener):
    def __init__(self):
        super().__init__()
        self.__count = var._tweet_count
        self.__max_tweets = var._tweet_max_count
        self.__pre = PreProcess()
        self.__db = MongoDB(key._db_name, key._db_document)
        self.__mts = MTS()
        self._threads = []
        self._sleep_time = 0.2

    def on_timeout(self):
        print("TimeOut !!")

    def on_data(self, _data):
        # Check Condition
        if(self.__count == self.__max_tweets):
            return False
        # Defining Local Var
        __text = ''
        __lang = 'hi'
        raw_data = _data
        # Scratching data
        try:
            print("Count: ", self.__count)
            data = json.loads(raw_data)            
            __text = data['extended_tweet']['full_text']            
            if len(__text) <= var._min_text_len:
                raise  Exception("Smaller Text!!")
            __lang = data['lang']                        
        except Exception as e:
            print({e})
            return True
        thread = threading.Thread(None, target=self.__cleaning, args=(__text, __lang, self.__count, ), daemon=True)
        thread.start()
        self._threads.append(thread)   
        return True
    
    def __cleaning(self, _text, _lang, _count):
        print("Text Cleaning...")
        # Data Cleaning
        sleep(self._sleep_time)
        _text = self.__pre._clean(_text)
        sleep(self._sleep_time)
        _text = self.__pre._emojis(_text, True)
        sleep(self._sleep_time)
        trans_text = self.__mts._translator(_text,_lang)
        sleep(self._sleep_time)
        # Object of data
        self.__count += 1
        _obj = {"__text": _text, "lang": _lang, "_count": _count, "translated_text": trans_text}
        print(_obj)
        sleep(self._sleep_time)
        self.__db._insert(_obj)
        return None

    def on_disconnect(self, notice):
        for thread in self._threads:
            print("Active Threads: ", threading.active_count())
            thread.join()
        print("Closing: ",notice)
        return

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
        print("Tweets Fetching...")
        __stream = Stream(self.__auth, StdOutListener())
        __stream.filter(track=_track)
        print(threading.current_thread())
        print("Tweets Collected!!")