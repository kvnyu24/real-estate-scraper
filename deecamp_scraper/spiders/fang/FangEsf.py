# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json
import ast
from ...items.fang.esf import FangEsfItem

class FangEsfSpider(scrapy.Spider):
    name = 'FangEsfSpider'
    allowed_domains = ['fang.com']
    start_urls = ['https://ditu.fang.com/?c=channel&a=ajaxXiaoquMapSearch&x1=116.5583724975586&y1=39.742698669433594&distance=2&strNewCode=1010713519&city=bj&esf=1']
    db_name = 'fang'
    collection_name = 'esf'

    def parse(self, response):
        res_json = json.loads(response.body)

        zhuzhai = res_json["住宅"]
        xiezilou = res_json["写字楼"]
        shangpu = res_json["商铺"]
        bieshu = res_json["别墅"]

        building_types = [zhuzhai, xiezilou, shangpu, bieshu]
        url_queue = []

        for building_type in building_types:
            for building in building_type:
                projcode = building["projcode"]
                coordx = building["coordx"]
                coordy = building["coordy"]
                city = building["city"].encode("unicode-escape").decode("utf-8").replace("\\", "%")
                district = building["district"].encode("unicode-escape").decode("utf-8").replace("\\", "%")

                url_queue.append((projcode, coordx, coordy))
                price_url = "https://pinggun.fang.com/RunChartNew/MakeChartData?newcode=" + projcode + \
                "&city=" + city + "&district=" + district + \
                "&commerce=&titleshow=&year="

                item = FangEsfItem()
                item["info"] = building

                yield scrapy.Request(url=price_url,
                    meta={"item": item},
                    callback=self.getPrice,
                    method="GET",
                    headers={"Content-Type": "application/json"},
                )

        new_url = 'https://ditu.fang.com/?c=channel&a=ajaxXiaoquMapSearch&x1={} \
        &y1={}&distance=2&strNewCode={}&esf=1'.format(url_queue[0][1], url_queue[0][2], url_queue[0][0])
        del url_queue[0]

        yield scrapy.Request(url=new_url,
            callback=self.parse    
        )

    def getPrice(self, response):
        item = response.meta["item"]
        price_list = ast.literal_eval(response.body.decode("utf-8", "ignore").split("&")[0])
        price_json = dict(price_list)
        price_json = json.loads(json.dumps(price_json), parse_int=str)

        item["price_change"] = price_json

        yield item
