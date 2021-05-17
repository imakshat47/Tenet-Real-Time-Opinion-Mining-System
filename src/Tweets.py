import tweepy
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from src.Database import MongoDB
from src.PreProcess import PreProcess
from time import sleep
import threading
import random
import key
import var
import json

# Listen to stream and return it
class StdOutListener(StreamListener):
    def __init__(self, _count):
        print("Tweepy Stream Connection...")
        super().__init__()
        self.__count = _count
        self.__max_tweets =  _count + var._tweet_max_count
        print("Max: ", self.__max_tweets)
        self.__pre = PreProcess()
        self.__db = MongoDB(key._db_name, key._db_document)      
        self._sleep_time = random.randint(1, 5)
        print("Sleep Time: ", self._sleep_time)

    def on_connect(self):
        print("Tweepy Stream Connection Success!!")
        pass
    
    def on_exception(self, exception):
        """Called when an unhandled exception occurs."""
        print("Exception: ", exception)
        return True
    
    def on_limit(self, track):
        """Called when a limitation notice arrives"""
        print("Limit: ", track)
        return True
    
    def on_error(self, status_code):
        """Called when a non-200 status code is returned"""
        print("Error Code: ", status_code)
        return True

    def on_timeout(self):
        """Called when stream connection times out"""        
        print("TimeOut!!")
        return True

    def on_disconnect(self, notice):
        """Called when twitter sends a disconnect notice
        Disconnect codes are listed here:
        https://developer.twitter.com/en/docs/tweets/filter-realtime/guides/streaming-message-types
        """
        print("Disconnect: ", notice)
        return True

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
            try:
                data = json.loads(raw_data)            
                sleep(self._sleep_time)
                __lang = data['lang']  
                __text = data['extended_tweet']['full_text']            
            except:
                __text = data['text']
                
            if len(__text) <= var._min_text_len:
                raise  Exception("Smaller Text!!")
            
            print("Text: ", __text)            
            
            print("Text Cleaning...")
            # Data Cleaning            
            sleep(self._sleep_time)                    
            _text = self.__pre._clean(__text)            
            sleep(self._sleep_time)                        
            _text = self.__pre._emojis(_text, True)            
            sleep(self._sleep_time)                    
            
            # Object of data
            self.__count += 1
            print("Count: ", self.__count)
            
            if len(_text) <= var._min_text_len:
                raise  Exception("Smaller Text!!")
            
            _obj = {"__text": _text, "lang": __lang, "_count": self.__count}
            print(_obj)            
            sleep(self._sleep_time)            
            self.__db._insert(_obj)
            
        except Exception as e:
            print("Exception: ",{e})            
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
        self.__auth.set_access_token(self.__access_token, self.__access_token_secret)       
        self._sleep_time = random.randint(1, 10) 

    def __fetch(self, _track, _count):
        try:
            print("Connecting Tweepy...")            
            sleep(self._sleep_time)
            __stream = Stream(self.__auth, StdOutListener(_count))
            print("Fetch Count: ", _count)
            __stream.filter(track=_track)
            sleep(self._sleep_time)
            print(threading.current_thread())
        except:
            print("Fetching Error!!") 
        sleep(self._sleep_time)
        print("One Thread Done!!")
        return None           

    def _fetch(self, _track=["Modi", "Covid", "IPL", "Stock Market"], _number = 10):
        threads = []                
        db = MongoDB(key._db_name, key._db_document)         
                
        while _number:
            print("Threading...")
            sleep(self._sleep_time)
            _count = db._count()
            sleep(self._sleep_time)            
            print("Row Count: ", _count)
            print("Number: ",_number)   
            print(threading.current_thread()) 
            self.__fetch(_track, _count)
            sleep(self._sleep_time)            
            # thread = threading.Thread(None, target=self.__fetch, args=(_track,_count,), daemon=True)
            sleep(self._sleep_time)
            # threads.append(thread) 
            sleep(self._sleep_time)        
            # thread.start()
            
            sleep(self._sleep_time)
            if len(threads) == var._max_allowed_threads:
                for thread in threads:
                    print("Active Threads: ", threading.active_count())
                    thread.join()
                threads = []
            sleep(self._sleep_time)            
            _number -= 1    
            print("Number: ",_number)    
        
        # Cleaning Threads
        print("Cleaning Threads: ")        
        while len(threads):
            for thread in threads:
                print("Active Threads: ", threading.active_count())
                thread.join()
        
        if len(threads) == 0:    
            print("Threads Cleaned.")
        
        print("Active Threads: ", threading.active_count())
        print("Tweets Collected!!")