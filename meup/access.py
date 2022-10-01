from .config import *

"""These are the types of import we might expect in this file
import httplib2
import oauth2
import tables
import mongodb
import sqlite"""

# This file accesses the data

"""Place commands in this file to access the data electronically. Don't remove any missing values, or deal with outliers. Make sure you have legalities correct, both intellectual property and personal data privacy rights. Beyond the legal side also think about the ethical issues around this data. """


import tweepy
import pandas as pd
import datetime

def twitter_client():
    """Return access to a twitter client."""

    bearer_token = config["twitter"]["bearer_token"]

    consumer_key = config["twitter"]["consumer_key"]
    consumer_secret = config["twitter"]["consumer_secret"]

    access_token = config["twitter"]["access_token"]
    access_token_secret = config["twitter"]["access_token_secret"]

    # You can authenticate as your app with just your bearer token
    return tweepy.Client(bearer_token=bearer_token)

def twitter_following(client):
    """Return a list of twitter users I'm following."""
    following = pd.read_csv(os.path.expandvars(os.path.join(config["twitter"]["following"]["directory"], config["twitter"]["following"]["file"])))
    ids = []
    names = []
    for username in following.username:
        user = client.get_user(username=username)
        ids.append(user.data.id)
        names.append(user.data.name)
    following["id"] = ids
    following["name"] = names
    following.set_index("id", inplace=True)
    return following

def twitter_get_tweets(client, following):
    """Get tweets from those that user is following."""
    for user_id in following.index:
        response = client.get_users_tweets(user_id, 
                                           max_results=5,
                                           end_time=datetime.datetime.now() - datetime.timedelta(days=1))
        username = following.loc[user_id]["username"]
        name = following.loc[user_id]["name"]
    return response
    
def tweet_like(client, tweetid):
    """Return all the users that like a particular tweet"""
    liking = client.get_liking_users(tweetid)
    
# You can provide the consumer key and secret with the access token and access
# token secret to authenticate as a user
#client = tweepy.Client(
#    consumer_key=consumer_key, consumer_secret=consumer_secret,
#    access_token=access_token, access_token_secret=access_token_secret
#)

def data():
    """Read the data from the web or local file, returning structured format such as a data frame"""
    raise NotImplementedError

