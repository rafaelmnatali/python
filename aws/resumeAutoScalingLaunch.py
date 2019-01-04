import boto3

# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g., 'us-east-1'
region = 'us-west-2'

def lambda_handler(event, context):
    as_client = boto3.client('autoscaling')
    
    # Suspend the launch process of the auto scalling to prevent the creation of a new instance
    resume_launch = as_client.resume_processes(
        AutoScalingGroupName='awseb-e-xux8vrmpez-stack-AWSEBAutoScalingGroup-1LEYITJUGWWSM',
        ScalingProcesses=[
            'Launch',
        ]
    )
