import boto3
import botocore

s3 = boto3.resource('s3')

for bucket in s3.buckets.all():
 	try:
 		bucket_acl  	= s3.BucketAcl(bucket.name)
# 		bucket_policy  	= s3.BucketPolicy(bucket.name)

 		print("Bucket:", bucket.name, "ACL: ", bucket_acl.load())#, "Policies:", bucket_policy.load())

 	except botocore.exceptions.ClientError as error:
 		pass


