import json 
import nltk
import boto3
from botocore.exceptions import ClientError
import decimal

nltk.data.path.append("/tmp")
nltk.download('punkt',download_dir = "/tmp")
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')
table = dynamodb.Table('quote_words_by_author_name')

def get_record_by_author_name(author_name, word):
    response = table.get_item(Key={
                'author_name': author_name,
                'word':word
            })
    return response  

def update_count(author_name, word, count):
    table.put_item(Item={'author_name':author_name,
              'word': word,
              'count':decimal.Decimal(count)
              }
            )

def store_tokens_by_author(author_name, words):
    for word in words:
        record = get_record_by_author_name(author_name,word)
        print(type(record))
        count = 0
        if "Item" in record:
            count = record['Item']['count']    
        count = count + 1
        update_count(author_name,word,count)
        # if result['Items'] is None:
        #     dynamodb.put_item(TableName='quote_words_by_author_name', 
        #     Item={'author_name':{'S':author_name},
        #       'word':{'S': word},
        #       'count':{'N':1}
        #       }
        #     )
        # else:
        #     print(result)
        
def process_change_event(author_name, quote):
    tokens = get_tokens(quote)
    store_tokens_by_author(author_name,tokens)

def get_tokens(sentence):
    words = nltk.word_tokenize(sentence)
    new_words= [word for word in words if word.isalnum()]
    return new_words
    
def quote_trigger_handler(event,context):
     # TODO implement
    print(event)
    print(context)
    try:
        records = event['Records']
        for record in records:
            eventName = record['eventName']
            print(eventName)
            if eventName=="INSERT":
                data = record["dynamodb"]["NewImage"]
                author_name = data["author_name"]["S"]
                quote = data["quote"]["S"]
                process_change_event(author_name,quote)
                print(author_name)
                print(quote)
              
    except Exception as e:
        print("quote dynamodb trigger execution failed with exception - ",e)           