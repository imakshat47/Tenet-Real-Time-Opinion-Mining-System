import key
import src.Tweets as t

# Driver Function
if __name__ == '__main__':
    try:
        # Data Collection & Cleaning        
        tweets = t.Tweets()
        tweets._model()
        tweets._fetch()        
        tweets._model()
    except Exception as e:
        tweets._model()
        print("App Error:   ", e)        
        pass
    exit("App Closes")