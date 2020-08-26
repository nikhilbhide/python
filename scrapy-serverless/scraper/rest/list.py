import os
import json
import boto3
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')

#lists all quotes from the table
def list_all_quotes(event, context):
    table = dynamodb.Table('quotes')

    # fetch all todos from the database
    result = table.scan()

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response