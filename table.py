
# Data Generating Script - fractal_data_julia
# Author - Julia You- 2018

## PREREQS
##          configured AWS tools
##          installed python3.5
##          installed boto3 (pip install boto3)
##          Installed tqdm module
##          'juliayou' AWS configuration profile - with admin rights
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='fractal_data_julia',
    KeySchema=[
        {
            'AttributeName': 'SN',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'TS',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'SN',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'TS',
            'AttributeType': 'S'
        },

    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
print("table is creating......")
table.meta.client.get_waiter('table_exists').wait(TableName='fractal_data_julia')

# Add new items to the table
table.put_item(
   Item= {"SN":"1",
          "TS" : "2018/01/25 03:00",
          "payload":{
                      "ChaSt": "Charging",
                      "DERTyp":"ESS",
                      "Evt":"00111",
                      "Hz":"60",
                      "KWAC":"4888"
                     }

        }
)

# Print out some data about the table.
print(table.item_count)
