import boto3
# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g., 'us-east-1'
region = 'us-west-2'

def lambda_handler(event, context):
	
	# locate the InstanceId for al EC2 in the region with tag Restart:yes

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
    
    # stop all the instances located previously
    for r in ec2_describe['Reservations']:
        for i in (r['Instances']):
            instances_id=(i['InstanceId'])
            ec2.stop_instances(InstanceIds=[instances_id])
            print("stopped your instances: " + str(instances_id))