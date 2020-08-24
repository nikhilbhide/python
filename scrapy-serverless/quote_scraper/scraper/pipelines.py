# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json

class QuoteScraperPipeline:
    def process_item(self, item, spider):
        data = {}
        author = item['author'][0]
        tags = item['tags']
        quote = item['quote_text'][0]
        quote = quote.replace('”','')
        quote = quote.replace('“','')
        data['quote']=quote
        data['author']=author[0]
        data['tags']=tags
        with open('data.txt', 'a') as outfile:
            json.dump(data, outfile)
            outfile.write("\n")
