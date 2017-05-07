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
    totalPrice = scrapy.Field() #�ܼ�
    layout = scrapy.Field()   #����
    area = scrapy.Field()      #���
    unitPrice = scrapy.Field()  #����
    downPayment = scrapy.Field()  #�׸�
    monthlyPayments = scrapy.Field() #�¹�
    completeYear = scrapy.Field()
    floor = scrapy.Field()
    orientations = scrapy.Field() #����
    decorate = scrapy.Field() #װ��
    loopLine = scrapy.Field()
    xiaoQu = scrapy.Field()
    address = scrapy.Field()
    lastTrade = scrapy.Field()
    elevator = scrapy.Field()
    realEstateType = scrapy.Field() # ��������
    ownershipCertificateDuration = scrapy.Field() #��������


class LianjiacrawlItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
