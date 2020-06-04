# TwitterBot
## Setup

Apply for a developer account at https://developer.twitter.com/

Make an app and record your consumer key and secret.

To get your access key and secret: https://github.com/tweepy/examples/blob/master/oauth/getaccesstoken.py

Run this code locally, and authorize your bot account to use this app. Then the python script will print out your Access Key and Secret.

```python
import webbrowser

import tweepy

"""
    Query the user for their consumer key/secret
    then attempt to fetch a valid access token.
"""

if __name__ == "__main__":

    consumer_key = raw_input('Consumer key: ').strip()
    consumer_secret = raw_input('Consumer secret: ').strip()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)

    # Open authorization URL in browser
    webbrowser.open(auth.get_authorization_url())

    # Ask user for verifier pin
    pin = raw_input('Verification pin number from twitter.com: ').strip()

    # Get access token
    token = auth.get_access_token(verifier=pin)

    # Give user the access token
    print 'Access token:'
    print '  Key: %s' % token.key
    print '  Secret: %s' % token.secret

```
## Confirm SSM Parameters

It is assumed that there are SSM parameters in your deployment region at `CONSUMER_SECRET` `CONSUMER_KEY` `ACCESS_TOKEN` `ACCESS_SECRET`. For help making SSM parameters: https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-console.html

![SSM Console](https://raw.githubusercontent.com/BoraxTheClean/TwitterBot/master/SSM.png)

## Python Code

We use the tweepy sdk to access the twitter api and boto3 API to access SSM Parameter Store.

```python
import tweepy
import boto3

'''
    AWS Client Initialization
'''

ssm = boto3.client('ssm')
```

Next we pull parameters from SSM using the AWS API. I use the `WithDecryption` flag to decrypt the values, since I chose the `SecureString` option when creating my parameters.

```python
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
```

Then we initialize our tweepy client with the decrypted secrets we pulled in the previous steps.

```python

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)

auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

api = tweepy.API(auth)
user = api.me()
print('Tweeting for '+user.name)

```
Finally, we define a handler for Lambda to invoke our function through. We wrap our business logic in convenient functions, and we're done.

```python
def handler(event, context):
    text = make_tweet()
    send_tweet(text)

def make_tweet():
    return "#BlackLivesMatter https://blacklivesmatters.carrd.co/"

def send_tweet(text):
    print(text)
    filename='BlackSquare.jpg'
    api.update_with_media(filename,status=text)

```

## Deployment

Modify this line of script.sh and replace `owen-lambda-bucket` with your own s3 bucket located in the region you are deploying into.

```Make
BUCKET=owen-lambda-bucket
```

Then simply run
```bash
make deploy
```

## Deploy and Enjoy

[Have fun coding! And be sure to follow me on GumRoad for new courses and updates!](https://store.owen.dev)

[Find me on Twitter.](https://twitter.com/AWSOwen)

[Shoot me an email.](mailto:owen@owen.dev)
