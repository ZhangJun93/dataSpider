# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class DZFSYJQRSpider(BaseSpider):
    name = "dzfsyjqr_spider"
    website = u"电子发烧友-机器人论坛"
    allowed_domains = ['elecfans.com']
    start_urls = ['http://bbs.elecfans.com/zhuti_jiqiren_1.html']

    rules = [
       Rule(LinkExtractor(allow=('/zhuti_jiqiren')), follow=True),
       Rule(LinkExtractor(allow=(r'/jishu')), callback='parse_item'),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        content = ''
        try:
            title = response.xpath(r'//*[@id="thread_subject"]//text()').extract()
            date = response.xpath(r'//*[@class="bar_tip float_l"]/em//text()').extract_first()
            if date is not None:
                date = date.strip().split(" ")[0].strip()
            else:
                date = '1970-01-01'
            content = response.xpath(r'//*[@class="t_f"]//text() | //*[@class="message_box"]//text()').extract()
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

