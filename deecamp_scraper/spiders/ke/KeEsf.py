# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json
import ast
from scrapy.utils.project import get_project_settings
from ...items.ke.esf import KeEsfItem

class KeEsfSpider(scrapy.Spider):
    name = 'KeEsfSpider'
    allowed_domains = ['ke.com']
    db_name = 'ke'
    collection_name = 'esf'

    def __init__(self, name=None, page_num=0, city_name="", **kwargs):
        super().__init__(name=name, **kwargs)
        self.page_num = int(page_num)
        self.city_name = city_name

    def start_requests(self):
        settings = get_project_settings()
        ke_list_path = settings.get('KE_LIST_FILE')
        with open(ke_list_path) as f:
            ke_list = json.load(f)


        api_url = ke_list[self.city_name] + '/ershoufang/esfrecommend?id='  
        base_url = ke_list[self.city_name] + '/ershoufang/pg'

        for i in range(1, self.page_num):
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




