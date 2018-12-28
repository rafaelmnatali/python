import boto3

region = 'us-west-2'

def lambda_handler(event, context):
    as_client = boto3.client('autoscaling')
    
    # Suspend the launch process of the auto scalling to prevent the creation of a new instance
    pause_launch = as_client.suspend_processes(
        AutoScalingGroupName='awseb-e-xux8vrmpez-stack-AWSEBAutoScalingGroup-1LEYITJUGWWSM',
        ScalingProcesses=[
            'Launch',
        ]
    )
    
            # Locate condofacil-dev instance id
    
    ec2 = boto3.client('ec2', region_name=region)
    ec2_describe = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:Name',
                'Values': [
                    'condofacil-dev',
                    ]
            },
        ]
    )
    
    for r in ec2_describe['Reservations']:
        for i in (r['Instances']):
            condo_id=(i['InstanceId'])
    
    ec2.stop_instances(InstanceIds=[condo_id])
    print("stopped your instances: " + str(condo_id))
