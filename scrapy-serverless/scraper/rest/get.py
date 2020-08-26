import os
import json
import boto3
dynamodb = boto3.client('dynamodb')

#retrives quote metadata using actual quote
def get_by_quote(event, context):
    table = dynamodb.Table('quotes')
    
    # fetch todo from the database
    result = table.get_item(
        Key={
            'quote': event['quote']
        }
    )

    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Item'])
    }

    return response