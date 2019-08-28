import boto3

region = 'us-west-2'

def lambda_handler(event, context):
    client = boto3.client('ec2')
    
    volumes = client.describe_volumes()
    
    for r in volumes["Volumes"]:
        for v in r['Attachments']:
            instances = client.describe_instances(
                InstanceIds=[v['InstanceId']],
            )
            
            for i in instances['Reservations']:
                for s in (i['Instances']):
                	print(s['PublicDnsName'], s['State'], v['InstanceId'], v['VolumeId'], r['Size'])
