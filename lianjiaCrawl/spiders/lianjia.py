# -*- coding: utf-8 -*-
import scrapy
import scrapy.shell
import lianjiaCrawl.settings as settings
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
    start_url = 'http://sh.lianjia.com/'
    cookies = ''
    def __init__(self):
        self.userName = '18221528649'
        self.password = 'asd1831031'

    def start_requests(self):
        return [scrapy.Request(self.start_url
                               , headers=self.headers
                               , meta={'cookiejar': 1}
                               , callback=self.after_login
                               , dont_filter=True)
                ]

    def after_login(self, response):
        return [scrapy.Request('http://sh.lianjia.com/xiaoqu'
                               , headers=self.headers
                               , method={'cookiejar':response.meta['cookiejar']}
                               , callback=self.parse_xiaoqu)]

    def parse_xiaoqu(self, response):
        scrapy.shell.inspect_response(response, self)
        hosuses = response.css('#house-lst')
        hosuses
        print hosuses

    def parse_ershoufan(self, response):
        scrapy.shell.inspect_response(response, self)
