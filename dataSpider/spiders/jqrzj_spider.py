# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem,spidermd5, removern
from dataSpider.misc.baseSpider import BaseSpider
import time
import re


class JQRZJSpider(BaseSpider):
    name = "jqrzj_spider"
    website = u"机器人之家"
    allowed_domains = ['jqr.com']
    start_urls = ['https://www.jqr.com/industry', 'https://www.jqr.com/service']

    rules = [
        Rule(LinkExtractor(allow=('/news/')), callback='parse_item', follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,
    }

    def parse_item(self, response):
        if response.body.find('class="pager"') != -1:
            # 提取下一页url
            url_list = response.xpath(r'//ul[@class="pager"]/li/a/@href').extract()
            if len(url_list) >= 1:
                next_url = 'https://www.jqr.com' + url_list[-1]
                yield Request(next_url)

        else:
            loader = ItemLoader(item=SpiderItem(), response=response)
            date = "1970-01-01"
            try:
                title = response.xpath(r'//*[@class="mb20 color-333 u-clamp1 fz24"]//text()').extract_first()
                date_raw = response.xpath(r'//*[@class="color-666"]/span[4]//text()').extract_first()
                if date_raw is not None:
                    date = date_raw.split()[0]
                content = response.xpath(r'//*[@class="fmt md-fmt mt30 mb30"]/p//text()').extract()
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
                    self.logger.warning(' url: %s msg: %s' % (response.url, 'content is None'))
                yield loader.load_item()
