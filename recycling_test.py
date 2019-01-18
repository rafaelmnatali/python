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
response = client.list_objects(Bucket="centauro-recycling-machine")
r = len(response['Contents'])

for r in response['Contents']:
    receipt = (r['Key'])
    try:
        #formating the URL with the filename
        with urllib.request.urlopen("https://s3-us-west-2.amazonaws.com/centauro-recycling-machine/{0}".format(receipt)) as receipt_file:
            data = (receipt_file.read(300).decode('utf-8'))
    except urllib.error.HTTPError:
        pass

    # spliting the receipt in a list
    mylist_data = data.splitlines()

    #printing bottles recycled
    #i=5
    #print(mylist_data[1:i])



    row_array=[]

    i = -1
    for a in mylist_data:

        i += 1

        if mylist_data[i] == "[RefVal]":
            refval = i

            if i == 2:
                b = mylist_data[1:i]
                s = str(b)
                row_array.append(r['Key'][0:8]) 
                row_array.append(''.join(c for c in s if c in '0123456789= '))
                row_array.append(r['LastModified'])

                z = -1

                for w in mylist_data:
                    z += 1

                    if "RcptSer" in mylist_data[z]:
                        s = mylist_data[z]
                        row_array.append(''.join(c for c in s if c in '0123456789'))
                        outputWriter_receipt.writerow(row_array)
                   
            else:

                z = -1

                row_array_2=[]
                b = mylist_data[2:3]
                s = str(b)
                row_array_2.append(r['Key'][0:8]) 
                row_array_2.append(''.join(c for c in s if c in '0123456789= '))  
                row_array_2.append(r['LastModified'])
                #outputWriter_receipt.writerow(row_array_2)

                for w in mylist_data:
                    z += 1

                    if "RcptSer" in mylist_data[z]:
                        s = mylist_data[z]
                        row_array_2.append(''.join(c for c in s if c in '0123456789'))
                        outputWriter_receipt.writerow(row_array_2)

                row_array_3=[]
                b = mylist_data[1:2]
                s = str(b)
                row_array_3.append(r['Key'][0:8]) 
                row_array_3.append(''.join(c for c in s if c in '0123456789= '))  
                row_array_3.append(r['LastModified'])
                #outputWriter_receipt.writerow(row_array_3)

                z = -1

                for w in mylist_data:
                    z += 1

                    if "RcptSer" in mylist_data[z]:
                        s = mylist_data[z]
                        row_array_3.append(''.join(c for c in s if c in '0123456789'))
                        outputWriter_receipt.writerow(row_array_3)
                



    #outputWriter_receipt.writerow(row_array)


outputFile_receipt.close()
