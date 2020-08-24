# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import boto3


class QuoteScraperPipeline:
    def process_item(self, item, spider):
        data = {}
        author = item['author'][0]
        tags = item['tags']
        quote = item['quote_text'][0]
        quote = quote.replace('”','')
        quote = quote.replace('“','')
        data['quote']=quote
        data['author']=author
        data['tags']=tags
        
        self.insert_quote(data)
        return item
    
    def insert_quote(self, data):
        dynamodb = boto3.client('dynamodb', region_name = 'ap-south-1')
        dynamodb.put_item(TableName='quotes', 
        Item={'quote':{'S':data['quote']},
              'author_name':{'S':data['author']}
              }
            )