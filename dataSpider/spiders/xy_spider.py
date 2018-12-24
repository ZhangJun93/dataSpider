# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class XYSpider(BaseSpider):
    name = "xy_spider"
    website = u"新芽网"
    allowed_domains = ['newseed.cn']
    start_urls = ['https://news.newseed.cn/']

    rules = [
        Rule(LinkExtractor(allow=(r'/p[0-9]+')), follow=True),
        Rule(LinkExtractor(allow=(r'/[0-9]+')), callback='parse_item'),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        content = ''
        try:
            title = response.xpath(r'//*[@id="title"]//text()').extract()
            date = response.xpath(r'//*[@class="date"]//text()').extract_first()
            if date is not None:
                date = date.split(" ")[0].strip()
            else:
                date = '1970-01-01'
            content = response.xpath(r'//*[@class="news-content"]//text()').extract()
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


