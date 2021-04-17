import key
import src.Tweets as t
import src.Mongodb as db
import src.Translate as trans
import src.SentimentAnalysis as senti
# Driver Function
if __name__ == '__main__':
    try:
        # Data Collection & Cleaning
        tweets = t.Tweets()
        tweets._fetch()

        # Model Working
        # Mongo Instance
        __db = db.MongoDB(key._db_name, key._db_document)
        tweets = __db._find()
        __db.__del__()
        sa = senti.SentimentAnalysis()
        # Translator Instance
        trans_module = trans.Translate()
        # Final Polarity
        _polarity = 0
        # result
        _db = db.MongoDB(key._db_name, "result")
        _count = 0
        # Data Loop
        for data in tweets:
            polarity = sa._score(data['tweet'])
            trans_text = trans_module._translate(data['tweet'], data['lang'])
            trans_polarity = sa._score(trans_text)
            set_data = {"$set": {"trans_text": trans_text,"polarity": polarity, "trans_polarity": trans_polarity}}
            __db._update({"_id": data['_id']}, set_data)
            _polarity = _polarity + trans_polarity
            _count += 1
            if _count // 10 == 0:
                _db._insert({"final_score" : _polarity})
    except Exception as e:
        print('App Error => ', e)
    exit("App Closes")
