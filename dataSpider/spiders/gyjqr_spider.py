# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class GYJQRSpider(BaseSpider):
    name = "gyjqr_spider"
    website = u"工业机器人"
    allowed_domains = ['chuandong.com']
    start_urls = ['http://www.chuandong.com/p/robot/news.aspx']

    rules = [
        Rule(LinkExtractor(allow=(r'/news'), deny=(r'page=')), callback='parse_item'),
        Rule(LinkExtractor(allow=(r'/news.aspx')), follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        content = ''
        try:
            title = response.xpath(r'//*[@class="ns-tit"]//text()').extract()
            date = response.xpath(r'//*[@class="time mr30"]//text()').extract_first()
            if date is not None:
                date = date.strip().split(" ")[0]
            else:
                date = "1970年01月01日"
            content = response.xpath(r'//*[@class="ns-con-texts mt30"]//text()').extract()
            loader.add_value('title', title)
            loader.add_value('date', date)
            loader.add_value('content', content)
        except Exception as e:
            self.logger.error('error url: %s error msg: %s' % (response.url, e))
            loader.add_value('title', 'unknown')
            loader.add_value('date', "1970年01月01日")
            loader.add_value('content', '')
        finally:
            self.logger.info("crawled url: %s" % response.url)
            loader.add_value('url', response.url)
            loader.add_value('collection_name', self.name)
            loader.add_value("website", self.website)
            if content == '':
                self.logger.warning(' url: %s msg: %s' % (response.url, ' content is None'))
            yield loader.load_item()


