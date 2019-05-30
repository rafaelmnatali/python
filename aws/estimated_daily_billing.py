import boto3
import time
from datetime import date
import datetime


def lambda_handler(event, context):
    
    ########### Getting the Daily Amount spent in AWS ###########
    # opening connection with cost explorer
    billing_client = boto3.client('ce')
    
    # getting dates (yyyy-MM-dd) and converting to string
    today = date.today()
    yesterday = today - datetime.timedelta(days = 1)
    str_today       = str(today)
    str_yesterday   = str(yesterday)
    
    # connecting to cost explorer to get daily aws usage
    response = billing_client.get_cost_and_usage(
    TimePeriod={
        'Start': str_yesterday,
        'End': str_today
    },
    Granularity='DAILY',
    Metrics=[
        'UnblendedCost',
    ]
    )
    
    # iteract through the response to get the daily amount
    for r in response['ResultsByTime']:
        str_amount=(r['Total']['UnblendedCost']['Amount'])
    
    # convert the amount to float
    amount = float(str_amount)
    
    ########### Sending SNS notification if the amount is higher than expected ###########
    
    if amount > your_estimation:
        # Create an SNS client
        sns = boto3.client('sns')
    
        # Publish a warninf message to the specified SNS topic
        response = sns.publish(
            TopicArn='arn:aws:sns:region:account:TopicName',
            Message='Yesterday amount spent was above the threshold!'
        )
