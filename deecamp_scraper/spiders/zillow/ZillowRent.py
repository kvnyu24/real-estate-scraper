# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
import json
from ...items.zillow.rent import ZillowRentItem

class ZillowRentSpider(scrapy.Spider):
    name = 'ZillowRentSpider'
    allowed_domains = ['zillow.com']
    page_num = 1
    start_urls = ['https://www.zillow.com/homes/for_rent/{}_p/'.format(str(page_num))]
    db_name = 'zillow'
    collection_name = 'rent'

    def parse(self, response):
        houses = Selector(response).xpath('/html/body/div[1]/div[5]/div/div[1]/div/div[1]/ul/li/article')

        for house in houses:
            item = ZillowRentItem()

            house_link = house.xpath(
                'div[2]/a/@href'
            ).extract()[0]
            house_link = house_link.split('/')[-2].strip('_zpid')
            
            info_url = 'https://www.zillow.com/graphql/?zpid=' + house_link + \
                '&contactFormRenderParameter=&queryId=394ed3300bcc9b921171ac74aa6d56c9&operationName=ForRentDoubleScrollFullRenderQuery'
            price_url = 'https://www.zillow.com/graphql/?zpid=' + house_link + \
                '&timePeriod=FIVE_YEARS&metricType=LOCAL_RENTAL_RATES&forecast=true&operationName=HomeValueChartDataQuery'


            yield scrapy.Request(url=info_url,
                meta={"item": item, "price_url": price_url},
                callback=self.get_house,
                method="POST",
                headers={"Content-Type": "application/json"},
                body=r'{"operationName":"ForRentDoubleScrollFullRenderQuery","variables":{"zpid":2079087470,"contactFormRenderParameter":{"zpid":2079087470,"platform":"desktop","isDoubleScroll":true}},"clientVersion":"home-details/6.0.11.1378.master.b7c3cff","queryId":"394ed3300bcc9b921171ac74aa6d56c9"}'
            )
        
        self.page_num += 1
        yield scrapy.Request(url='https://www.zillow.com/homes/for_rent/{}_p/'.format(str(page_num)),
            callback=self.parse    
        )
       

    
    def get_house(self, response):
        item = response.meta["item"]
        info_json = json.loads(response.body)["data"]
        item["info"] = info_json

        price_url = response.meta["price_url"]
        
        yield scrapy.Request(url=price_url,
            meta={"item": item},
            callback=self.get_price,
            method="POST",
            headers={"Content-Type": "application/json"},
            body=r'{"query":"query HomeValueChartDataQuery($zpid: ID!, $metricType: HomeValueChartMetricType, $timePeriod: HomeValueChartTimePeriod) {\n  property(zpid: $zpid) {\n    homeValueChartData(metricType: $metricType, timePeriod: $timePeriod) {\n      points {\n        x\n        y\n      }\n      name\n    }\n  }\n}\n","operationName":"HomeValueChartDataQuery","variables":{"zpid":2079087470,"timePeriod":"FIVE_YEARS","metricType":"LOCAL_RENTAL_RATES","forecast":true},"clientVersion":"home-details/6.0.11.1378.master.b7c3cff"}'
        )

    def get_price(self, response):
        item = response.meta["item"]
        price_json = json.loads(response.body)["data"]
        item["price_change"] = price_json

        yield item

