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

### Aurora Serverless

## aurora_serverless_connection

Lambda function to connect to a Aurora Serverless database and execute a select

## aurora_serverless_insert

Lambda function to insert data into a Aurora Serverless database