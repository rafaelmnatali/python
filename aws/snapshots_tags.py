import boto3

def lambda_handler(event, context):

    #open ec2 client connection (snapshot-id)
    ec2_client = boto3.client('ec2')
    
    #filter snapshot by EBS volume-id
    response = ec2_client.describe_snapshots(
        Filters=[
            {
                'Name': 'volume-id',
                'Values': [ 'xxxxxxxxxxxx' ] 
            }
        ],
    )
    
    #get the snapshot id
    
    for s in response['Snapshots']:
        snap_id=(s['SnapshotId'])
        ec2_client.create_tags(Resources=[snap_id], Tags=[
            {'Key':'Team', 'Value': 'xxxxxx'}, 
            {'Key':'Name', 'Value': 'xxxxxx'},
            {'Key':'Project', 'Value': 'xxxxxxx'},
            {'Key':'Environment', 'Value': 'xxxxxx'}])
