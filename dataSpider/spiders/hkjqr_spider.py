# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class HKJQRSpider(BaseSpider):
    name = "hkjqr_spider"
    website = u"海康机器人"
    allowed_domains = ['hikrobotics.com']
    start_urls = ['http://www.hikrobotics.com/media/news.htm']

    rules = [
       Rule(LinkExtractor(allow=('/news.htm')), callback='parse_next_page', follow=True),
       Rule(LinkExtractor(allow=(r'/news_detail.htm.*')), callback='parse_item'),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_next_page(self, response):
        page_num = 26
        base_url = "http://www.hikrobotics.com/media/news.htm?pageNo="
        for i in range(2, page_num+1):
            next_url = base_url + str(i)
            yield Request(next_url)

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        # use default date
        date = time.strftime("%Y-%m-%d", time.localtime(time.time()))
        content = ''
        try:
            title = response.xpath(r'//*[@class="con_news"]/h1//text()').extract()
            content = response.xpath(r'//*[@class="con_news"]/section//text() | //*[@class="con_news"]/p//text()').extract()
            loader.add_value('title', title)
            loader.add_value('content', content)
        except Exception as e:
            self.logger.error('error url: %s error msg: %s' % (response.url, e))
            loader.add_value('title', 'unknown')
            loader.add_value('content', '')
        finally:
            self.logger.info("crawled url: %s" % response.url)
            loader.add_value('url', response.url)
            loader.add_value('collection_name', self.name)
            loader.add_value('date', date)
            loader.add_value("website", self.website)
            if content == '':
                self.logger.warning(' url: %s msg: %s' % (response.url, ' content is None'))
            yield loader.load_item()


