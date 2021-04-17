import key
import src.Tweets as t

# Driver Function
if __name__ == '__main__':
    try:
        # Data Collection & Cleaning
        tweets = t.Tweets()
        tweets._fetch()
        REDU:
        tweets._model()
    except Exception as e:
        goto REDU
        pass
    exit("App Closes")