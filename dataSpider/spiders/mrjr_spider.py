# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem,spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class MRJRSpider(BaseSpider):
    name = "mrjr_spider"
    website = u"每日金融"
    allowed_domains = ['meirijinrong.com']
    start_urls = ['http://www.meirijinrong.com/']

    rules = [
        Rule(LinkExtractor(allow=(r'.*html')), callback='parse_item'),
        Rule(LinkExtractor(allow=( '/news', '/guandian/', '/event')), callback=None, follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        date = '1970-01-01'
        content = ''
        try:
            title = response.xpath(r'//*[@class="title"]//text()').extract()
            date_raw = response.xpath(r'//*[@class="info"]//text()').extract()
            if date_raw is not None:
                date = date_raw[0].strip().split(" ")[1]
            content = response.xpath(r'//*[@class="text"]//text()').extract()
            loader.add_value('date', date)
            loader.add_value('title', title)
            loader.add_value('content', content)
        except Exception as e:
            self.logger.error('error url: %s error msg: %s' % (response.url, e))
            loader.add_value('date', date)
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


