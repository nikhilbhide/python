import scrapy
from ..items import QuoteScraperItem

class QuoteSpider(scrapy.Spider):
    name = "quote_spider"
    start_urls = [
        "http://quotes.toscrape.com/"
    ]

    def parse(self, response):
        quotes = response.css(".quote")
        items = QuoteScraperItem()
        for quote in quotes:
            quote_text = quote.css(".text::text").extract()
            author = quote.css(".author::text").extract()
            tags = quote.css(".tag::text").extract()
  
            items['quote_text'] = quote_text
            items['author'] = author
            items['tags'] = tags
           
            yield items
