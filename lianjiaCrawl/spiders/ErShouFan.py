# -*- coding: utf-8 -*-
import scrapy
from functools import partial
import lianjiaCrawl.items as items

def parse_ershoufan(self, response):
    for ershoufan in response.css('div.c-sort+ul>li'):
        detailUrl = ershoufan.css('a[gahref="results_click_order_1"] ::attr("href")').extract_first()
        yield scrapy.Request(response.urljoin(detailUrl)
                             , headers=self.headers
                             , meta={'cookiejar': response.meta['cookiejar'], 'cssSelector': 'a[href="%s"]' % detailUrl}
                             , callback=self.parse_ershoufan_detail)

    next = response.css('a[gahref="results_next_page"] ::attr("href")')
    if next is not None:
        nextPageUrl = next.extract_first()
        yield scrapy.Request(response.urljoin(nextPageUrl)
                             , headers=self.headers
                             , meta={'cookiejar': response.meta['cookiejar'], 'cssSelector': 'a[href="%s"]' % detailUrl}
                             , callback=self.parse_ershoufan)

def parse_ershoufan_detail(self, response):
    pass