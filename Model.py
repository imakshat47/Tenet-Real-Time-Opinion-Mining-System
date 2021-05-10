import key
import threading
from time import sleep
import src.Mongodb as db
import src.SentimentAnalysis as senti
import src.Translate as trans
# Model class


class Model(object):
    # init method
    def __init__(self):
        self.count = 0
        print("Model Loading...")

    def _run_heroku(self,  _obj=None):
        print("Heroku Running...")
        # db instance
        self.__db = db.MongoDB(key._db_name, key._db_document)
        # self._db = db.MongoDB(key._db_name, key._db_result)
        # Sentiment Score Instance
        self.sa = senti.SentimentAnalysis()
        # Translator Instance
        self.trans_module = trans.Translate()
        # Data Loop
        threads = []        
        for data in self.__db._sorted_find(_obj, key._tweet_limit):
            try:
                thread = threading.Thread(None, target=self.__middleware, args=(
                    data['tweet'], data['lang'], data['_id'],))
                thread.start()
                threads.append(thread)
                if len(threads) == 10:
                    for thread in threads:
                        thread.join()
                    threads = []
            except:
                print("Error here => ", e)
                sleep(30)
                continue
        print("Threads Running: ", threading.enumerate())

        for thread in threads:
            print("Active Thread Left => ", threading.active_count())
            thread.join()
        self.__db.__del__()
        # self._db.__del__()

        print("Active Thread => ", threading.active_count())

        print("Heroku Ends!!")
        sleep(key._sleep_time)
        print(threading.current_thread())
        self._run_heroku(_obj)

    # middleware for heroku
    def __middleware(self, text, lang_tag, id):
        _err = False
        self.count += 1

        if len(text) <= 25:
            _err = True

        if _err == False:
            try:
                sleep(key._sleep_time)
                trans_text = self.trans_module._translate(text, lang_tag)
                print("Translated Text: ", trans_text)
            except:
                _err = True

        if _err == True:
            print("Error for Id: ", id)
            self.__db._delete({"_id": id})
            print("-- Thread End with Error --    @ ", self.count)
            return None

        polarity = self.sa._score(text)
        trans_polarity = self.sa._score(trans_text)
        set_data = {"$set": {"trans_text": trans_text,
                             "polarity": polarity, "trans_polarity": trans_polarity}}
        print("Updating with: ", set_data)
        self.__db._update({"_id": id}, set_data)

        print("-- Thread End --    @ ", self.count)
        return None        