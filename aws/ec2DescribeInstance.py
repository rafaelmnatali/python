import boto3

ec2 = boto3.client('ec2')

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

for r in response['Reservations']:
	for i in (r['Instances']):
		print(i['InstanceId'])

