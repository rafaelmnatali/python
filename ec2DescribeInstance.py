import boto3

# low-level client representing Amazon Elastic Compute Cloud (EC2)
ec2 = boto3.client('ec2')

# filter EC2 instances by tag NAME 
response = ec2.describe_instances(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                'condofacil-dev',
            ]
        },
    ]
)

# Print the InstanceId for the EC2 that matchs the filter
for r in response['Reservations']:
	for i in (r['Instances']):
		print(i['InstanceId'])

