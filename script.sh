mkdir dist
cp src/* dist/

pip3 install -r requirements.txt -t dist/
aws cloudformation package --template-file template.yaml --s3-bucket owen-lambda-bucket --s3-prefix twitter-bot --output-template processed.template.yaml
aws cloudformation deploy --template-file processed.template.yaml --stack-name corp-twitter-bot --capabilities CAPABILITY_IAM --region us-east-1

rm processed.template.yaml
rm -rf dist/
