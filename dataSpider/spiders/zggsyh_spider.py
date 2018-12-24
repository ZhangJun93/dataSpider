# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class ZGGSYHSpider(BaseSpider):
    name = "zggsyh_spider"
    website = u"中国工商银行"
    allowed_domains = ['icbc.com.cn']
    start_urls = ['http://www.icbc.com.cn/ICBC/%E9%87%91%E8%9E%8D%E5%B8%82%E5%9C%BA%E4%B8%93%E5%8C%BA/%E8%B5%84%E8%AE%AF%E4%B8%AD%E5%BF%83/%E5%B7%A5%E8%A1%8C%E7%9C%8B%E5%B8%82%E5%9C%BA/default.htm',
                  'http://www.icbc.com.cn/ICBC/%E9%87%91%E8%9E%8D%E5%B8%82%E5%9C%BA%E4%B8%93%E5%8C%BA/%E8%B5%84%E8%AE%AF%E4%B8%AD%E5%BF%83/%E5%B8%82%E5%9C%BA%E8%BF%B0%E8%AF%84/default.htm']

    rules = [
        Rule(LinkExtractor(allow=(r'/default')), follow=True),
        Rule(LinkExtractor(allow=(r'[0-9].htm')), callback='parse_item'),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        content = ''
        try:
            title = response.xpath(r'//*[@class="dianzititle"]//text()').extract()
            date = response.xpath(r'//*[@id="InfoPickFromFieldControl"]//text()').extract_first()
            match = re.search(r'([0-9-]+)', date)
            if match:
                date = match.group(1)
            else:
                date = '1970-01-01'
            content = response.xpath(r'//*[@id="FreePlaceHoldersControl1"]//text()').extract()
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


