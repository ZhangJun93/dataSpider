# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class BXJQRSpider(BaseSpider):
    name = "bxjqr_spider"
    website = u"百星机器人"
    allowed_domains = ['bxrobot.net']
    start_urls = ['http://www.bxrobot.net/index/news/cid/2.html']

    rules = [
        Rule(LinkExtractor(allow=(r'/news_xq/')), callback='parse_item'),
       Rule(LinkExtractor(allow=('/news/cid')), follow=True),

    ]


    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        # use default date
        date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        content = ''
        try:
            title = response.xpath(r'//*[@class="wayc"]//text()').extract()

            content = response.xpath(r'//*[@class="con"]/p//text()').extract()
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
            loader.add_value('date', date)
            loader.add_value('collection_name', self.name)
            loader.add_value("website", self.website)
            if content == '':
                self.logger.warning(' url: %s msg: %s' % (response.url, ' content is None'))
            yield loader.load_item()


