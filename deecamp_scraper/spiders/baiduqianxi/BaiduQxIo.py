# -*- coding: utf-8 -*-
import scrapy
import json
from datetime import date, timedelta
from ...items.baiduqianxi.baiduqxio import BaiduQxInOutItem
from scrapy.utils.project import get_project_settings



class BaiduQxIoSpider(scrapy.Spider):
    name = 'BaiduQxIoSpider'
    allowed_domains = ['http://huiyan.baidu.com']
    db_name = 'baiduqx'
    collection_name = 'inout'
    
    def start_requests(self):
  
        settings = get_project_settings()
        city_codes_path = settings.get('BAIDU_CITY_CODE_DICT_FILE')
        with open(city_codes_path) as f:
            city_codes = json.load(f).values()

        dates = []
        start_date =  date(2019,6,15)
        end_date = date(2019,6,18)
        for n in range(int((end_date - start_date).days+1)):
            dates.append((start_date + timedelta(n)).strftime('%Y%m%d'))
        
        urls = []
        print(city_codes, dates)
        for city_code in city_codes:
            for date in dates:
                urls.append(('https://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id={}&type=move_in&date={}'.format(city_code, date), date, city_code))

        print(urls)
        for url in urls:
            print(url)
            yield scrapy.Request(
                url=url[0], 
                meta={"date": url[1], "city_code":url[2]},
                callback=self.parse,
                method="GET",
                headers={"Content-Type": "application/json"},
            )


    def parse(self, response):
        city_in = json.loads(response.body.decode("utf-8").strip(r'cb(').strip(r')'))["data"]
        date = response.meta["date"]
        city_code = response.meta["city_code"]

        item = BaiduQxInOutItem()
        item["city_in"] = city_in

        city_out_url = 'http://huiyan.baidu.com/migration/cityrank.jsonp?dt=city&id={}&type=move_out&date={}'.format(city_code, date)


        yield scrapy.Request(url=city_out_url,
            meta={"item": item},
            callback=self.getOut,
            method="GET",
            headers={"Content-Type": "application/json"},
        )

    def getOut(self, response):
        item = response.meta["item"]
        city_out = json.loads(response.body.decode("utf-8").strip(r'cb(').strip(r')'))["data"]

        item["city_out"] = city_out

        yield item

