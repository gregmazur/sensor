#create s3 bucket
aws s3 mb s3://sensor-code-sam

#package cloudformation
aws cloudformation package --s3-bucket sensor-code-sam --template-file template.yaml --output-template-file gen/template-gen.yaml

#deploy
aws cloudformation deploy --template-file gen/template-gen.yaml --stack-name sensor-sam --capabilities CAPABILITY_IAM


