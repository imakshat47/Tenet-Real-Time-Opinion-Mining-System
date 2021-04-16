import os
from os import environ

_tweet_max_count = 50000

_consumer_key = environ['C_KEY']
_consumer_secret = environ['C_SEC']
_auth_token = environ['A_TOKEN']
_auth_secret = environ['A_SEC']

# Mongo DB URI
_mongo_uri = environ['MONGO_URI']

_db_name = "tenet"
_db_document = "tweets"