# -*- coding: utf-8 -*-
import scrapy


class ZillowRentItem(scrapy.Item):
    info = scrapy.Field()
    price_change = scrapy.Field()


