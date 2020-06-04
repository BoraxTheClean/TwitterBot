import tweepy
import boto3

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
    raise error

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)
user = api.me()
print('Tweeting for '+user.name)
def handler(event, context):
    text = make_tweet()
    send_tweet(text)

def make_tweet():
    return "#BlackLivesMatter https://blacklivesmatters.carrd.co/"


def send_tweet(text):
    print(text)
    filename='BlackSquare.jpg'
    api.update_with_media(filename,status=text)
