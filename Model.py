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

    def _run_heroku(self):
        print("Heroku Running...")
        # db instance
        self.__db = db.MongoDB(key._db_name, key._db_document)
        self._db = db.MongoDB(key._db_name, key._db_result)
        # Sentiment Score Instance
        self.sa = senti.SentimentAnalysis()
        # Translator Instance
        self.trans_module = trans.Translate()
        # fetch tweets
        tweets = self.__db._sorted_find(None, key._tweet_limit)
        # print(tweets)
        # Data Loop
        threads = []
        for data in tweets:
            try:
                print("Id => ", data['_id'])
                thread = threading.Thread(None, target=self.__middleware, args=(
                    data['tweet'], data['lang'], data['_id'],))
                thread.start()
                threads.append(thread)
                print("Active Thread => ", threading.active_count())
            except Exception as e:
                print("Error here => ", e)
                continue
        for thread in threads:
            print("Active Thread Left => ", threading.active_count())
            thread.join()
        self.__db.__del__()
        self._db.__del__()

        print("Active Thread => ", threading.active_count())
        print("Threads Running: ", threading.enumerate())
        print(threading.current_thread())

        print("Heroku Ends!!")

    # middleware for heroku
    def __middleware(self, text, lang_tag, id):
        print("-- Thread Set --")
        sleep(0.5)
        print("Thread Active Now!!")
        # result
        polarity = self.sa._score(text)
        trans_text = self.trans_module._translate(text, lang_tag)
        trans_polarity = self.sa._score(trans_text)
        set_data = {"$set": {"trans_text": trans_text,
                             "polarity": polarity, "trans_polarity": trans_polarity}}
        print(set_data)
        self.__db._update({"_id": id}, set_data)

        # Update Result
        _obj = self._db._find({"_id": key._tenet_record})
        if _obj != None:
            _obj = _obj[0]['ordinals']
        print(_obj)
        if trans_polarity == 0:
            _obj[0] += 1
        elif trans_polarity > 0:
            if trans_polarity >= .5:
                _obj[1] += 1
            else:
                _obj[2] += 1
        else:
            if trans_polarity < -0.5:
                _obj[3] += 1
            else:
                _obj[4] += 1
        self._db._update({"_id": key._tenet_record}, {
                         "$set": {"ordinals": _obj}})
        print("-- Thread Ends --")
        return None

# //polarity = sa._score(data['tweet'])
# //                trans_text = trans_module._translate(
# //                    data['tweet'], data['lang'])
# //                trans_polarity = sa._score(trans_text)
# //                set_data = {"$set": {"trans_text": trans_text,
# //                                     "polarity": polarity, "trans_polarity": trans_polarity}}
# //                print(set_data)
# //                __db._update({"_id": data['_id']}, set_data)
# //                if trans_polarity > 0:
# //                    self.__pos_polarity = trans_polarity
# //                else:
# //                    self.__neg_polarity = trans_polarity
# //                _count += 1
# //                print(_count)
# //                _id = _count % 10
# //                print(_id)
# //                # Updates Positive & Negative Score to DB
# //                _score = (self.__pos_polarity + abs(self.__neg_polarity)) / 2
# //                _obj = {"_id": _id, "count": _count, "pos_polarity": self.__pos_polarity,
# //                        "neg_polarity": self.__neg_polarity, "polarity": _score}
# //                print(_obj)
# //                _db._insert(_obj, True)
