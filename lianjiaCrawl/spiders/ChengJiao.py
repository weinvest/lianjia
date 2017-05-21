# -*- coding: gbk -*-
import scrapy
import lianjiaCrawl.items as items
def parse_chengjiao(self, response):
    # scrapy.shell.inspect_response(response, self)
    for ershoufan in response.css('div.m-list.cj-list ul>li'):
        detailUrl = ershoufan.css('a.info-col.text.link-hover-green ::attr("href")').extract_first()
        yield scrapy.Request(response.urljoin(detailUrl)
                             , headers=self.headers
                             , meta={'cookiejar': response.meta['cookiejar'], 'cssSelector': 'a[href="%s"]' % detailUrl}
                             , callback=self.parse_chengjiao_detail
                             , dont_filter=True)

    next = response.css('a[gahref="results_next_page"] ::attr("href")')
    if next is not None:
        nextPageUrl = next.extract_first()
        yield scrapy.Request(response.urljoin(nextPageUrl)
                             , headers=self.headers
                             , meta={'cookiejar': response.meta['cookiejar'], 'cssSelector': 'a[href="%s"]' % nextPageUrl}
                             , callback=self.parse_chengjiao)

chengjiao_mapping = {
    u'挂牌单价：': 'unitPrice',
    u'楼层：': 'floor',
    u'年代：': 'completeYear',
    u'装修：': 'decorator',
    u'朝向：': 'orientations',
    u'小区：': 'xiaoQu',
    u'地址：': 'address',
    u'房源编号：': 'sourceNo'
}

def parse_chengjiao_detail(self, response):
    chengJiao = items.ChengJiao()
    # scrapy.shell.inspect_response(response, self)
    solidInfo = response.css('div.soldInfo')

    tradingTimeAndAgency = solidInfo.css('div.cell.first ::text').extract()
    if 2 <= len(tradingTimeAndAgency):
        chengJiao["tradeTime"] = tradingTimeAndAgency[-2].strip()
        chengJiao['agency'] = tradingTimeAndAgency[-1].strip()

    totalPrice = solidInfo.css('div.cell p ::text').extract()[1:] #挂牌总价
    chengJiao['totalPrice'] = totalPrice[0] + totalPrice[1]

    for td in response.css('table.aroundInfo td'):
        pair = td.css('::text').extract()
        if 2 <= len(pair):
            key = pair[-2].strip()
            value = pair[-1].strip()
        else:
            continue

        if key in chengjiao_mapping:
            chengJiao[chengjiao_mapping[key]] = value
    yield chengJiao