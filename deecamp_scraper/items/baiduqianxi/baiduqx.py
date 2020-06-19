import scrapy 

class BaiduQXItem(scrapy.Item):
    city_in = scrapy.Field()
    city_out = scrapy.Field()
    migration_index = scrapy.Field()
    internal_flow = scrapy.Field()

