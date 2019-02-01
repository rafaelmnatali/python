import urllib.request
import csv
import boto3

#creating CSV files
outputFile_receipt = open("machine_receipt.csv","w", encoding='utf-8')
outputWriter_receipt = csv.writer(outputFile_receipt)

#opening connection with S3

s3 = boto3.resource('s3')
client = boto3.client('s3')

#listing the contents of the bucket
response = client.list_objects(Bucket="centauro-recycling-machine-processing")
r = len(response['Contents'])

for r in response['Contents']:
    receipt = (r['Key'])
    try:
        #formating the URL with the filename
        with urllib.request.urlopen("https://s3-us-west-2.amazonaws.com/centauro-recycling-machine-processing/{0}".format(receipt)) as receipt_file:
            data = (receipt_file.read(1024).decode('utf-8'))
    except urllib.error.HTTPError:
        pass

    # spliting the receipt in a list
    mylist_data = data.splitlines()

    #index to iteract with the list
    i = -1
    for a in mylist_data:

        i += 1

        #locate the [RefVal] entry in the receipt to know the quantity of bottles
        if mylist_data[i] == "[RefVal]":
            refval = i

            #if RefVal's index is 2 it means there's only 1 bottle
            if i == 2:
                row_array=[]
                b = mylist_data[1:i]
                s = str(b)
                #machine name from S3
                row_array.append(r['Key'][0:8]) 
                #bootle identification from receipt [BotGr]
                row_array.append(''.join(c for c in s if c in '0123456789= '))
                #date of the receipt from S3
                date=r['LastModified']
                date_str=str(date)
                row_array.append(date_str[0:19])

                z = -1

                for w in mylist_data:
                    
                    #index to iteract with the list
                    z += 1

                    #receipt number
                    if "RcptSer" in mylist_data[z]:
                        s = mylist_data[z]
                        row_array.append(''.join(c for c in s if c in '0123456789'))

                    #number of bottles refunded
                    if "Refunded" in mylist_data[z]:
                        s = mylist_data[z]
                        row_array.append(''.join(c for c in s if c in '0123456789'))   

                    #total value for the refunded bottles
                    if "RefundTotalVal" in mylist_data[z]:
                        s = mylist_data[z]
                        row_array.append(''.join(c for c in s if c in '0123456789'))

                    #barcode of the receipt
                    if "Barcode1" in mylist_data[z]:
                        s = mylist_data[z]
                        row_array.append(s[9::])
                        outputWriter_receipt.writerow(row_array)

            else:

                #creating x and y to get the position of each bottle; from last to first
                x = i

                while x > 1:

                    y = x-1
                    
                    #index to iteract with the list
                    z = -1

                    row_array_2=[]
                    b = mylist_data[y:x]
                    s = str(b)
                    #machine name from S3
                    row_array_2.append(r['Key'][0:8]) 
                    #bootle identification from receipt [BotGr]
                    row_array_2.append(''.join(c for c in s if c in '0123456789= '))  
                    #date of the receipt from S3
                    date=r['LastModified']
                    date_str=str(date)
                    row_array_2.append(date_str[0:19])
                    
                    #iteract through the receipt to get the information for each bottle in a new line
                    for w in mylist_data:
                        z += 1

                        #receipt number
                        if "RcptSer" in mylist_data[z]:
                            s = mylist_data[z]
                            row_array_2.append(''.join(c for c in s if c in '0123456789'))
                        
                        #number of bottles refunded    
                        if "Refunded" in mylist_data[z]:
                            s = mylist_data[z]
                            row_array_2.append(''.join(c for c in s if c in '0123456789'))   

                        #total value for the refunded bottles
                        if "RefundTotalVal" in mylist_data[z]:
                            s = mylist_data[z]
                            row_array_2.append(''.join(c for c in s if c in '0123456789'))

                        #barcode of the receipt
                        if "Barcode1" in mylist_data[z]:
                            s = mylist_data[z]
                            row_array_2.append(s[9::])
                            outputWriter_receipt.writerow(row_array_2)
                            x = x - 1
                            y = y - 1

outputFile_receipt.close()