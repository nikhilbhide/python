import scrapy
from ..items import QuoteScraperItem
from scrapy import signals
import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

class QuoteSpider(scrapy.Spider):
    name = "quote_spider"
    start_urls = [
        "http://quotes.toscrape.com/"
    ]

    def parse(self,response):
        # The main method of the spider. It scrapes the URL(s) specified in the
        # 'start_url' argument above. The content of the scraped URL is passed on
        # as the 'response' object.

        nextpageurl = response.css(".next a ::attr(href)")
        
        # When asked for a new item, ask self.scrape for new items and pass them along
        yield from self.scrape(response)
    
        if nextpageurl:
            path = nextpageurl.extract_first()
            nextpage = response.urljoin(path)
            print("Found url: {}".format(nextpage))
            yield scrapy.Request(nextpage, callback=self.parse)

    def scrape(self, response):
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

    # the wrapper to make it run more times
    def run_spider(spider):
        def f(q):
            try:
                runner = crawler.CrawlerRunner()
                deferred = runner.crawl(spider)
                deferred.addBoth(lambda _: reactor.stop())
                reactor.run()
                q.put(None)
            except Exception as e:
                q.put(e)

        q = Queue()
        p = Process(target=f, args=(q,))
        p.start()
        result = q.get()
        p.join()

        if result is not None:
            raise result
            
                