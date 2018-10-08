
# get a specific item from dynamodb --fractal_data_julia
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('fractal_data_julia')



# get an item from the dynamodb
response = table.get_item(
    Key={
        'SN': '1',
        'TS': '2018/01/25 03:00'
    }
)
item = response['Item']
print(item)
