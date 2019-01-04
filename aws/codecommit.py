import boto3
from prettytable import PrettyTable

# create a table to print the information
x = PrettyTable()
x.field_names = ["Repository", "URL"]
x.align = "l"

# low-level client representing CodeCommit
client = boto3.client('codecommit')

# list all the repositories
response = client.list_repositories()

# count the total number of repositories
r = len((response['repositories']))

# iteract through all the repositories to collect Name and URL
for r in response['repositories']:
    name = (r['repositoryName'])
    response_batch = client.batch_get_repositories(repositoryNames=[name])
    for u in response_batch['repositories']:
        x.add_row([u['repositoryName'], u['cloneUrlHttp']])

# print the table with repositories Name and URL
print(x)




