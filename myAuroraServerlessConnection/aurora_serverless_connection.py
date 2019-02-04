import boto3

def lambda_handler(event, context):
    
    client = boto3.client('rds-data')
    
    response = client.execute_sql(
        awsSecretStoreArn='arn:*',
        database='database',
        dbClusterOrInstanceArn='arn:*',
        sqlStatements='select * from table'
    )