# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json
from ...items.zillow.buy import ZillowBuyItem

class ZillowBuySpider(scrapy.Spider):
    name = 'ZillowBuySpider'
    allowed_domains = ['zillow.com']
    page_num = 1
    start_urls = ['https://www.zillow.com/homes/{}_p/'.format(str(page_num))]
    db_name = 'zillow'
    collection_name = 'buy'

    def parse(self, response):
        houses = Selector(response).xpath('/html/body/div[1]/div[5]/div/div[1]/div/div[1]/ul/li/article')

        for house in houses:
            item = ZillowBuyItem()

            house_link = house.xpath(
                'div[2]/a/@href'
            ).extract()[0]
            house_link = house_link.split('/')[-2].strip('_zpid')
            
            info_url = 'https://www.zillow.com/graphql/?zpid=' + house_link + \
                '&contactFormRenderParameter=&queryId=f04703b7a1f4f2f9722b3a568e469622&operationName=ForSaleDoubleScrollFullRenderQuery'
            price_url = 'https://www.zillow.com/graphql/?zpid=' + house_link + \
                '&timePeriod=TEN_YEARS&metricType=LOCAL_HOME_VALUES&forecast=true&operationName=HomeValueChartDataQuery'


            yield scrapy.Request(url=info_url,
                meta={"item": item, "price_url": price_url},
                callback=self.getHouse,
                method="POST",
                headers={"Content-Type": "application/json"},
                body=r'{"operationName":"ForSaleDoubleScrollFullRenderQuery","variables":{"zpid":31533266,"contactFormRenderParameter":{"zpid":31533266,"platform":"desktop","isDoubleScroll":true}},"clientVersion":"home-details/6.0.11.1378.master.b7c3cff","queryId":"f04703b7a1f4f2f9722b3a568e469622"}'
            )

        self.page_num += 1
        for _ in range(1000):
            print('https://www.zillow.com/homes/{}_p/'.format(str(page_num)))
        yield scrapy.Request(url='https://www.zillow.com/homes/{}_p/'.format(str(page_num)),
            callback=self.parse    
        )
       

    
    def getHouse(self, response):
        item = response.meta["item"]
        info_json = json.loads(response.body)["data"]
        item["info"] = info_json

        price_url = response.meta["price_url"]
        
        yield scrapy.Request(url=price_url,
            meta={"item": item},
            callback=self.getPrice,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=r'{"query":"query HomeValueChartDataQuery($zpid: ID!, $metricType: HomeValueChartMetricType, $timePeriod: HomeValueChartTimePeriod) {\n  property(zpid: $zpid) {\n    homeValueChartData(metricType: $metricType, timePeriod: $timePeriod) {\n      points {\n        x\n        y\n      }\n      name\n    }\n  }\n}\n","operationName":"HomeValueChartDataQuery","variables":{"zpid":30638302,"timePeriod":"TEN_YEARS","metricType":"LOCAL_HOME_VALUES","forecast":true},"clientVersion":"home-details/6.0.11.1378.master.b7c3cff"}'
        ) 

    def getPrice(self, response):
        item = response.meta["item"]
        price_json = json.loads(response.body)["data"]
        item["price_change"] = price_json

        yield item

