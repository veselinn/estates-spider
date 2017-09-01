# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html1

import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        db = connection[settings['MONGODB_DB']]
        self.estate_collection = db[settings['MONGODB_COLLECTION']]
        self.new_estates = []

    def process_item(self, item, spider):
        for data in item:
            if not data:
                raise DropItem("Missing data!")
        update_result = self.estate_collection.update({'url': item['url']}, dict(item), upsert=True)

        if not update_result['updatedExisting']:
            self.new_estates.append(item)
        
        print("Estate added to MongoDB1 database!")
        return item

    def close_spider(self, spider):
        print("Closing spider ... ")
        print("New estates " + str(self.new_estates))
        connection.close()
