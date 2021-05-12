import Model
from src.Tweets import Tweets
# Driver Function
if __name__ == '__main__':
    try:
        print("App Starts...")
        # Fetching Tweets
        tweet = Tweets()        
        tweet._fetch(_track=["Call center Reviews", "New Product Review", "Product Complaints", "Customer Service Center","Customer HelpCenter", "Amazon Product Reviews", "Service Reviews", "Company’s Reputation", "Product Comment"])
        
        # intiating Model
        # model = Model.Model()        
        # calling for heroku
        # model._run_heroku({"polarity": None})
    except Exception as e:
        print("App Error:  ", e)

    print("App Closed.")
