import boto3
import click
from prettytable import PrettyTable


# Retrieve s3 information
s3 = boto3.resource('s3')

@click.group()
def buckets():
	"""Command for S3"""

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


@buckets.command('getacl')
@click.option('--getacl', default="true", help="List S3 bucket's ACL information")

def acl_bucket(getacl):
	x = PrettyTable()
	x.field_names = ["S3 Bucket", "ACL"]

	for bucket in s3.buckets.all():
		bucket_acl = s3.BucketAcl(bucket.name)
	#	print("Bucket:", bucket.name, "| ACL: ", bucket_acl.load())
		x.add_row([bucket.name,bucket_acl.load])
	print(x)
	return
    

if __name__ == '__main__':
	buckets()
