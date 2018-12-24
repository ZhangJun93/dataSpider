# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class XZLJQRSpider(BaseSpider):
    name = "xzljqr_spider"
    website = u"新战略机器人网"
    allowed_domains = ['xzlrobot.com']
    start_urls = ['http://www.xzlrobot.com/']

    rules = [
        Rule(LinkExtractor(allow=('/cs-chanyezixun', '/cs-chanyelian', '/cs-yingyongxingye', '/cs-chanpinfenlei', '/cs-zibenfengyun', '/cs-zhinangtuan')), follow=True),
        Rule(LinkExtractor(allow=(r'.*html')), callback='parse_item', follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)

        content = ''
        try:
            title = response.xpath(r'//*[@class="articleTitle"]//text()').extract()
            date = response.xpath(r'//*[@class="articleTime"]/span//text()').extract_first()
            if date is not None:
                date = date.strip().split(" ")[1]
            else:
                date = '1970-01-01'
            content = response.xpath(r'//*[@class="articleFontSize_medium"]//text()').extract()
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


