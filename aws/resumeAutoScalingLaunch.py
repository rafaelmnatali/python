import boto3

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
