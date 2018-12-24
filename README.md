# python

In this repository I'll be adding my Python scripts.

### aws-ec2-manager.py

updated script that uses click module, and show more information about EC2 instances

## Configuring

uses the configuration file created by the AWS CLI. e.g.: 

aws configure --profile python

## Running

'pipenv run "python aws/aws-ec2-manager.py <command> <--project=PROJECT>"'

*command* is list, stop, or start
*project* is optional

### s3.py

## Running

python s3.py

Usage: s3.py [OPTIONS] COMMAND [ARGS]...

  Commands for S3 security check

Options:
  --help  Show this message and exit.

Commands:
  getbucketencryption
  getbucketpolicy
  getbucketversioning
  getpublicacl
  listbucket
  listbucketsize (limited to 1000 objects)

### codecommit.py

## Running

python codecommit.py

* lists 'HTTP URL' for each code commit repository

### stop/startEC2Instances.py

## Running

python stop/startEC2Instances.py

### ec2DescribeInstance.py

used to retrieve metadata information from EC2 instances

## Running 

python ec2DescribeInstance.py