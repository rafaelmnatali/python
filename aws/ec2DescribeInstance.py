import boto3

# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g., 'us-east-1'
region = 'us-west-2'

ec2 = boto3.client('ec2', region_name=region)
ec2_describe = ec2.describe_instances(
    Filters=[
        {
            'Name': 'tag:Restart',
            'Values': [
                'yes',
            ]
        },
    ]
)

for r in ec2_describe['Reservations']:
    for i in (r['Instances']):
        instances_id = (i['InstanceId'])
        print(instances_id)
