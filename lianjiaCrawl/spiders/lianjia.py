# -*- coding: gbk -*-
import scrapy
import scrapy.shell
import lianjiaCrawl.settings as settings
import XiaoQu
from functools import partial
import ErShouFan
class LianjiaSpider(scrapy.Spider):
    name = "lianjia"
    headers={
        'Accept-Encoding': 'gzip,deflate,sdch',
        'Accept-Language': 'en-US,en;q=0.8',
        'User-Agent': settings.USER_AGENT,
        'Accept': '*/*',
        'Connection': 'keep-alive',
        'Content-Type': 'text/plain; charset=utf-8'
    }
    domain = 'http://sh.lianjia.com'



    cookies = ''
    def __init__(self):
        self.userName = '18221528649'
        self.password = 'asd1831031'
        self.crawlingDeals = False

        self.parse_xiaoqu = partial(XiaoQu.parse_xiaoqu, self)
        self.parse_xiaoQuDetail = partial(XiaoQu.parse_xiaoQuDetail, self)

        self.parse_ershoufan = partial(ErShouFan.parse_ershoufan, self)
        self.parse_ershoufan_detail = partial(ErShouFan.parse_ershoufan_detail, self)

    def start_requests(self):
        #urls = {'/xiaoqu' : self.parse_xiaoqu, '/ershoufang': self.parse_ershoufan}
        urls = {'/ershoufang': self.parse_ershoufan}
        for url, callback in urls.items():
            yield scrapy.Request(self.domain + url
                                 , headers=self.headers
                                 , meta={'cookiejar': 1}
                                 , callback=callback
                                 , dont_filter=True)

    def login(self, response):
        return [scrapy.Request(self.start_url
                               , headers=self.headers
                               , meta={'cookiejar': 1}
                               , callback=self.after_login
                               , dont_filter=True)
                ]

    def after_login(self, response):
        url = self.start_url + 'xiaoqu'
        return [scrapy.Request(url
                               , headers=self.headers
                               , meta={'cookiejar':response.meta['cookiejar'], 'cssSelector': 'a[href="%s"]' % url}
                               , callback=self.parse_xiaoqu)]

