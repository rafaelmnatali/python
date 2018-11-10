# python

In this repository I'll be adding my Python scripts.

### aws-ec2-list-instances.py ###

uses boto3 to list AWS EC2 instances ids.

## Configuring

uses the configuration file created by the AWS CLI. e.g.: 

aws configure --profile python

## Running

'pipenv run "python aws/aws-ec2-list-instances.py'


### aws-ec2-manager.py

updated script that uses click module, and show more information about EC2 instances

## Configuring

uses the configuration file created by the AWS CLI. e.g.: 

aws configure --profile python

## Running

'pipenv run "python aws/aws-ec2-manager.py'
