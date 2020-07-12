# -*- coding: utf-8 -*-
import scrapy
import json
from ...items.qqheat.xingyun import QQHeatXyItem


class QQHeatXingYun0Spider(scrapy.Spider):
    name = 'QQHeatXingYun0Spider'
    allowed_domains = ['heat.qq.com']
    db_name = 'qqheat'
    collection_name = 'xingyun'

    def start_requests(self):        
        url = 'https://xingyun.map.qq.com/api/getXingyunPoints'

        ranks = [0]

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

        locations = res["locs"]
        locs_split = locations.split(",")

        all_locs = []
        for i in range(int(len(locs_split)/3)):
            lat = locs_split[0+3*i]      
            lon = locs_split[1+3*i]      
            count = locs_split[2+3*i]
            
            all_locs.append([int(lat)/100, int(lon)/100, count])

        item["locs"] = all_locs
 
        
        yield item 