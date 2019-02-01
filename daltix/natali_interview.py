import ndjson
import csv
from urllib.request import urlopen
import datetime

print("Step 1 - Loading data from origin")

urls=['https://s3-eu-west-1.amazonaws.com/daltix-public-interviews/data-engineering-challenge/raw/transformer-output-cust-2-2018-11-05-03-14-06-99f22c24-54d6-4dcc-a234-ae860ab971c2','https://s3-eu-west-1.amazonaws.com/daltix-public-interviews/data-engineering-challenge/raw/transformer-output-cust-2-2018-11-05-03-24-06-0a166cb1-5677-4cc8-8465-534ebcf480f9','https://s3-eu-west-1.amazonaws.com/daltix-public-interviews/data-engineering-challenge/raw/transformer-output-cust-2-2018-11-05-03-44-09-2071370f-76fa-4c62-95ee-2b2b8e37b5ee','https://s3-eu-west-1.amazonaws.com/daltix-public-interviews/data-engineering-challenge/raw/transformer-output-cust-2-2018-11-06-03-09-23-b57f2bce-ecf2-4b99-a609-15fe0949c571','https://s3-eu-west-1.amazonaws.com/daltix-public-interviews/data-engineering-challenge/raw/transformer-output-cust-2-2018-11-06-03-19-24-47304deb-7353-4074-b129-bc90e9bde404','https://s3-eu-west-1.amazonaws.com/daltix-public-interviews/data-engineering-challenge/raw/transformer-output-cust-2-2018-11-06-03-29-25-48777a72-a8ef-4887-83ee-459e1135f548','https://s3-eu-west-1.amazonaws.com/daltix-public-interviews/data-engineering-challenge/raw/transformer-output-cust-2-2018-11-07-03-02-33-03035a6b-3bed-421c-9912-d5508fb31002','https://s3-eu-west-1.amazonaws.com/daltix-public-interviews/data-engineering-challenge/raw/transformer-output-cust-2-2018-11-07-03-12-36-1c80014a-b77e-4389-a9c7-f8e42f27601d','https://s3-eu-west-1.amazonaws.com/daltix-public-interviews/data-engineering-challenge/raw/transformer-output-cust-2-2018-11-08-03-08-31-db10954e-a0f3-40a1-affa-53847f1a8275','https://s3-eu-west-1.amazonaws.com/daltix-public-interviews/data-engineering-challenge/raw/transformer-output-cust-2-2018-11-08-03-18-32-bbe1651e-c158-4659-9d9d-cfcc4754d0ec','https://s3-eu-west-1.amazonaws.com/daltix-public-interviews/data-engineering-challenge/raw/transformer-output-cust-2-2018-11-08-03-28-35-be758895-b6bb-4c1d-9ee7-7072dbe4adbf']

print("Step 2 - Creating CSV files")
#amazon shop file
outputFile_amazon = open("Shop_amazon_ConvertedJSON.csv","w", encoding='utf-8')
outputWriter_amazon = csv.writer(outputFile_amazon)

#amazonde shop file
outputFile_amazonde = open("Shop_amazonde_ConvertedJSON.csv","w", encoding='utf-8')
outputWriter_amazonde = csv.writer(outputFile_amazonde)

#bol shop file
outputFile_bol = open("Shop_bol_ConvertedJSON.csv","w", encoding='utf-8')
outputWriter_bol = csv.writer(outputFile_bol)

#fundoo shop file
outputFile_fundoo = open("Shop_fundoo_ConvertedJSON.csv","w", encoding='utf-8')
outputWriter_fundoo = csv.writer(outputFile_fundoo)

print("Step 3 - Loading data into CSV file")
for u in urls:
    with urlopen(u) as shop:
        data = ndjson.load(shop)

    for d in data:
        row_array = []
        for attributes in d['products']:
            if attributes['shop'] == 'amazonde':
                row_array.append(attributes['shop'])
                row_array.append(attributes['location'])
                row_array.append(attributes['country'])
                row_array.append(attributes['id'])

                # convert downloaded_on time from epoch to human readable
                epoch_time = attributes['downloaded_on']
                time = datetime.datetime.fromtimestamp(epoch_time).strftime('%c')
                row_array.append(time)

                # if product doesn't have eans and/or categories include blank column
                try:
                    row_array.append(attributes['eans'])
                    row_array.append(attributes['categories'])
                except KeyError:
                    row_array.append("")
                    row_array.append("")

                # if product doesn't have one of the pricing information include blank column
                try:
                    for p in attributes['pricing']:
                        for unit in p['prices']:
                            row_array.append(unit['regular'])
                            row_array.append(unit['promo'])
                            row_array.append(unit['unit'])
                except KeyError:
                    row_array.append("")
                    row_array.append("")
                    row_array.append("")

                outputWriter_amazonde.writerow(row_array)

            elif attributes['shop'] == 'amazon':
                row_array.append(attributes['shop'])
                row_array.append(attributes['location'])
                row_array.append(attributes['country'])
                row_array.append(attributes['id'])

                # convert downloaded_on time from epoch to human readable
                epoch_time = attributes['downloaded_on']
                time = datetime.datetime.fromtimestamp(epoch_time).strftime('%c')
                row_array.append(time)

                # if product doesn't have eans and/or categories include blank column
                try:
                    row_array.append(attributes['eans'])
                    row_array.append(attributes['categories'])
                except KeyError:
                    row_array.append("")
                    row_array.append("")

                # if product doesn't have one of the pricing information include blank column
                try:
                    for p in attributes['pricing']:
                        for unit in p['prices']:
                            row_array.append(unit['regular'])
                            row_array.append(unit['promo'])
                            row_array.append(unit['unit'])
                except KeyError:
                    row_array.append("")
                    row_array.append("")
                    row_array.append("")

                outputWriter_amazon.writerow(row_array)

            elif attributes['shop'] == "bol":
                row_array.append(attributes['shop'])
                row_array.append(attributes['location'])
                row_array.append(attributes['country'])
                row_array.append(attributes['id'])

                # convert downloaded_on time from epoch to human readable
                epoch_time = attributes['downloaded_on']
                time = datetime.datetime.fromtimestamp(epoch_time).strftime('%c')
                row_array.append(time)

                # if product doesn't have eans and/or categories include blank column
                try:
                    row_array.append(attributes['eans'])
                    row_array.append(attributes['categories'])
                except KeyError:
                    row_array.append("")
                    row_array.append("")

                # if product doesn't have one of the pricing information include blank column
                try:
                    for p in attributes['pricing']:
                        for unit in p['prices']:
                            row_array.append(unit['regular'])
                            row_array.append(unit['promo'])
                            row_array.append(unit['unit'])
                except KeyError:
                    row_array.append("")
                    row_array.append("")
                    row_array.append("")

                outputWriter_bol.writerow(row_array)

            elif attributes['shop'] == "fundoo":
                row_array.append(attributes['shop'])
                row_array.append(attributes['location'])
                row_array.append(attributes['country'])
                row_array.append(attributes['id'])

                # convert downloaded_on time from epoch to human readable
                epoch_time = attributes['downloaded_on']
                time = datetime.datetime.fromtimestamp(epoch_time).strftime('%c')
                row_array.append(time)

                # if product doesn't have eans and/or categories include blank column
                try:
                    row_array.append(attributes['eans'])
                    row_array.append(attributes['categories'])
                except KeyError:
                    row_array.append("")
                    row_array.append("")

                # if product doesn't have one of the pricing information include blank column
                try:
                    for p in attributes['pricing']:
                        for unit in p['prices']:
                            row_array.append(unit['regular'])
                            row_array.append(unit['promo'])
                            row_array.append(unit['unit'])
                except KeyError:
                    row_array.append("")
                    row_array.append("")
                    row_array.append("")


                outputWriter_fundoo.writerow(row_array)

print("Step 4 - CSV files created!")

# closing CSV files
outputFile_amazon.close()
outputFile_amazonde.close()
outputFile_bol.close()
outputFile_fundoo.close()
