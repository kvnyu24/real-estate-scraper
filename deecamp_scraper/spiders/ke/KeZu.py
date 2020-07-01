# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json
import ast
from ...items.ke.zu import KeZuItem

class KeZuSpider(scrapy.Spider):
    name = 'KeZuSpider'
    allowed_domains = ['ke.com']
    db_name = 'ke'
    collection_name = 'zu'

    def start_requests(self):

        api_url = 'https://bj.zu.ke.com/aj/house/similarRecommend?house_code=' 
        city_id = '&city_id=110000'
        base_url = 'https://bj.zu.ke.com/zufang/pg'

        for i in range(1, 101):
            yield scrapy.Request(
                url=base_url+str(i),
                meta={"api_url": api_url, "city_id": city_id},
                callback=self.parse    
            )



    def parse(self, response):
        api_url = response.meta["api_url"]
        city_id = response.meta["city_id"]
        houses = Selector(response).xpath('/html/body/div[3]/div[1]/div[5]/div[1]/div[1]/div/div/p[1]')
        
        for house in houses:
            house_link = house.xpath(
                'a/@href'
            ).extract()[0]

            house_code = house_link.split('/')[-1].strip('.html')

            url = api_url + house_code + city_id

            yield scrapy.Request(
                url=url, 
                callback=self.get_house,
                method="GET",
                headers={"Content-Type": "application/json"},
            )




    def get_house(self, response):
        res_json = json.loads(response.body)["data"]["recommend_list"]


        for house  in res_json:
            item = KeZuItem()
            item["info"] = house
            yield item




