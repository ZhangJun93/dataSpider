# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem,spidermd5, removern
from dataSpider.misc.baseSpider import BaseSpider
import time
import re


class ZGJRWSpider(BaseSpider):
    name = "zgjrw_spider"
    website = u"中国金融网"
    allowed_domains = ['financeun.com']
    start_urls = ['http://www.financeun.com/']

    rules = [
        Rule(LinkExtractor(allow=('/articleList/')), callback=None),       # 跟进articleList的链接
        Rule(LinkExtractor(allow=('/newsDetail/')), callback='parse_item', follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        date = "1970-01-01"
        try:
            title = response.xpath(r'//*[@class="content_left"]/div[@class="news"]/div//text()').extract_first()
            date_raw = response.xpath(r'//*[@class="copyright"]//text()').extract_first()
            if date_raw is not None:
                date = date_raw.split()[0]
                date = time.strptime(date, u"%Y年%m月%d日")
                date = time.strftime("%Y-%m-%d", date)
            content = response.xpath(r'//*[@class="news_content"]/p//text()').extract()

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

