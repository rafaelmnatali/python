import boto3
import botocore
import click

@click.command()
@click.option("--acl", help="select TRUE to list ACL for all buckets")

def acl(acl):
	if acl == "TRUE":
		s3 = boto3.resource('s3')
		for bucket in s3.buckets.all():
			try:
				bucket_acl = s3.BucketAcl(bucket.name)
				print("Bucket:", bucket.name, ", ACL: ", bucket_acl.load())
			except botocore.exceptions.ClientError as error:
				pass

if __name__ == '__main__':
	acl()