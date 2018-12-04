import boto3
import click
import botocore
from prettytable import PrettyTable

# Retrieve s3 information
s3 = boto3.resource('s3')
client = boto3.client('s3')

@click.group()
def buckets():
    """Commands for S3 security check"""


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


@buckets.command('getpublicacl')
@click.option('--getpublicacl', default="true", help="List S3 bucket's with Public Access enabled")
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

@buckets.command('getbucketpolicy')
@click.option('--getbucketpolicy', default="true", help="List S3 bucket's with Policies enabled")
def policy_bucket(getbucketpolicy):

    for bucket in s3.buckets.all():
        try:
            bucket_policy = bucket.Policy()
            print("\nBucket: ",bucket.name, "\nPolicy: ",bucket_policy.policy)

        except botocore.exceptions.ClientError:
            print("\nBucket: ", bucket.name, "\nNo Bucket Policy")
    return

@buckets.command('getbucketencryption')
@click.option('--getbucketencryption', default="true", help="List S3 bucket's with Encryption enabled")
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

@buckets.command('getbucketversioning')
@click.option('--getbucketversioning', default="true", help="List S3 bucket's with Versioning enabled")
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

@buckets.command('getpublicaccessblock')
@click.option('--getpublicaccessblock', default="true", help="List S3 bucket's with Encryption enabled")
def policy_bucket(getpublicaccessblock):
    x = PrettyTable()
    x.field_names = ["S3 Bucket", "BlockPublicAcls"] #, "IgnorePublicAcls", "BlockPublicPolicy", "RestrictPublicBuckets"]
    x.align["S3 Bucket"] = "l"

    for bucket in s3.buckets.all():
        try:
            response = client.get_public_access_block(Bucket = bucket.name)
            x.add_row([bucket.name, "True"])

        except botocore.exceptions.ClientError:
            x.add_row([bucket.name, "False"])

    print(x)

if __name__ == '__main__':
    buckets()