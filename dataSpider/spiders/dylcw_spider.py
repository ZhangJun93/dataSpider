# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class DYLCWSpider(BaseSpider):
    name = "dylcw_spider"
    website = u"第一理财网"
    allowed_domains = ['amoney.com.cn']
    start_urls = ['http://www.amoney.com.cn/stock.shtml',
                  'http://www.amoney.com.cn/fund/',
                  'http://www.amoney.com.cn/bank.shtml',
                  'http://www.amoney.com.cn/trust.shtml',
                  'http://www.amoney.com.cn/instrance.shtml',
                  'http://www.amoney.com.cn/finance.shtml',
                  'http://www.amoney.com.cn/article_list/1101_0.html']

    rules = [
        Rule(LinkExtractor(allow=('/article_list/')), follow=True),
        Rule(LinkExtractor(allow=(r'/article_detail/')), callback='parse_item'),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        content = ''
        try:
            title = response.xpath(r'//*[@class="border newsdetail space"]/h1//text()').extract()
            date = response.xpath(r'//*[@class="source"]//text()').extract()
            date = removern(date)
            match = re.search(r'([0-9-]+)', date)
            if match:
                date = match.group(1)
            else:
                date = '1970-01-01'
            content = response.xpath(r'//*[@class="content"]//text()').extract()
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


