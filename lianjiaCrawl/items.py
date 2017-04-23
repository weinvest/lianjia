# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class XiaoQu(scrapy.Item):
    realEstateType = scrapy.Field()
    completeTime = scrapy.Field()
    propertyFee = scrapy.Field()
    propertyCompany = scrapy.Field()
    propertyDevelopers = scrapy.Field()
    loopLine = scrapy.Field()
    area = scrapy.Field()

class LianjiacrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
