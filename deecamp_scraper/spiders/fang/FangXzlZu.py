# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json
import ast
from ...items.fang.xzlzu import FangXzlZuItem

class FangXzlZuSpider(scrapy.Spider):
    name = 'FangXzlZuSpider'
    allowed_domains = ['fang.com']
    start_urls = ['https://ditu.fang.com/?c=channel&a=ajaxXiaoquMapSearch&x1=116.34791564941406&y1=39.895774841308594&distance=2&strNewCode=1010152347&esf=1']
    db_name = 'fang'
    collection_name = 'xzlzu'

    def parse(self, response):
        res_json = json.loads(response.body)

        zhuzhai = res_json["住宅"]
        xiezilou = res_json["写字楼"]


        building_types = [zhuzhai, xiezilou]
        url_queue = []

        for building_type in building_types:
            for building in building_type:
                projcode = building["projcode"]
                coordx = building["coordx"]
                coordy = building["coordy"]
                city = building["city"].encode("unicode-escape").decode("utf-8").replace("\\", "%")
                district = building["district"].encode("unicode-escape").decode("utf-8").replace("\\", "%")

                url_queue.append((projcode, coordx, coordy))

                item = FangXzlZuItem()
                item["info"] = building

                yield item

        new_url = 'https://ditu.fang.com/?c=channel&a=ajaxXiaoquMapSearch&x1={} \
        &y1={}&distance=2&strNewCode={}&esf=1'.format(url_queue[0][1], url_queue[0][2], url_queue[0][0])
        del url_queue[0]

        yield scrapy.Request(url=new_url,
            callback=self.parse    
        )
