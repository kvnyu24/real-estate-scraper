# -*- coding: utf-8 -*-
import scrapy


class QQHeatXyItem(scrapy.Item):
    rank = scrapy.Field()
    time = scrapy.Field()
    locs = scrapy.Field()


