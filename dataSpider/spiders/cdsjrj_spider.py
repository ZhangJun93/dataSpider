# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class CDSJRJSpider(BaseSpider):
    name = "cdsjrj_spider"
    website = u"成都市金融工作局"
    allowed_domains = ['cdjr.gov.cn']
    start_urls = ['http://www.cdjr.gov.cn/']

    rules = [
        Rule(LinkExtractor(allow=(r'/content')), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=('/c138993/', '/c138998/')), follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        content = ''
        try:
            title = response.xpath(r'//*[@class="lh-newsRes-h1"]//text()').extract()
            date = response.xpath(r'//*[@class="lh-newsRes-time left"]//text()').extract()
            try:
                date = date[1].strip().split(" ")[0]
            except:
                date = '1970-01-01'
            content = response.xpath(r'//*[@class="lh-news-info clearfix"]//text()').extract()
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
