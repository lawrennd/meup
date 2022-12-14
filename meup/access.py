import os
import fnmatch
import datetime

import pandas as pd
import tweepy

from .config import *
from .log import Logger

"""These are the types of import we might expect in this file
import httplib2
import oauth2
import tables
import mongodb
import sqlite"""


# This file accesses the data

"""Place commands in this file to access the data electronically. Don't remove any missing values, or deal with outliers. Make sure you have legalities correct, both intellectual property and personal data privacy rights. Beyond the legal side also think about the ethical issues around this data. """



log = Logger(
    name=__name__,
    level=config["logging"]["level"],
    filename=config["logging"]["filename"]
)


def twitter_client():
    """Return access to a twitter client."""

    bearer_token = config["twitter"]["bearer_token"]

    # You can authenticate as your app with just your bearer token
    return tweepy.Client(bearer_token=bearer_token)

def twitter_api():
    """Return access to the twitter API."""
    consumer_key = config["twitter"]["consumer_key"]
    consumer_secret = config["twitter"]["consumer_secret"]
    
    access_token = config["twitter"]["access_token"]
    access_token_secret = config["twitter"]["access_token_secret"]
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def twitter_following(client):
    """Return a list of twitter users I'm following."""
    following = pd.read_csv(os.path.expandvars(os.path.join(config["twitter"]["following"]["directory"], config["twitter"]["following"]["file"])))
    ids = []
    names = []
    for username in following.username:
        user = client.get_user(username=username)
        if user.data is None:
            if user.errors is not None:
                log.warning(f"Error when requesting twitterid \"{username}\"")
                ids.append("delete_row")
                names.append(None)
                continue
            else:
                raise Exception(f"Not able to access data for twitterid \"{username}\"")
        ids.append(int(user.data.id))
        names.append(user.data.name)
    following["id"] = ids
    following["name"] = names
    following.set_index("id", inplace=True)
    following.drop("delete_row", inplace=True)
    return following

def twitter_get_tweets(client, users, max_results=5):
    """Get tweets from those in a user list."""
    tweets = []
    for user_id in users.index:
        response = client.get_users_tweets(user_id, 
                                           max_results=max_results,
                                           end_time=datetime.datetime.now() - datetime.timedelta(days=1))
        for tweet in response.data:
            tweets.append({
                "id":  tweet.id,
                "text":  tweet.text,
                "username": users.loc[user_id]["username"],
                "name": users.loc[user_id]["name"],
                "user_id": user_id,
	})
    return pd.DataFrame(tweets).set_index("id")
    
def tweet_like(client, tweetid):
    """Return all the users that like a particular tweet"""
    twitter_liking = client.get_liking_users(tweetid)
    data = {
        "username": [],
        "name": [],
        "id": [],
        }
    for user in twitter_liking.data:
        data["username"].append(user.username)
        data["name"].append(user.name)
        data["id"].append(user.id)
    return pd.DataFrame(data=data).set_index("id")


def file_locations(top_dir, pattern, exclude_dir_prefix=None):
    try:
        for dir_path, dir_names, file_names in os.walk(top_dir):
                for file_name in file_names:
                    if not exclude_dir_prefix or not get_file_name(dir_path).startswith(exclude_dir_prefix):
                        if fnmatch.fnmatch(file_name, pattern):
                            yield os.path.join(dir_path, file_name)
    except (IOError, OSError) as ex:
        raise e.LoadFileException(str(ex)+'\nUnable to load ' + top_dir + ' with pattern ' + pattern + ' excluding ' + exclude_dir_prefix)

def referia_locations(dir):
    """Find referia locations."""
    return file_locations(dir, "_referia.yml")

# You can provide the consumer key and secret with the access token and access
# token secret to authenticate as a user
#client = tweepy.Client(
#    consumer_key=consumer_key, consumer_secret=consumer_secret,
#    access_token=access_token, access_token_secret=access_token_secret
#)

def data():
    """Read the data from the web or local file, returning structured format such as a data frame"""
    raise NotImplementedError

