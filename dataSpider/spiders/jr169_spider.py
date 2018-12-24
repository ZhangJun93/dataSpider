# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class JR169Spider(BaseSpider):
    name = "jr169_spider"
    website = u"金融169"
    allowed_domains = ['jr169.com']
    start_urls = ['http://www.jr169.com/']

    rules = [
        Rule(LinkExtractor(allow=(r'/[0-9]*.html'), deny=('/help')), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('/'), ), follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        content = ''
        try:
            title = response.xpath(r'//*[@class="title"]/h1//text()').extract()
            date = response.xpath(r'//*[@class="countBox"]/span[1]//text()').extract()
            try:
                date = date[1].strip()
            except:
                date = '01-01'
            content = response.xpath(r'//*[@class="con htmlcontent"]//text()').extract()
            loader.add_value('date', date)
            loader.add_value('title', title)
            loader.add_value('content', content)
        except Exception as e:
            self.logger.error('error url: %s error msg: %s' % (response.url, e))
            loader.add_value('date', '01-01')
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


