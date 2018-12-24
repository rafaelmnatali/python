import boto3
# Enter the region your instances are in. Include only the region without specifying Availability Zone; e.g., 'us-east-1'
region = 'us-west-2'
# Enter your instances here: ex. ['X-XXXXXXXX', 'X-XXXXXXXX']
instances = ['i-0d569c453dffcb893', 'i-053cc5bd3a42cce01', 'i-0f3b463d668c243f1', 'i-0462669ebc9cb233b', 'i-070332008f2812516']

def lambda_handler(event, context):
    ec2 = boto3.client('ec2', region_name=region)
    ec2.stop_instances(InstanceIds=instances)
    print 'stopped your instances: ' + str(instances)