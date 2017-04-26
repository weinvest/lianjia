# -*- coding: utf-8 -*-
import scrapy
import scrapy.shell
import lianjiaCrawl.settings as settings
import lianjiaCrawl.items as items
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
        url = self.start_url + 'xiaoqu'
        return [scrapy.Request(url
                               , headers=self.headers
                               , meta={'cookiejar':response.meta['cookiejar'], 'cssSelector': 'a[href="%s"]' % url}
                               , callback=self.parse_xiaoqu)]

    def parse_xiaoqu(self, response):
        from functools import partial
        for jsXiaoQu in response.css('ul.house-lst>li'):
            xiaoQu = items.XiaoQu()
            where = jsXiaoQu.css('a.actshowMap_list ::attr("xiaoqu")').extract_first()
            where = where[1:-2]
            where = where.split(',')
            xiaoQu['lat'] = where[0].strip()
            xiaoQu['lon'] = where[1].strip()
            xiaoQu['name'] = where[2].strip()
            xiaoQu['districtName'] = jsXiaoQu.css('a.actshowMap_list ::attr("districtname")').extract_first()
            xiaoQu['plateName'] = jsXiaoQu.css('a.actshowMap_list ::attr("platename")').extract_first()
            xiaoQu['bookingQty'] = jsXiaoQu.css('div.square span.num ::text').extract_first()

            detailUrl = jsXiaoQu.css('a[name="selectDetail"] ::attr("href")').extract_first()
            yield scrapy.Request(response.url.replace('/xiaoqu', detailUrl)
                                 , headers=self.headers
                                 , meta={'cookiejar':response.meta['cookiejar'], 'cssSelector': 'a[href="%s"]' % detailUrl}
                                 , callback=partial(self.parse_xiaoQuDetail, xiaoQu))

    def parse_xiaoQuDetail(self, xiaoQu, response):
        scrapy.shell.inspect_response(response, self)
        for li in response.css("div.col-2.clearfix li"):
            key = li.css('label ::text').extract_first()
            value = li.css('span.other ::text').extract_first().strip()
            v = {
                '': 'realEstateType'
                ,'1': 'completeTime'
                ,'2': 'propertyFee'
                ,'3': 'propertyCompany'
                ,'4': 'propertyDevelopers'
                ,'5': 'loopline'
                ,'6': 'city'
            }

            xiaoQu[v[key]] = value

        xiaoQu['avgPrice'] = response.css('span.p ::text').extract_first().strip()

    def parse_ershoufan(self, response):
        scrapy.shell.inspect_response(response, self)
