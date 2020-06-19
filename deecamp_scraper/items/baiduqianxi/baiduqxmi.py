import scrapy 

class BaiduQxMigrationIndexItem(scrapy.Item):
    immigration_index = scrapy.Field()
    emmigration_index = scrapy.Field()

