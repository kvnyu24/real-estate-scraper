# -*- coding: utf-8 -*-
import scrapy
import json
from ...items.baiduqianxi.baiduqxmi import BaiduQXMigrationIndexItem
from scrapy.utils.project import get_project_settings




class BaiduQxIoSpider(scrapy.Spider):
    name = 'BaiduQxIoSpider'
    allowed_domains = ['http://huiyan.baidu.com']
    start_urls = ['https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id=420100&type=move_in&date=20200110']
    db_name = 'baiduqx'
    collection_name = 'wuhan'
    
    settings = get_project_settings()

    code = str(420100)
    


    def parse(self, response):
        city_in = json.loads(response.body.decode("utf-8").strip(r'cb(').strip(r')'))["data"]

        item = BaiduQXMigrationIndexItem()
        item["migration_index"] = city_in

        city_out_url = 'http://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id={code}&type=move_out&date={date}'
        migration_index_url = 'http://huiyan.baidu.com/migration/historycurve.jsonp?dt=city&id={code}&type=move_{direction}&date={date}'
        internal_flow_url = 'http://huiyan.baidu.com/migration/internalflowhistory.jsonp?dt=city&id={code}&date={date}'



        yield city_in
