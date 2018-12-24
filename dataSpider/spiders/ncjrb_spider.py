# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class NCJRBSpider(BaseSpider):
    name = "ncjrb_spider"
    website = u"南昌金融办"
    allowed_domains = ['jrb.nc.gov.cn']
    start_urls = ['http://jrb.nc.gov.cn/']

    rules = [
        Rule(LinkExtractor(allow=(r'/ncjrb/tzgg/', r'/ncjrb/zcfg/', r'/ncjrb/gzdt/', r'/ncjrb/jryw/')),callback='parse_item', follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        content = ''
        try:
            title = response.xpath(r'//*[@class="h120 f20 bold"]//text()').extract_first()
            date_info = response.xpath(r'//*[@class="h120 f20 bold"]/div//text()').extract()
            date = '1970-01-01'
            if len(date_info) > 3:
                match = re.search(r'([0-9-]+)', date_info[3])
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


