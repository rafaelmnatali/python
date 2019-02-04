import boto3

def lambda_handler(event, context):
    
    client = boto3.client('rds-data')
    
    response = client.execute_sql(
        awsSecretStoreArn='arn:aws:secretsmanager:us-east-1:191127002560:secret:rds-db-credentials/cluster-SSCOGL2YAGCYHKO4NWUMFDNZ7E/recyclingdba-tQT9Wv',
        database='recycling',
        dbClusterOrInstanceArn='arn:aws:rds:us-east-1:191127002560:cluster:recycling',
        sqlStatements='select * from receipt'
    )