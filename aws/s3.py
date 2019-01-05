import boto3
import click
import botocore
from prettytable import PrettyTable

# Retrieve s3 information
s3 = boto3.resource('s3')
client = boto3.client('s3')

@click.group()
def buckets():
    """Commands for S3 information"""
    """uses the click library to allow for command line parameters"""
    """uses the prettytable library to output the results in table format"""

# list S3 buckets
@buckets.command('listbucket')
@click.option('--listbucket', default="true", help="List S3 bucket names")
def list_bucket(listbucket):
    x = PrettyTable()
    x.field_names = ["S3 Bucket"]
    x.align["S3 Bucket"] = "l"

    for bucket in s3.buckets.all():
        x.add_row([bucket.name])

    print(x)
    return

# list S3 bucket size - boto3 library limits the retrieval of objects to 1000
@buckets.command('listbucketsize')
@click.option('--listbucketsize', default="true", help="List S3 bucket size")
def list_bucket_size(listbucketsize):
    x = PrettyTable()
    x.field_names = ["S3 Bucket", "Size (Mb)"]
    x.align["S3 Bucket"] = "l"

    for bucket in s3.buckets.all():
        response = client.list_objects(Bucket=bucket.name)
        try:
            r = len(response['Contents'])
            size = 0
            for r in response['Contents']:
                size = (r['Size']) + size
            size = size/1024/1024
            x.add_row([bucket.name, round(size,2)])

        except KeyError:
            x.add_row([bucket.name, "No Size information"])

    print(x)


# List S3 buckets with Public Access enabled 
@buckets.command('getpublicacl')
@click.option('--getpublicacl', default="true", help="List S3 buckets with Public Access enabled")
def acl_bucket(getpublicacl):
    x = PrettyTable()
    x.field_names = ["S3 Public Buckets", "Permission"]
    x.align["S3 Public Buckets"] = "l"

    for bucket in s3.buckets.all():
        bucket_acl = bucket.Acl()
        for grant in bucket_acl.grants:
            # http://docs.aws.amazon.com/AmazonS3/latest/dev/acl-overview.html
            if grant['Grantee']['Type'].lower() == 'group' \
                    and grant['Grantee']['URI'] == 'http://acs.amazonaws.com/groups/global/AllUsers':
                        x.add_row([bucket.name, grant['Permission'].lower()])
    print(x)

# List S3 bucket's policies
@buckets.command('getbucketpolicy')
@click.option('--getbucketpolicy', default="true", help="List S3 bucket's policies ")
def policy_bucket(getbucketpolicy):

    for bucket in s3.buckets.all():
        try:
            bucket_policy = bucket.Policy()
            print("\nBucket: ",bucket.name, "\nPolicy: ",bucket_policy.policy)

        except botocore.exceptions.ClientError:
            print("\nBucket: ", bucket.name, "\nNo Bucket Policy")
    return

# Retrieve the information whether the bucket is encrypted
@buckets.command('getbucketencryption')
@click.option('--getbucketencryption', default="true", help="Retrieve the information whether the bucket is encrypted")
def policy_bucket(getbucketencryption):
    x = PrettyTable()
    x.field_names = ["S3 Bucket", "Encryption"]
    x.align["S3 Bucket"] = "l"

    for bucket in s3.buckets.all():
        try:
            response = client.get_bucket_encryption(Bucket = bucket.name)
            x.add_row([bucket.name, response['ServerSideEncryptionConfiguration']])

        except botocore.exceptions.ClientError:
            x.add_row([bucket.name, "No Encryption"])

    print(x)

# Retrieve the information whether the bucket have versioning enable
@buckets.command('getbucketversioning')
@click.option('--getbucketversioning', default="true", help="Retrieve the information whether the bucket have versioning enable")
def policy_bucket(getbucketversioning):
    x = PrettyTable()
    x.field_names = ["S3 Bucket", "Versioning", "MFA Delete"]
    x.align["S3 Bucket"] = "l"

    for bucket in s3.buckets.all():
        try:
            bucket_versioning = bucket.Versioning()
            x.add_row([bucket.name, bucket_versioning.status, bucket_versioning.mfa_delete])

        except botocore.exceptions.ClientError:
            x.add_row([bucket.name, "No Bucket Versioning", "No MFA Delete"])

    print(x)

# Retrieve the information whether the bucket have public access block configured
@buckets.command('getpublicaccessblock')
@click.option('--getpublicaccessblock', default="true", help="Retrieve the information whether the bucket have public access block configured")
def policy_bucket(getpublicaccessblock):
    x = PrettyTable()
    x.field_names = ["S3 Bucket", "Public Access Block"]
    x.align["S3 Bucket"] = "l"

    for bucket in s3.buckets.all():
        try:
            response = client.get_public_access_block(Bucket = bucket.name)
            x.add_row([bucket.name, response['PublicAccessBlockConfiguration']])

        except botocore.exceptions.ClientError:
            x.add_row([bucket.name, "False"])

    print(x)

if __name__ == '__main__':
    buckets()