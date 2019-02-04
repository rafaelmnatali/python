import boto3

def lambda_handler(event, context):

    # opening boto3 to connect to  Aurora Serverless
    client = boto3.client('rds-data')

    # values to be inserted into database
    id = "NULL"
    machine = "machine55"
    BotGr = "105=7"
    date = "2019-02-04 10:03:00"
    RefundTotalVal = "20"
    Refunded = "0"
    RcptSer = "126790"
    Barcode = "970000000100"

    # formating the SQL Stament and transforming in string
    sql_insert=("""insert into `database` (`id`, `machine`,`BotGr`,`date`,`RefundTotalVal`,`Refunded`,`RcptSer`,`Barcode`) values( %s, '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" % (id, machine, BotGr, date, RefundTotalVal, Refunded, RcptSer, Barcode))
    
    response = client.execute_sql(
        awsSecretStoreArn='arn:*',
        database='...',
        dbClusterOrInstanceArn='arn:*',
        sqlStatements=sql_insert
    )

    print(response)
