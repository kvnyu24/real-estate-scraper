# -*- coding: utf-8 -*-
import scrapy


class QQheatSpider(scrapy.Spider):
    name = 'QQHeatSpider'
    allowed_domains = ['https://heat.qq.com/index.php']
    start_urls = ['http://heat.qq.com/index.php/']

    def parse(self, response):
        pass
