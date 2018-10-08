
# put item into dynamodb table --fractal_data_julia
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

table = dynamodb.Table('fractal_data_julia')

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

table.put_item(
   Item= {"SN":"1",
          "TS" : "2018/01/25 06:00",
          "payload":{
                      "ChaSt": "Charging",
                      "DERTyp":"ESS",
                      "Evt":"00111",
                      "Hz":"60",
                      "KWAC":"4888"
                     }

        }
)
