import scrapy 

class BaiduQxInOutItem(scrapy.Item):
    city_in = scrapy.Field()
    city_out = scrapy.Field()

