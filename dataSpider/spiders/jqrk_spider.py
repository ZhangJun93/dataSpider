# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem,spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class JQRKSpider(BaseSpider):
    name = "jqrk_spider"
    website = u"机器人库"
    allowed_domains = ['jiqirenku.com']
    start_urls = ['http://www.jiqirenku.com/']

    rules = [
        Rule(LinkExtractor(allow=('/'), deny='/wp-login'), callback='parse_item', follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        if response.body.find('加载更多') != -1:
            next_urls = response.xpath(r'//*[@class="next next_page"]/a/@href').extract()
            # print "****************test", response.url, next_urls
            for next_url in next_urls:
                yield Request(next_url.strip())
        else:
            loader = ItemLoader(item=SpiderItem(), response=response)
            date = '1970-01-01'
            try:
                title = response.xpath(r'//*[@class="single-post__title"]//text()').extract_first()
                # 从url中提取日期
                match = re.match(".*com/([0-9]*)/([0-9]*)/([0-9]*)/.*html", response.url)
                if match:
                    date = match.group(1) + '-' + match.group(2) + '-' + match.group(3)
                content = response.xpath(r'//*[@class="article"]//text()').extract()
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


