#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy of this
# software and associated documentation files (the "Software"), to deal in the Software
# without restriction, including without limitation the rights to use, copy, modify,
# merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Cost Explorer Report

A script, for local or lambda use, to generate CostExplorer excel graphs

"""

from __future__ import print_function

__author__ = "David Faulkner"
__version__ = "0.1.2"
__license__ = "MIT No Attribution"

import os
import sys
# Required to load modules from vendored subfolder (for clean development env)
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vendored"))

import boto3
import datetime
import logging
import pandas as pd
#For date
from dateutil.relativedelta import relativedelta
#For email
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import COMMASPACE, formatdate

#GLOBALS
SES_REGION = os.environ.get('SES_REGION')
if not SES_REGION:
    SES_REGION="us-east-1"
ACCOUNT_LABEL = os.environ.get('ACCOUNT_LABEL')
if not ACCOUNT_LABEL:
    ACCOUNT_LABEL = 'Email'
    
CURRENT_MONTH = os.environ.get('CURRENT_MONTH')
if CURRENT_MONTH == "true":
    CURRENT_MONTH = True
else:
    CURRENT_MONTH = False

#Default exclude support, as for Enterprise Support
#as support billing is finalised later in month so skews trends    
INC_SUPPORT = os.environ.get('INC_SUPPORT')
if INC_SUPPORT == "true":
    INC_SUPPORT = True
else:
    INC_SUPPORT = False

class CostExplorer:
    """Retrieves BillingInfo checks from CostExplorer API
    >>> costexplorer = CostExplorer()
    >>> costexplorer.addReport(GroupBy=[{"Type": "DIMENSION","Key": "SERVICE"}])
    >>> costexplorer.generateExcel()
    """    
    def __init__(self, CurrentMonth=False):
        #Array of reports ready to be output to Excel.
        self.reports = []
        self.client = boto3.client('ce', region_name='us-east-1')
        self.end = datetime.date.today().replace(day=1)
        self.riend = datetime.date.today()
        if CurrentMonth or CURRENT_MONTH:
            self.end = self.riend
        #self.start = (datetime.date.today() - relativedelta(months=+12)).replace(day=1) #1st day of month 12 months ago
        self.start = (datetime.date.today() - relativedelta(months=+1)).replace(day=1) #1st day of month 12 months ago
        self.ristart = (datetime.date.today() - relativedelta(months=+11)).replace(day=1) #1st day of month 11 months ago
        self.sixmonth = (datetime.date.today() - relativedelta(months=+6)).replace(day=1) #1st day of month 6 months ago, so RI util has savings values
        try:
            self.accounts = self.getAccounts()
        except:
            logging.exception("Getting Account names failed")
            self.accounts = {}
        
    def getAccounts(self):
        accounts = {}
        client = boto3.client('organizations', region_name='us-east-1')
        paginator = client.get_paginator('list_accounts')
        response_iterator = paginator.paginate()
        for response in response_iterator:
            for acc in response['Accounts']:
                accounts[acc['Id']] = acc
        return accounts
            
    def addReport(self, Name="Default",GroupBy=[{"Type": "DIMENSION","Key": "SERVICE"},], 
    Style='Total', NoCredits=True, CreditsOnly=False, RefundOnly=False, UpfrontOnly=False, IncSupport=False):
        type = 'chart' #other option table
        results = []
        if not NoCredits:
            response = self.client.get_cost_and_usage(
                TimePeriod={
                    'Start': self.start.isoformat(),
                    'End': self.end.isoformat()
                },
                Granularity='MONTHLY',
                Metrics=[
                    'UnblendedCost',
                ],
                GroupBy=GroupBy
            )
        else:
            Filter={"Not": {"Dimensions": {"Key": "RECORD_TYPE","Values": ["Credit", "Refund", "Upfront", "Support"]}}}
            if INC_SUPPORT or IncSupport: #If global set for including support, we dont exclude it
                Filter={"Not": {"Dimensions": {"Key": "RECORD_TYPE","Values": ["Credit", "Refund", "Upfront"]}}}
            if CreditsOnly:
                Filter={"Dimensions": {"Key": "RECORD_TYPE","Values": ["Credit",]}}
            if RefundOnly:
                Filter={"Dimensions": {"Key": "RECORD_TYPE","Values": ["Refund",]}}
            if UpfrontOnly:
                Filter={"Dimensions": {"Key": "RECORD_TYPE","Values": ["Upfront",]}}
            response = self.client.get_cost_and_usage(
                TimePeriod={
                    'Start': self.start.isoformat(),
                    'End': self.end.isoformat()
                },
                Granularity='MONTHLY',
                Metrics=[
                    'UnblendedCost',
                ],
                GroupBy=GroupBy,
                Filter=Filter
            )

        if response:
            results.extend(response['ResultsByTime'])
            
            while 'nextToken' in response:
                nextToken = response['nextToken']
                response = self.client.get_cost_and_usage(
                    TimePeriod={
                        'Start': self.start.isoformat(),
                        'End': self.end.isoformat()
                    },
                    Granularity='MONTHLY',
                    Metrics=[
                        'UnblendedCost',
                    ],
                    GroupBy=GroupBy,
                    NextPageToken=nextToken
                )
                results.extend(response['ResultsByTime'])
                if 'nextToken' in response:
                    nextToken = response['nextToken']
                else:
                    nextToken = False
        rows = []
        sort = ''
        for v in results:
            row = {'date':v['TimePeriod']['Start']}
            sort = v['TimePeriod']['Start']
            for i in v['Groups']:
                key = i['Keys'][0]
                if key in self.accounts:
                    key = self.accounts[key][ACCOUNT_LABEL]
                row.update({key:float(i['Metrics']['UnblendedCost']['Amount'])}) 
            if not v['Groups']:
                row.update({'Total':float(v['Total']['UnblendedCost']['Amount'])})
            rows.append(row)  

        df = pd.DataFrame(rows)
        df.set_index("date", inplace= True)
        df = df.fillna(0.0)
        
        if Style == 'Forecast':
            dfc = df.copy()
            lastindex = None
            for index, row in df.iterrows():
                if lastindex:
                    for i in row.index:
                        try:
                            #df.at[index,i] = dfc.at[index,i] - dfc.at[lastindex,i]
                            current_month = dfc.at[index,i]
                            today = datetime.date.today()
                            current_day = today.day
                            month_days = 31
                            
                            df.at[index,i] = ((current_month/current_day)*month_days)
                        except:
                            logging.exception("Error")
                            df.at[index,i] = 0
                lastindex = index
        df = df.T
        df = df.sort_values(sort, ascending=False)
        self.reports.append({'Name':Name,'Data':df, 'Type':type})
        
        
    def generateExcel(self):
        # Create a Pandas Excel writer using XlsxWriter as the engine.\
        os.chdir('/tmp')
        now = datetime.datetime.now()
        str_now = str(now)
        filename = str_now + '-weekly-cost_explorer_report.xlsx'
        #writer = pd.ExcelWriter('cost_explorer_report.xlsx', engine='xlsxwriter')
        writer = pd.ExcelWriter(filename, engine='xlsxwriter')
        workbook = writer.book
        for report in self.reports:
            print(report['Name'],report['Type'])
            report['Data'].to_excel(writer, sheet_name=report['Name'])
            worksheet = writer.sheets[report['Name']]
            if report['Type'] == 'chart':
                
                # Create a chart object.
                chart = workbook.add_chart({'type': 'column', 'subtype': 'stacked'})
                
                
                chartend=1
                if CURRENT_MONTH:
                    chartend=2
                for row_num in range(1, len(report['Data']) + 1):
                    chart.add_series({
                        'name':       [report['Name'], row_num, 0],
                        'categories': [report['Name'], 0, 1, 0, chartend],
                        'values':     [report['Name'], row_num, 1, row_num, chartend],
                    })
                chart.set_y_axis({'label_position': 'low'})
                chart.set_x_axis({'label_position': 'low'})
                worksheet.insert_chart('O2', chart, {'x_scale': 2.0, 'y_scale': 2.0})
        writer.save()
        
        #Time to deliver the file to S3
        if os.environ.get('S3_BUCKET'):
            s3 = boto3.client('s3')
            #s3.upload_file("cost_explorer_report.xlsx", os.environ.get('S3_BUCKET'), "cost_explorer_report.xlsx")
            s3.upload_file(filename, os.environ.get('S3_BUCKET'), filename)
        if os.environ.get('SES_SEND'):
            #Email logic
            msg = MIMEMultipart()
            msg['From'] = os.environ.get('SES_FROM')
            msg['To'] = COMMASPACE.join(os.environ.get('SES_SEND').split(","))
            msg['Date'] = formatdate(localtime=True)
            msg['Subject'] = "Cost Explorer Report"
            text = "Find your Cost Explorer report attached\n\n"
            msg.attach(MIMEText(text))
            #with open("cost_explorer_report.xlsx", "rb") as fil:
            with open(filename, "rb") as fil:
                part = MIMEApplication(
                    fil.read(),
                    #Name="cost_explorer_report.xlsx"
                    Name=filename
                )
            #part['Content-Disposition'] = 'attachment; filename="%s"' % "cost_explorer_report.xlsx"
            part['Content-Disposition'] = 'attachment; filename="%s"' % filename
            msg.attach(part)
            #SES Sending
            ses = boto3.client('ses', region_name=SES_REGION)
            result = ses.send_raw_email(
                Source=msg['From'],
                Destinations=os.environ.get('SES_SEND').split(","),
                RawMessage={'Data': msg.as_string()}
            )     


def main_handler(event=None, context=None): 
    costexplorer = CostExplorer(CurrentMonth=False)
    #Default addReport has filter to remove Support / Credits / Refunds / UpfrontRI
    #Overall Billing Reports
    costexplorer.addReport(Name="Total", GroupBy=[],Style='Total',IncSupport=True)
    costexplorer.addReport(Name="TotalForecast", GroupBy=[],Style='Forecast')
    costexplorer.addReport(Name="TotalInclCredits", GroupBy=[],Style='Total',NoCredits=False,IncSupport=True)
    costexplorer.addReport(Name="TotalInclCreditsForecast", GroupBy=[],Style='Forecast',NoCredits=False)
    costexplorer.addReport(Name="Credits", GroupBy=[],Style='Total',CreditsOnly=True)
    costexplorer.addReport(Name="Refunds", GroupBy=[],Style='Total',RefundOnly=True)
    #GroupBy Reports
    costexplorer.addReport(Name="Services", GroupBy=[{"Type": "DIMENSION","Key": "SERVICE"}],Style='Total',IncSupport=True)
    costexplorer.addReport(Name="ServicesForecast", GroupBy=[{"Type": "DIMENSION","Key": "SERVICE"}],Style='Forecast')
    costexplorer.addReport(Name="UsageType", GroupBy=[{"Type": "DIMENSION","Key": "USAGE_TYPE"}],Style='Total',IncSupport=True)
    costexplorer.addReport(Name="UsageTypeForecast", GroupBy=[{"Type": "DIMENSION","Key": "USAGE_TYPE"}],Style='Forecast')
    costexplorer.addReport(Name="Accounts", GroupBy=[{"Type": "DIMENSION","Key": "LINKED_ACCOUNT"}],Style='Total')
    costexplorer.addReport(Name="AccountsForecast", GroupBy=[{"Type": "DIMENSION","Key": "LINKED_ACCOUNT"}],Style='Forecast')
    costexplorer.addReport(Name="Regions", GroupBy=[{"Type": "DIMENSION","Key": "REGION"}],Style='Total')
    costexplorer.addReport(Name="RegionsForecast", GroupBy=[{"Type": "DIMENSION","Key": "REGION"}],Style='Forecast')
    if os.environ.get('COST_TAGS'): #Support for multiple/different Cost Allocation tags
        for tagkey in os.environ.get('COST_TAGS').split(','):
            tabname = tagkey.replace(":",".") #Remove special chars from Excel tabname
            costexplorer.addReport(Name="{}".format(tabname)[:31], GroupBy=[{"Type": "TAG","Key": tagkey}],Style='Total')
            costexplorer.addReport(Name="Forecast-{}".format(tabname)[:31], GroupBy=[{"Type": "TAG","Key": tagkey}],Style='Forecast')
    costexplorer.generateExcel()
    return "Report Generated"

if __name__ == '__main__':
    main_handler()
