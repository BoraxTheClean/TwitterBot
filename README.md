# TwitterBot

![architecture-diagram](https://raw.githubusercontent.com/BoraxTheClean/TwitterBot/master/TwitterBot.png)

## Setup

Apply for a developer account at https://developer.twitter.com/

We need to get four secrets from Twitter to use their API:
  - ACCESS_SECRET
  - ACCESS_TOKEN
  - CONSUMER_KEY
  - CONSUMER_SECRET

After you make an app you can get your _CONSUMER_KEY_ and _CONSUMER_SECRET_ from the Twitter API console.

Then you can generate your _ACCESS_SECRET_ and _ACCESS_TOKEN_ in the API console as well.

![Generating Twitter Secrets](https://dev-to-uploads.s3.amazonaws.com/i/k0rs45pazkja17khaqns.png)

## Confirm SSM Parameters

It is assumed that there are SSM parameters in your deployment region at `CONSUMER_SECRET` `CONSUMER_KEY` `ACCESS_TOKEN` `ACCESS_SECRET`. For help making SSM parameters: https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-console.html

![SSM Console](https://raw.githubusercontent.com/BoraxTheClean/TwitterBot/master/SSM.png)

## Lambda Configuration

Our Lambda Function has a name, _twitter-bot_, a handler, the method `handler(event,context)` in the file `text.py`, and we want to use the latest python3.8 runtime.

```yaml
SimpleTwitterApp:
    Type: AWS::Serverless::Function
    Properties:
        FunctionName: twitter-bot
        CodeUri: dist/
        Handler: text.handler
        Runtime: python3.8
```

We give our Function basic SSM permisions, so it can fetch the parameters we configured for it.

```yaml
Policies:
  - Version: '2012-10-17'
    Statement:
      - Effect: Allow
        Action: ssm:GetParameter
        Resource: '*'
```

Finally, we add an event to the function, sending out or tweet every 24 hours.

If you want to send tweets more often, you'll have to make them dynamic, twitter blocks repeat tweets in a 24 hour period.

```yaml
Events:
  TweetEveryDay:
    Type: Schedule
    Properties:
      Schedule: rate(1 day)
```

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
## Confirm SSM Parameters

Next we pull parameters from SSM using the AWS API. I use the `WithDecryption` flag to decrypt the values, since I chose the `SecureString` option when creating my parameters.

![SSM Console](https://raw.githubusercontent.com/BoraxTheClean/TwitterBot/master/SSM.png)

## Lambda Configuration

Our Lambda Function has a name, _twitter-bot_, a handler, the method `handler(event,context)` in the file `text.py`, and we want to use the latest python3.8 runtime.

```yaml
SimpleTwitterApp:
    Type: AWS::Serverless::Function
    Properties:
        FunctionName: twitter-bot
        CodeUri: dist/
        Handler: text.handler
        Runtime: python3.8
```

We give our Function basic SSM permisions, so it can fetch the parameters we configured for it.

```yaml
Policies:
  - Version: '2012-10-17'
    Statement:
      - Effect: Allow
        Action: ssm:GetParameter
        Resource: '*'
```

Finally, we add an event to the function, sending out or tweet every 24 hours.

If you want to send tweets more often, you'll have to make them dynamic, twitter blocks repeat tweets in a 24 hour period.

```yaml
Events:
  TweetEveryDay:
    Type: Schedule
    Properties:
      Schedule: rate(1 day)
```

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
    return "I've completed my Quest!\n\nI built this Lambda Bot using @AWSOwen's course!"


def send_tweet(text):
    print(text)
    api.update_status(text)
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
