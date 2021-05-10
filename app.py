import Model
from src.Tweets import Tweets
# Driver Function
if __name__ == '__main__':
    try:
        tweet = Tweets()
        # ,"Rotten Tomatoes Reviews"
        tweet._fetch(_track=["Amazon Product Reviews", "Service Reviews", "Call center Reviews", "Company’s Reputation"])
        # intiating Model
        # model = Model.Model()        
        # calling for heroku
        # model._run_heroku({"polarity": None})
    except Exception as e:
        print("App Error:  ", e)

    print("App Closes.")
