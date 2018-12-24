# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class ZHJQRSpider(BaseSpider):
    name = "btbzj_spider"
    website = u"比特币之家"
    allowed_domains = ['btc798.com']
    start_urls = ['http://www.btc798.com/cate/0']

    rules = [
        Rule(LinkExtractor(allow=(r'/Home/p/')), follow=True),
        Rule(LinkExtractor(allow=(r'/articles/')), callback='parse_item'),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        content = ''
        try:
            title = response.xpath(r'//*[@class="summi"]/h1//text()').extract()
            date = response.xpath(r'//*[@class="summi"]/ul/li[1]//text()').extract()
            if date is None:
                date = date.split(" ")[0].strip()
            else:
                date = '1970-01-01'
            content = response.xpath(r'//*[@class="summs"]//text()').extract()
            loader.add_value('date', date)
            loader.add_value('title', title)
            loader.add_value('content', content)
        except Exception as e:
            self.logger.error('error url: %s error msg: %s' % (response.url, e))
            loader.add_value('date', '1970-01-01')
            loader.add_value('title', 'unknown')
            loader.add_value('content', '')
        finally:
            self.logger.info("crawled url: %s" % response.url)
            loader.add_value('url', response.url)
            loader.add_value('collection_name', self.name)
            loader.add_value("website", self.website)
            if content == '':
                self.logger.warning(' url: %s msg: %s' % (response.url, ' content is None'))
            yield loader.load_item()


