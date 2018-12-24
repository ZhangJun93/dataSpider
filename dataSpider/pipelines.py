# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import time
from pymongo import MongoClient
from hashlib import md5


class DataspiderPipeline(object):
    def __init__(self, mongo_db, mongo_username, mongo_password, mongo_ip, mongo_port, mongo_collection):
        self.mongo_db = mongo_db
        self.mongo_usrname = mongo_username
        self.mongo_pwd = mongo_password
        self.mongo_ip = mongo_ip
        if self.mongo_ip.find(',') != -1:
            self.mongo_ip = self.mongo_ip.split(',')
        self.mongo_port = mongo_port
        self.mongo_collection = mongo_collection
        self.client = MongoClient(host=self.mongo_ip, port=self.mongo_port)
        self.db = self.client[self.mongo_db]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_db=crawler.settings.get('MONGO_DATABASE'),
            mongo_username=crawler.settings.get('MONGO_USER'),
            mongo_password=crawler.settings.get('MONGO_PASSWORD'),
            mongo_ip=crawler.settings.get('MONGO_IP'),
            mongo_port=crawler.settings.get('MONGO_PORT'),
            mongo_collection=crawler.settings.get('MONGO_COLLECTION'),
        )

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        item['md5'] = self.spidermd5(item)
        item = dict(item)
        item['crawl_date'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
        # self.db[self.mongo_collection].update({'md5': item['md5'], 'date': item['date']}, {'$set': dict(item)}, True, True)     # 所有网站数据放在一个表
        self.db[item['collection_name']].update({'md5': item['md5'], 'date': item['date']}, {'$set': dict(item)}, True, True)     # 每个网站数据建立一个表

    def spidermd5(self, item):
        return md5((item['url']).encode('utf-8')).hexdigest()
