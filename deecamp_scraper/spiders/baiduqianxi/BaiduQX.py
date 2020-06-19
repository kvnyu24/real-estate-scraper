# -*- coding: utf-8 -*-
import scrapy
import json
from ...items.baiduqianxi.baiduqx import BaiduQXItem



class BaiduQXSpider(scrapy.Spider):
    name = 'BaiduQXSpider'
    allowed_domains = ['http://huiyan.baidu.com']
    start_urls = ['https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=420100&type=move_in&date=20200110']
    db_name = 'baiduqx'
    collection_name = 'wuhan'


    def parse(self, response):
        city_in = json.loads(response.body.decode("utf-8").strip(r'cb(').strip(r')'))["data"]

        item = BaiduQXItem()
        item["city_in"] = city_in



        yield city_in
