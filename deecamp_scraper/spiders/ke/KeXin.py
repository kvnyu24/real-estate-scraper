# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json
import ast
from ...items.ke.xin import KeXinItem

class KeXinSpider(scrapy.Spider):
    name = 'KeXinSpider'
    allowed_domains = ['ke.com']
    db_name = 'ke'
    collection_name = 'xin'

    def start_requests(self):

        api_url = 'https://bj.fang.ke.com/loupan/' 
        tag = '/buildingmark'
        base_url = 'https://bj.fang.ke.com/loupan/pg'

        for i in range(1, 40):
            yield scrapy.Request(
                url=base_url+str(i),
                meta={"api_url": api_url, "tag": tag},
                callback=self.parse    
            )



    def parse(self, response):
        api_url = response.meta["api_url"]
        tag = response.meta["tag"]
        houses = Selector(response).xpath('/html/body/div[6]/ul[2]/li/div/div[1]')
        
        for house in houses:
            house_link = house.xpath(
                'a/@href'
            ).extract()[0]

            house_code = house_link.split('/')[-2]

            url = api_url + house_code + tag

            yield scrapy.Request(
                url=url, 
                callback=self.get_house,
                method="GET",
                headers={"Content-Type": "application/json"},
            )




    def get_house(self, response):
        res_json = json.loads(response.body)["data"]["build_list"]


        for house  in res_json:
            item = KeXinItem()
            item["info"] = house
            yield item




