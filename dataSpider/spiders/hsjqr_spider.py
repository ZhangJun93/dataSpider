# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class HSJQRSpider(BaseSpider):
    name = "hsjqr_spider"
    website = u"华数机器人"
    allowed_domains = ['hsrobotics.cn']
    start_urls = ['http://www.hsrobotics.cn/news.html']

    rules = [
       Rule(LinkExtractor(allow=('/news1', '/news2', 'news3')), follow=True),
       Rule(LinkExtractor(allow=(r'/news-view.*html')), callback='parse_item'),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)

        content = ''
        try:
            title = response.xpath(r'//*[@class="news_htit"]//text()').extract()
            date = response.xpath(r'//*[@class="clearfix"]/span[1]//text()').extract_first()
            if date is not None:
                date = date.split(u"：")[1].strip()
            else:
                date = '1970-01-01'
            content = response.xpath(r'//*[@class="news_n_text"]//text()').extract()
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


