import boto3
from prettytable import PrettyTable

x = PrettyTable()
x.field_names = ["Repository", "URL"]
x.align = "l"

client = boto3.client('codecommit')

response = client.list_repositories()

r = len((response['repositories']))

for r in response['repositories']:
    name = (r['repositoryName'])
    response_batch = client.batch_get_repositories(repositoryNames=[name])
    for u in response_batch['repositories']:
        x.add_row([u['repositoryName'], u['cloneUrlHttp']])

print(x)




