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
        
  #exclude snapshots that are past 7 days
    for d in response['Snapshots']:
        d1=(d['StartTime'])
        now = datetime.now()
        #remove time zone info from snapshot
        snapshot_time = d1.replace(tzinfo=None)
        
        #number of days
        n=7
        date_n_days_ago = datetime.now() - timedelta(days=n)
        #print(snapshot_time,date_n_days_ago)
        
        #difference between snapshot and 7 days ago 
        delta=snapshot_time-date_n_days_ago
        
        #convert to string to iterate
        str_delta=str(delta)
        if "-1 day" in str_delta:
            print("Removing snapshot: {} from: {}".format(d['SnapshotId'], snapshot_time))
            ec2_client.delete_snapshot(SnapshotId=d['SnapshotId'])
