import sys
import imp
import os
import logging
from urllib.parse import urlparse
from scrapy.spiderloader import SpiderLoader
from scrapy import crawler
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerRunner
from importlib import import_module 
from multiprocessing import Process, Queue
from twisted.internet import reactor

# Need to "mock" sqlite for the process to not crash in AWS Lambda / Amazon Linux
sys.modules["sqlite"] = imp.new_module("sqlite")
sys.modules["sqlite3.dbapi2"] = imp.new_module("sqlite.dbapi2")
result = None

def spider_closing(spider):
    """Activates on spider closed signal"""
    logging.msg("Spider closed: %s" % spider, level=log.INFO)
    reactor.stop()
    logging.msg("reactor stopping")

def is_in_aws():
    return os.getenv('AWS_EXECUTION_ENV') is not None

def set_result(item):
    result = item

def crawl(settings={}, spider_name="quote_spider", spider_kwargs={}):
    project_settings = get_project_settings()
    spider_loader = SpiderLoader(project_settings)

    spider_cls = spider_loader.load(spider_name)

    feed_uri = ""
    feed_format = "json"

    if is_in_aws():
		# Lambda can only write to the /tmp folder.
        settings['HTTPCACHE_DIR'] =  "/tmp"

    process = CrawlerProcess({**project_settings, **settings})

    process.crawl(spider_cls, **spider_kwargs)
    process.start() 

    try:
        reactor.stop()    
    except Exception as e:
        print(e)
# # the wrapper to make it run more times
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