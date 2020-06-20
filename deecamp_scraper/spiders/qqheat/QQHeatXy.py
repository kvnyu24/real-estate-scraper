# -*- coding: utf-8 -*-
import scrapy
import json
from ...items.qqheat.xingyun import QQHeatXyItem


class QQHeatXingYunSpider(scrapy.Spider):
    name = 'QQHeatXingYunSpider'
    allowed_domains = ['heat.qq.com']
    db_name = 'qqheat'
    collection_name = 'xingyun'

    def start_requests(self):        
        url = 'https://xingyun.map.qq.com/api/getXingyunPoints'

        ranks = [i for i in range(4)]

        for rank in ranks:
            yield scrapy.Request(
                url=url, 
                meta={"rank": rank},
                callback=self.parse,
                method="POST",
                headers={"Content-Type": "application/json"},
                body=json.dumps({"count":4,"rank":rank})
            )
    
    
    def parse(self, response):
        res = json.loads(response.body)

        item = QQHeatXyItem()
        item["rank"] = response.meta["rank"]
        item["time"] = res["time"]
        item["locs"] = res["locs"]
        
        yield item 