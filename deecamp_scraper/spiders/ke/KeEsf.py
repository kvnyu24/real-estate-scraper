# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json
import ast
from ...items.ke.esf import KeEsfItem

class KeEsfSpider(scrapy.Spider):
    name = 'KeEsfSpider'
    allowed_domains = ['ke.com']
    db_name = 'ke'
    collection_name = 'esf'

    def start_requests(self):

        api_url = 'https://bj.ke.com/ershoufang/esfrecommend?id='  
        base_url = 'https://bj.ke.com/ershoufang/pg'

        for i in range(1, 101):
            yield scrapy.Request(
                url=base_url+str(i),
                meta={"api_url": api_url},
                callback=self.parse    
            )



    def parse(self, response):
        api_url = response.meta["api_url"]
        houses = Selector(response).xpath('/html/body/div[1]/div[4]/div[1]/div[4]/ul/li/div')
        
        for house in houses:
            house_link = house.xpath(
                'div[1]/a/@href'
            ).extract()[0]

            house_code = house_link.split('/')[-1].strip('.html')

            url = api_url + house_code

            yield scrapy.Request(
                url=url, 
                callback=self.get_house,
                method="GET",
                headers={"Content-Type": "application/json"},
            )




    def get_house(self, response):
        res_json = json.loads(response.body)["data"]["recommend"]


        for house  in res_json:
            item = KeEsfItem()
            item["info"] = house
            yield item




