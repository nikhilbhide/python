import os
import json
import boto3
from boto3.dynamodb.conditions import Key, And
import boto3
from functools import reduce

dynamodb = boto3.resource('dynamodb')

#retrives quote metadata using actual quote
def get_by_quote(event, context):
    table = dynamodb.Table('quotes')
    
    # fetch item from the database using quote as a key
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

#retrives quote metadata using actual index author_name-index by author_name
def get_by_author_name(author_name):
    table = dynamodb.Table('quotes')
    if author_name==None or author_name=="":
        #bad reuqest so respond with 400
        return {
            "statusCode": 400
        }
    else:
        #fetch item from the database using author_name
        response = table.query(IndexName='author_name-index',
                            KeyConditionExpression=Key('author_name').eq(author_name))
        if "Items" in response:
            return {
                "statusCode":200,
                "body": json.dumps(response ['Items'])
            }
        else:
            #check for empty response
            return {
                "statusCode": 204
            }    
  
#lists all quotes 
def list():
    table = dynamodb.Table('quotes')
    # fetch all todos from the database
    result = table.scan()
    print(type(result))
    # create a response
    response = {
        "statusCode": 200,
        "body": json.dumps(result['Items'])
    }

    return response

#validates the field and returns status based on the value of the field
def validate_field(value):
    if(value is None or value == ""):
        return False
    else:
        return True

def get_valid_fields(author_name, quote):
    if validate_field(author_name) and validate_field(quote):
        return False

#retrives quote metadata on the basis of inputs
def get(event, context):
    print("This is event:")
    print(event)
    table = dynamodb.Table('quotes')
    queryParams = event.get('queryStringParameters')
    print("queryParams is")
    print(queryParams)
    if queryParams is None or len(queryParams)==0:
        return list()
    else:
        author_name = queryParams.get("author_name")  
        quote = queryParams.get("quote")
        if validate_field(quote):
            FilterExpression=reduce(And, ([Key(k).eq(v) for k, v in queryParams.items()]))
            print("ExpressionAttributeValues")
            print(FilterExpression)
             # fetch item from the database using quote as a key
            result = table.query(
                KeyConditionExpression= FilterExpression
             )
            print(result)
            response = {
               "statusCode": 200,
                "body": json.dumps(result['Items'])
            }
            return response     
        else:
            print("filter by only author")
            return get_by_author_name(author_name)
