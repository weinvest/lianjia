# -*- coding: utf-8 -*-
import scrapy
import lianjiaCrawl.items as items

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
        # xiaoQu['city'] = response.cooki
        detailUrl = jsXiaoQu.css('a[name="selectDetail"] ::attr("href")').extract_first()
        yield scrapy.Request(response.urljoin(detailUrl)
                             , headers=self.headers
                             , meta={'cookiejar': response.meta['cookiejar'], 'cssSelector': 'a[href="%s"]' % detailUrl}
                             , callback=partial(self.parse_xiaoQuDetail, xiaoQu))

    next = response.css('a[gahref="results_next_page"] ::attr("href")')
    if next is not None:
        nextPageUrl = next.extract_first()
        yield scrapy.Request(response.urljoin(nextPageUrl)
                             , headers=self.headers
                             , meta={'cookiejar': response.meta['cookiejar'], 'cssSelector': 'a[href="%s"]' % nextPageUrl}
                             , callback=self.parse_xiaoqu)


def parse_xiaoQuDetail(self, xiaoQu, response):
    # scrapy.shell.inspect_response(response, self)
    for li in response.css("div.col-2.clearfix li"):
        key = li.css('label ::text').extract_first()
        value = li.css('span.other ::text').extract_first()

        if key is None or value is None:
            continue

        key = unicode.strip(key)
        value = unicode.strip(value)
        #print key, value
        v = {
            u'物业类型：': 'realEstateType'
            , u'建成年代：': 'completeTime'
            , u'物业费用：': 'propertyFee'
            , u'物业公司：': 'propertyCompany'
            , u'开发商：': 'propertyDevelopers'
            , u'环线： ': 'loopline'
        }

        if key in v:
            xiaoQu[v[key]] = value
        else:
            pass
            #print 'Error key:' + key

    priceEle = response.css('span.p ::text').extract_first()
    if priceEle is not None:
        xiaoQu['avgPrice'] = priceEle.strip()
    yield xiaoQu
