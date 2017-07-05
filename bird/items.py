# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Item, Field

# 线路信息
class LineItem(Item):

    # 出发城市
    fromCity = Field()
    # 到达城市
    toCity = Field()

# 航班价格信息
class FlightItem(Item):

    # 获得日期
    findDate = Field()
    # 获得时间
    findTime = Field()
    # 销售渠道
    source = Field()

    # 出发城市 dcn
    fromCity = Field()
    # 出发城市编号 dcc
    fromCityCode = Field()
    # 出发机场 dpbn
    fromAir = Field()
    # 出发机场编号 dpc
    fromAirCode = Field()
    # 出发机场航站楼 dsmsn
    fromAirNo = Field()

    # 到达城市 acn
    toCity = Field()
    # 到达城市编号 acc
    toCityCode = Field()
    # 到达机场 apbn
    toAir = Field()
    # 到达机场编号 apc
    toAirCode = Field()
    # 到达机场航站楼 asmsn
    toAirNo = Field()

    # 航空公司 alc
    air = Field()
    # 航班号 fn
    number = Field()
    # 出发日期
    fromDate = Field()
    # 出发时间 dt
    fromTime = Field()
    # 到达时间 at
    toTime = Field()

    # 价格 lp
    price = Field()
    # 原价 lcfp
    basePrice = Field()
    # 机场建设费 tax
    tax = Field()


