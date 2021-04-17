import key
import src.Tweets as t

# Driver Function
if __name__ == '__main__':
    try:
        # Data Collection & Cleaning
        tweets = t.Tweets()
        tweets._fetch()
        tweets._model()
    except Exception as e:
        print('App Error => ', e)
    exit("App Closes")
