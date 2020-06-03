# TwitterBot
## Setup

Thanks for checking out my Twitter Bot. You can also find my *Free Course* for this bot at https://store.owen.dev.

Apply for a developer account at https://developer.twitter.com/

Make an app and record your consumer key and secret.

To get your access key and secret: https://github.com/tweepy/examples/blob/master/oauth/getaccesstoken.py

Just run this code locally, and authorize your bot account to use this app. Then the python script will print out your Access Key and Secret.

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

It is assumed that there are SSM parameters in your deployment region at `CONSUMER_SECRET` `CONSUMER_KEY` `ACCESS_TOKEN` `ACCESS_SECRET`. For help making SSM parameters: https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-console.html

```python
    CONSUMER_KEY = ssm.get_parameter(Name='CONSUMER_KEY',WithDecryption=True)['Parameter']['Value']
    CONSUMER_SECRET = ssm.get_parameter(Name='CONSUMER_SECRET',WithDecryption=True)['Parameter']['Value']
    ACCESS_TOKEN = ssm.get_parameter(Name='ACCESS_TOKEN',WithDecryption=True)['Parameter']['Value']
    ACCESS_SECRET = ssm.get_parameter(Name='ACCESS_SECRET',WithDecryption=True)['Parameter']['Value']
```

## Deployment

Modify this line of script.sh and replace `owen-lambda-bucket` with your own s3 bucket located in the region you are deploying into.

```bash
aws cloudformation package --template-file template.yaml --s3-bucket ***owen-lambda-bucket*** --s3-prefix twitter-bot --output-template processed.template.yaml
```

Then simply run
```bash
make deploy
```

## Deploy and Enjoy

[Have fun coding! And be sure to follow me on GumRoad for new courses and updates!](https://store.owen.dev)
