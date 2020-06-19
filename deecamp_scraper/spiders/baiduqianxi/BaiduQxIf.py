# -*- coding: utf-8 -*-
import scrapy
import json
import datetime
from datetime import timedelta
from scrapy.utils.project import get_project_settings
from ...items.baiduqianxi.baiduqxif import BaiduQXInternalFlowItem



class BaiduQxIfSpider(scrapy.Spider):
    name = 'BaiduQxIfSpider'
    allowed_domains = ['huiyan.baidu.com']
    db_name = 'baiduqx'
    collection_name = 'internalflow'
    
    def start_requests(self):
  
        settings = get_project_settings()
        city_codes_path = settings.get('BAIDU_CITY_CODE_DICT_FILE')
        with open(city_codes_path) as f:
            city_codes = json.load(f).values()

        dates = []
        start_date =  datetime.date(2020,1,15)
        end_date = datetime.date(2020,1,20)
        for n in range(int((end_date - start_date).days+1)):
            dates.append((start_date + timedelta(n)).strftime('%Y%m%d'))
        
        urls = []
        for city_code in city_codes:
            for date in dates:
                urls.append('https://huiyan.baidu.com/migration/internalflowhistory.jsonp?dt=city&id={}&date={}'.format(city_code, date))

        for url in urls:
            yield scrapy.Request(
                url=url, 
                callback=self.parse,
                method="GET",
                errback=self.errback_web,
                headers={"Content-Type": "application/json"},
            )



    def parse(self, response):
        internal_flow = json.loads(response.body.decode("utf-8").strip(r'cb(').strip(r')'))["data"]

        item = BaiduQXInternalFlowItem()
        item["internal_flow"] = internal_flow

        yield item

    def errback_web(self, failure):
        # log all failures
        self.logger.error(repr(failure))
        item ={}
        item['Web Address']= failure.request.url
        yield item
