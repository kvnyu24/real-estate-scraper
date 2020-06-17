# -*- coding: utf-8 -*-
import scrapy


class ZillowBuyItem(scrapy.Item):
    info = scrapy.Field()
    price_change = scrapy.Field()


