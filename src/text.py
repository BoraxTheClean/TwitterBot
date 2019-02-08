import os
import tweepy
import boto3
import datetime

'''
    AWS Client Initialization
'''

ssm = boto3.client('ssm')

'''
    Twitter API Initialization
'''

try:
    CONSUMER_KEY = ssm.get_parameter(Name='CONSUMER_KEY',WithDecryption=True)['Parameter']['Value']
    CONSUMER_SECRET = ssm.get_parameter(Name='CONSUMER_SECRET',WithDecryption=True)['Parameter']['Value']
    ACCESS_TOKEN = ssm.get_parameter(Name='ACCESS_TOKEN',WithDecryption=True)['Parameter']['Value']
    ACCESS_SECRET = ssm.get_parameter(Name='ACCESS_SECRET',WithDecryption=True)['Parameter']['Value']
except Exception as error:
    print(error)
    print("Failed to fetch api keys.")

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)
user = api.me()
print('Tweeting for '+user.name)
def handler(event, context):
    text = make_tweet()
    clear_timeline()
    send_tweet(text)

def make_tweet():
    return "I'm so glad I learned AWS Lambda and Python with @AWSOwen's free GumRoad course at store.owen.dev"


def send_tweet(text):
    print(text)
    api.update_status(text)


#Deletes tweets older than a week.
def clear_timeline():
    now = datetime.datetime.now()
    last_week = now - datetime.timedelta(days=1)
    for i in range(20):
        try:
            tweets = api.user_timeline(page=i)
        except Error as error:
            print(error)
        if len(tweets) == 0:
            return
        for tweet in tweets:
            if tweet.created_at < last_week:
                print("Deleting "+str(tweet.id))
                destroy_status(tweet.id)


def destroy_status(id):
    api.destroy_status(id)
