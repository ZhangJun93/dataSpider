# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem, spidermd5, removern
import time
from dataSpider.misc.baseSpider import BaseSpider
import re


class JTYHSpider(BaseSpider):
    name = "jtyh_spider"
    website = u"交通银行"
    allowed_domains = ['bankcomm.com']
    start_urls = ['http://www.bankcomm.com/BankCommSite/shtml/jyjr/cn/7158/7162/list_1.shtml?channelId=7158']

    rules = [
        Rule(LinkExtractor(allow=('/list_')), callback='parse_next_page', follow=True),
        Rule(LinkExtractor(allow=(r'/'), deny=(r'/report', r'/7226')), callback='parse_item'),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,    # 1小时后自动关闭
    }

    def parse_next_page(self, response):
        next_info = response.xpath(r'//*[@class="hint"]//@href').extract()[-1]
        match = re.search(r'list_([0-9]+)', next_info)
        match_url = re.search(r'(.*list_)[0-9]+(\.shtml.*)', response.url)
        if match and match_url:
            end_url_index = int(match.group(1))
            for i in range(1, end_url_index+1):
                next_url = match_url.group(1) + str(i) + match_url.group(2)
                yield Request(next_url)


    def parse_item(self, response):
        loader = ItemLoader(item=SpiderItem(), response=response)
        content = ''
        try:
            title = response.xpath(r'//*[@class="news-block"]/h2//text()').extract()

            date = response.xpath(r'//*[@class="time"]/span//text()').extract()
            date = removern(date)
            match = re.search(r'([0-9-]+)', date)
            if match:
                date = match.group(1)
            else:
                date = '1970-01-01'
            content = response.xpath(r'//*[@class="show_main c_content"]//text()').extract()
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


