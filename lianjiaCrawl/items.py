# -*- coding: gbk -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class XiaoQu(scrapy.Item):
    name = scrapy.Field()
    realEstateType = scrapy.Field()
    completeTime = scrapy.Field()
    propertyFee = scrapy.Field()
    propertyCompany = scrapy.Field()
    propertyDevelopers = scrapy.Field()
    loopLine = scrapy.Field()
    lat = scrapy.Field()
    lon = scrapy.Field()
    city = scrapy.Field()
    districtName = scrapy.Field()
    plateName = scrapy.Field()
    avgPrice = scrapy.Field()
    bookingQty = scrapy.Field()


class ErShouFan(scrapy.Item):
    totalPrice = scrapy.Field() #总价
    layout = scrapy.Field()   #房型
    area = scrapy.Field()      #面积
    unitPrice = scrapy.Field()  #单价
    downPayment = scrapy.Field()  #首付
    monthlyPayments = scrapy.Field() #月供
    completeYear = scrapy.Field()
    floor = scrapy.Field()
    orientations = scrapy.Field() #朝向
    decorate = scrapy.Field() #装修
    loopLine = scrapy.Field()
    xiaoQu = scrapy.Field()
    address = scrapy.Field()
    lastTrade = scrapy.Field()
    elevator = scrapy.Field()
    realEstateType = scrapy.Field() # 房屋类型
    ownershipCertificateDuration = scrapy.Field() #房本年限

class ChengJiao(scrapy.Item):
    tradeTime = scrapy.Field()
    agency = scrapy.Field() #中介
    totalPrice = scrapy.Field() #挂牌总价
    unitPrice = scrapy.Field() #挂牌单价
    floor = scrapy.Field() #楼层
    completeYear = scrapy.Field() #年代
    decorator = scrapy.Field() #装修
    orientations = scrapy.Field() #朝向
    xiaoQu = scrapy.Field()
    address = scrapy.Field()
    sourceNo = scrapy.Field() #词源编号

