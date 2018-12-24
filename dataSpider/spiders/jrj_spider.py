# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem,spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class JRJSpider(BaseSpider):
    name = "jrj_spider"
    website = u"金融界"
    allowed_domains = ['jrj.com.cn']
    start_urls = ['http://www.jrj.com.cn/']

    rules = [
        Rule(LinkExtractor(allow=(r'.*shtml'),deny=(r'itougu', r'summary')), callback='parse_item'),
        Rule(LinkExtractor(allow=('/'), deny=(r'.*shtml')), callback=None, follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        date = '1970-01-01'
        content = ''
        try:
            title = response.xpath(r'//*[@class="titmain"]/h1//text()').extract()
            if title is None:
                title = response.xpath(r'//*[@class="texttitbox"]/h1//text()').extract()
            date_raw = response.xpath(r'//*[@class="inftop"]/span//text()').extract_first()
            if date_raw is None:
                date = response.xpath(r'//*[@class="time"]//text()').extract_first()
            if date_raw is not None:
                date = date_raw.strip().split(" ")[0]
            content = response.xpath(r'//*[@class="texttit_m1"]/p//text()').extract()
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


