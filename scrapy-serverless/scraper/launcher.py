import sys
import json
from quote_scraper.spiders.quote_spider import QuoteSpider
from quote_scraper.crawl import crawl, run_spider
import boto3 
from rest.get import get_by_author_name

def scrape(event={}, context={}):
    crawl(**event)
    #run_spider(QuoteSpider)

if __name__ == "__main__":
    try:
        event = json.loads(sys.argv[1])
    except IndexError:
        event = {}
    scrape(event)