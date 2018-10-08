import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("Fractal_Site")

response = table.query(
              Limit = 5,
              ScanIndexForward = False,
              KeyConditionExpression=Key('SN').eq("4140002")
           )
print(response)
