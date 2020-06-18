# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json
import ast
from ...items.fang.xzlshou import FangXzlShouItem

class FangXzlShouSpider(scrapy.Spider):
    name = 'FangXzlShouSpider'
    allowed_domains = ['fang.com']
    start_urls = ['https://ditu.fang.com/?c=channel&a=ajaxXiaoquMapSearch&x1=116.47361755371094&y1=39.964210510253906&distance=2&strNewCode=1010082663&esf=1']
    db_name = 'fang'
    collection_name = 'xzlshou'

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

                item = FangXzlShouItem()
                item["info"] = building

                yield item

        new_url = 'https://ditu.fang.com/?c=channel&a=ajaxXiaoquMapSearch&x1={} \
        &y1={}&distance=2&strNewCode={}&esf=1'.format(url_queue[0][1], url_queue[0][2], url_queue[0][0])
        del url_queue[0]

        yield scrapy.Request(url=new_url,
            callback=self.parse    
        )
