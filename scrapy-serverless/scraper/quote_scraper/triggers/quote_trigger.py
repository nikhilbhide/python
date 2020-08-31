import json 
import nltk
import boto3, botostubs
from botocore.exceptions import ClientError
import decimal

nltk.data.path.append("/tmp")
nltk.download('punkt',download_dir = "/tmp")
dynamodb = boto3.resource('dynamodb', region_name='ap-south-1')  
table = dynamodb.Table('quote_words_by_author_name')

def get_record_by_author_name(author_name, word):
    print("reading with transactions")
    response = table.transact_get_items(Key={
                'author_name': author_name,
                'word':word
            })
    return response  

def update_count(author_name, word, count,):
    print("writing with transactions")
    response = table.transact_write_items(Item={'author_name':author_name,
              'word': word,
              'count':decimal.Decimal(count)
              }
            )
    print(response)

def store_tokens_by_author(author_name, words, mode):
    for word in words:
        record = get_record_by_author_name(author_name,word)
        print(type(record))
        count = 0 if mode==0 else 1
        if "Item" in record:
            #check for existing count
            count = record['Item']['count']    
        if mode == 0:
            #if its new quote then increment word count
            count = count + 1
        else:
            count = count - 1
        #update word count per author_name    
        update_count(author_name,word,count)
        
        
def process_change_event(author_name, quote):
    tokens = get_tokens(quote)
    store_tokens_by_author(author_name,tokens)

def get_tokens(sentence):
    words = nltk.word_tokenize(sentence)
    new_words= [word for word in words if word.isalnum()]
    return new_words
    
def quote_trigger_handler(event,context):
     # TODO implement
    print("published event for change event trigger of quotes table")
    print(event)
    try:
        records = event['Records']
        for record in records:
            eventName = record['eventName']
            print(eventName)
            data = record["dynamodb"]["NewImage"]
            author_name = data["author_name"]["S"]
            quote = data["quote"]["S"]
            if eventName=="INSERT":
                process_change_event(author_name,quote,0)
            else:
                process_change_event(author_name,quote,1)
    except Exception as e:
        print("quote dynamodb trigger execution failed with exception - ",e)           