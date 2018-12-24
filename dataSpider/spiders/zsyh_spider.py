# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem,spidermd5, removern
from dataSpider.misc.baseSpider import BaseSpider
import time
import re


url_date_dict = {}


class ZSYHSpider(BaseSpider):
    name = "zsyh_spider"
    website = u"招商银行"
    allowed_domains = ['cmbchina.com']
    start_urls = ['http://www.cmbchina.com/cmbinfo/news/']

    rules = [
        Rule(LinkExtractor(allow=('/news')), callback='parse_item', follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,
    }

    def parse_item(self, response):
        url = response.url
        # 获取新闻时间
        if re.match(".*PageNo=.*", url):
            date_list = response.xpath(r'//*[@id="column_content"]/div[2]/div[1]/ul/li/span[2]//text()').extract()
            title_list = response.xpath(r'//*[@id="column_content"]/div[2]/div[1]/ul/li/span[1]/a//text()').extract()
            url_list = response.xpath(r'//*[@id="column_content"]/div[2]/div[1]/ul/li/span[1]/a/@href').extract()
            # print len(title_list), len(date_list), len(url_list)
            # print title_list[0], date_list[0], url_list[0]
            for idx, temp_url in enumerate(url_list):
                final_url = 'http://www.cmbchina.com/cmbinfo/news/' + temp_url.strip()
                md5 = spidermd5(final_url)
                url_date_dict[md5] = [title_list[idx], date_list[idx]]
            return
        # 获取新闻正文
        loader = ItemLoader(item=SpiderItem(), response=response)
        date = "1970-01-01"
        try:
            title = response.xpath(r'//*[@id="column_content"]/div[1]/span//text()').extract()
            # content = response.xpath(r'//*[@id="column_content"]/div[2]/div/p//text()').extract()
            # update
            content = response.xpath(r'//*[@id="column_content"]/div[2]/div//text()').extract()

            if spidermd5(url) in url_date_dict.keys():
                date = url_date_dict[spidermd5(url)][1][1:-2]

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

