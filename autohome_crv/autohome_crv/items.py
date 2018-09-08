# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst

class AutohomeCrvItem(scrapy.Item):
    # 将提取的数据整合到4个类别中
    base = scrapy.Field()
    car = scrapy.Field()
    feeling = scrapy.Field()
    comments = scrapy.Field()

    # 基本信息
    eid = scrapy.Field()
    userId = scrapy.Field()
    userName = scrapy.Field()
    lastEdit = scrapy.Field()
    medal = scrapy.Field()
    visitcount = scrapy.Field()
    helpfulcount = scrapy.Field()
    commentcount = scrapy.Field()
    # 汽车信息
    specname = scrapy.Field()
    boughtAddress = scrapy.Field()
    boughtPrice = scrapy.Field()
    drivekilometer = scrapy.Field()
    boughtdate = scrapy.Field()
    actualOilConsumption = scrapy.Field()
    # 满意度
    bestScene = scrapy.Field()
    worstScene = scrapy.Field()
    # 评论
    spaceScene = scrapy.Field()
    powerScene = scrapy.Field()
    maneuverabilityScene = scrapy.Field()
    oilScene = scrapy.Field()
    comfortablenessScene = scrapy.Field()
    apperanceScene = scrapy.Field()
    internalScene = scrapy.Field()
    costefficientScene = scrapy.Field()
    reasonScene = scrapy.Field()
    ## 评论中的 其他描述
    otherScene = scrapy.Field()
    batteryScene = scrapy.Field()


class AutohomeCrvLoader(ItemLoader):
    default_output_processor = TakeFirst() # 返回的json数据的值都用列表包装，所以提取第一个（返回的原始数据样本见 test.txt）
