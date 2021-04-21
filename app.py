import key
import src.Tweets as t

# Driver Function
if __name__ == '__main__':
    try:
        tweets = t.Tweets()
        # Data Collection & Cleaning
        tweets._model({'polarity': {'$exists': False}})                 # to be removed in near future
        tweets._fetch()
        tweets._model()
    except Exception as e:
        tweets._model({'polarity': {'$exists': False}})
        print("App Error:  ", e)        
    print("App Closes")