# -*- coding: utf-8 -*-

import pymongo

class DeecampScraperPipeline:
    def __init__(self, mongo_uri, db_name, collection_name):
        self.mongo_uri = mongo_uri
        self.db_name = db_name
        self.collection_name = collection_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            db_name = getattr(crawler.spider, 'db_name'),
            collection_name = getattr(crawler.spider, 'collection_name')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item
