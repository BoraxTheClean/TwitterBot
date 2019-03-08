# TwitterBot
## Setup

Apply for a developer account at https://developer.twitter.com/

Make an app and record your consumer key and secret.

To get your access key and secret: https://github.com/tweepy/examples/blob/master/oauth/getaccesstoken.py

It is assumed that there are SSM parameters in your deployment region at `CONSUMER_SECRET` `CONSUMER_KEY` `ACCESS_TOKEN` `ACCESS_SECRET`. For help making SSM parameters: https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-console.html

```    
    CONSUMER_KEY = ssm.get_parameter(Name='CONSUMER_KEY',WithDecryption=True)['Parameter']['Value']
    CONSUMER_SECRET = ssm.get_parameter(Name='CONSUMER_SECRET',WithDecryption=True)['Parameter']['Value']
    ACCESS_TOKEN = ssm.get_parameter(Name='ACCESS_TOKEN',WithDecryption=True)['Parameter']['Value']
    ACCESS_SECRET = ssm.get_parameter(Name='ACCESS_SECRET',WithDecryption=True)['Parameter']['Value']
```

## Deployment

Modify this line of script.sh and replace `owen-lambda-bucket` with your own s3 bucket located in the region you are deploying into.

```
aws cloudformation package --template-file template.yaml --s3-bucket ***owen-lambda-bucket*** --s3-prefix twitter-bot --output-template processed.template.yaml
```

Then simply run
```
./script.sh
```

## Deploy and Enjoy

Have fun coding!
