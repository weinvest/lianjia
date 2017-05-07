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

detail_mapping = {
            u'房屋户型：': 'layout'
            , u'所在楼层：': 'floor'
            , u'建筑面积：': 'area'
            , u'房屋朝向：': 'orientations'
            , u'配备电梯：': 'elevator'
            , u'装修情况：': 'decorate'
            , u'上次交易：': 'lastTrade'
            , u'房屋类型：': 'realEstateType'
            , u'房本年限：': 'ownershipCertificateDuration'
            , u'单价：': 'unitPrice'
            , u'首付：': 'downPayment'
            , u'月供：': 'monthlyPayments'
            , u'年代：': 'completeYear'
            , u'环线：': 'loopLine'
        }

def parse_ershoufan_detail(self, response):
    # scrapy.shell.inspect_response(response, self)
    from CSSUtils import extract
    erShouFan = items.ErShouFan()
    priceNode = response.css('div.houseInfo div.price')
    erShouFan['totalPrice'] = extract(priceNode.css('div.mainInfo ::text')) + extract(priceNode.css('span.unit ::text'))
    erShouFan['xiaoQu'] = extract(response.css('a.propertyEllipsis.ml_5 ::text')) + extract(response.css('span.areaEllipsis ::text'))
    erShouFan['address'] = extract(response.css('p.addrEllipsis.fl.ml_5 ::text'))

    details = {}
    # body > div.esf - top > div.cj - cun > div.content > table > tbody > tr:nth - child(1) > td:nth - child(1)
    for tr in response.css('table.aroundInfo tr td'):
        key = tr.css('span.title ::text').extract_first()
        value = tr.css("::text").extract()[-1]
        if key is None or value is None:
            continue
        details[key.strip()] = value.strip()

    for li in response.css("div.content ul li"):
        key = li.css('span.label::text').extract_first()
        value = li.css('::text').extract()[-1]
        if key is None or value is None:
            continue
        details[key.strip()] = value.strip()

    for key, value in details.items():
        key = key.strip()
        value = value.strip()
        v = detail_mapping
        if key in v:
            erShouFan[v[key]] = value
        else:
            pass
            # print 'Error key:' + key
        # print "%s:%s" % (key, value)

    yield erShouFan