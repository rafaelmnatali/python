import boto3

def lambda_handler(event, context):
    
    #opening connection with S3
    
    s3 = boto3.resource('s3')
    client = boto3.client('s3')
    
    #listing the contents of the source bucket
    response = client.list_objects(Bucket="centauro-recycling-machine")
    r = len(response['Contents'])
    
    for r in response['Contents']:
        source = (r['Key'])
    
        #copying file to be processed
        copy_temp = {
            'Bucket': 'centauro-recycling-machine',
            'Key': source
        }
                
        s3.meta.client.copy(copy_temp, 'centauro-recycling-machine-temp', source)
        
        #copying file to be archived
        copy_temp = {
            'Bucket': 'centauro-recycling-machine',
            'Key': source
        }
                
        s3.meta.client.copy(copy_temp, 'centauro-recycling-machine-archived', source)
        
        if "PRN" in source:
            #deleting file from source bucket
            remove_source = client.delete_object(
                Bucket= 'centauro-recycling-machine',
                Key= source
                )
