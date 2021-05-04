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
        self.count = 0
        for data in self.__db._sorted_find(_obj, key._tweet_limit):
            try:
                # print("Tweet => ", data)
                thread = threading.Thread(None, target=self.__middleware, args=(
                    data['tweet'], data['lang'], data['_id'],))
                thread.start()
                threads.append(thread)
                print("Active Thread => ", threading.active_count())
                if len(threads) == 10:
                    for thread in threads:
                        thread.join()
                    threads = []
            except:
                print("Error here => ", e)
                sleep(30)
                continue
        for thread in threads:
            print("Active Thread Left => ", threading.active_count())
            thread.join()
        self.__db.__del__()
        # self._db.__del__()

        print("Active Thread => ", threading.active_count())
        print("Threads Running: ", threading.enumerate())
        print(threading.current_thread())

        print("Heroku Ends!!")
        self._run_heroku(_obj)

    # middleware for heroku
    def __middleware(self, text, lang_tag, id):
        print("-- Thread Set --")
        sleep(key._sleep_time)
        print("Thread Active Now!!")
        # result
        polarity = self.sa._score(text)
        # print("Going to sleep...")
        # sleep(key._sleep_time)
        # print("Back from sleep...")
        trans_text = self.trans_module._translate(text, lang_tag)
        # print("Going to sleep...")
        # sleep(key._sleep_time)
        # print("Back from sleep...")
        trans_polarity = self.sa._score(trans_text)
        set_data = {"$set": {"trans_text": trans_text,
                             "polarity": polarity, "trans_polarity": trans_polarity}}
        print(set_data)
        self.__db._update({"_id": id}, set_data)

        # print("Going to sleep...")
        # sleep(key._sleep_time)
        # print("Thread Active...")

        # Update Result
        # _obj = self._db._find({"_id": key._tenet_record})
        # if _obj != None:
        #     _obj = _obj[0]['ordinals']
        # # print(_obj)
        # if trans_polarity == 0:
        #     _obj[0] += 1
        # elif trans_polarity > 0:
        #     if trans_polarity >= .5:
        #         _obj[1] += 1
        #     else:
        #         _obj[2] += 1
        # else:
        #     if trans_polarity < -0.5:
        #         _obj[3] += 1
        #     else:
        #         _obj[4] += 1
        # self.count += 1
        # self._db._update({"_id": key._tenet_record}, {
        #                  "$set": {"ordinals": _obj, "count_dataset": self.count}})
        print("-- Thread End --    @ ", self.count)
        return None
