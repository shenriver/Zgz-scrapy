# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import time
from scrapy.http import HtmlResponse


# user_agent和ip
class RandomUserAgentMiddleware(object):
    def __init__(self, crawler):
        super(RandomUserAgentMiddleware, self).__init__()

        self.ua = UserAgent()
        self.ua_type = crawler.settings.get('RANDOM_UA_TYPE', 'random')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler)

    def process_request(self, request, spider):
        def get_ua():
            '''Gets random UA based on the type setting (random, firefox…)'''
            return getattr(self.ua, self.ua_type)

        request.headers.setdefault('User-Agent', get_ua())
        request.meta["proxy"] = "http://61.135.217.7:80"


# 模拟浏览器
class JSPageMiddleware(object):
    def process_request(self, request, spider):
        spider.browser.get(request.url)
        time.sleep(3)
        print("访问:{0}".format(request.url))

        return HtmlResponse(url=spider.browser.current_url, body=spider.browser.page_source, encoding="utf-8", request=request)





