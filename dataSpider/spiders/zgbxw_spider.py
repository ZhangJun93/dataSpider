# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class ZGBXWSpider(BaseSpider):
    name = "zgbxw_spider"
    website = u"中国保险网"
    allowed_domains = ['china-insurance.com']
    start_urls = ['http://www.china-insurance.com/']

    rules = [
        Rule(LinkExtractor(allow=(r'/newslist.asp?',)), callback='parse_item'),
        Rule(LinkExtractor(allow=(r'/news-center/',  r'/social/', r'/case/',)), follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        content = ''
        try:
            title = response.xpath(r'//*[@class="f20b"]//text()').extract()
            date_info = response.xpath(r'//td[@align="center"]//text()').extract()
            date_info = removern(date_info)
            match = re.search(u'([0-9]+)年([0-9]+)月([0-9]+)日', date_info)
            if match:
                date = match.group(1) + '-' + match.group(2) + '-' + match.group(3)
            else:
                date = '1970-01-01'
            content = response.xpath(r'//*[@id="zoom"]//text()').extract()
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


