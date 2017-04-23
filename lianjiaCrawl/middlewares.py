# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals


class LianjiacrawlSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


# This is a downloader middleware that can be used to get rendered javascript pages using webkit.
#
# this could be extended to handle form requests and load errors, but this is the bare bones code to get it done.
#
# the advantage over the selenium based approachs I've seen is that it only makes one request and you don't have to set up selenium.

from scrapy.http import FormRequest, HtmlResponse
from lianjiaCrawl import settings


class WebkitDownloader(object):
    def __init__(self):
        self.s = None

    def login(self, url, userName, password, headers):
        from ghost import Ghost
        self.s = Ghost().start()
        self.s.open(url, user_agent=settings.USER_AGENT)
        self.s.wait_for_selector('#loginUrl')
        self.s.click('#loginUrl')
        self.s.wait_for_selector('#login-user-btn', 10)

        self.s.set_field_value('#user_name', userName)
        self.s.set_field_value('#user_password', password)
        self.s.click('#login-user-btn')
        self.s.wait_for_selector('span.user-name')

    def process_request(self, request, spider):
        if (type(request) is not FormRequest):
            if self.s is None:
                self.login(request.url, spider.userName, spider.password, spider.headers)
            else:
                self.s.click('a[href="%s"]' % request.url)
                self.s.wait_for_page_loaded(15)
            return HtmlResponse(request.url, body=self.s.content, encoding='utf-8')

