#query record from specific device and specific numbers 

import boto3
import botocore
from boto3.dynamodb.conditions import Key, Attr


dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table("simulated_fractal_data")
a=input("SN number  ")
b=input("how many record?")


response = table.query(
              Limit = int(b),
              ScanIndexForward = False,
              KeyConditionExpression=Key('SN').eq(a)
           )
print(response)
