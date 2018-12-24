# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class JYJQRSpider(BaseSpider):
    name = "jyjqr_spider"
    website = u"家用机器人"
    allowed_domains = ['eeworld.com.cn']
    start_urls = ['http://www.eeworld.com.cn/tags/%E5%AE%B6%E7%94%A8%E6%9C%BA%E5%99%A8%E4%BA%BA']

    rules = [
        Rule(LinkExtractor(allow=('/news')), follow=True),
        Rule(LinkExtractor(allow=(r'/article')), callback='parse_item'),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        content = ''
        try:
            title = response.xpath(r'//*[@class="font36px fontw"]//text()').extract()
            date = response.xpath(r'//*[@class="txtc4 font12px"]//text()').extract_first()
            date = removern(date)
            if date is None:
                date = '1970-01-01'
            content = response.xpath(r'//*[@class="newscontxt"]//text()').extract()
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


