import scrapy 

class FangEsfItem(scrapy.Item):
    info = scrapy.Field()
    price_change = scrapy.Field()

