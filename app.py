import key
import src.Tweets as t

# Driver Function
if __name__ == '__main__':
    try:
        tweets = t.Tweets()
        # Data Collection & Cleaning
        tweets._fetch()
        tweets._model()
    except Exception as e:
        tweets._model()
        print("App Error:  ", e)
        pass
    print("App Closes")