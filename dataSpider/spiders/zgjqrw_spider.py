# -*- coding: utf-8 -*-
import re
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import Request, CrawlSpider
from scrapy.loader import ItemLoader
from dataSpider.items import SpiderItem
from dataSpider.misc.baseSpider import BaseSpider

from ..misc.baseSpider import BaseSpider


class ZGJQRWSpider(BaseSpider):
    name = "zgjqrw_spider"
    website = u"中国机器人网"
    allowed_domains = ['robot-china.com']
    start_urls = ['http://www.robot-china.com/news/list-937.html', 'http://www.robot-china.com/zhuanti/list-187.html',
                  'http://www.robot-china.com/zhuanti/list-189.html', 'http://www.robot-china.com/zhuanti/list-188.html',
                  'http://www.robot-china.com/zhuanti/list-190.html']

    rules = [
        Rule(LinkExtractor(allow=(r'/news', r'/zhuanti')), callback='parse_item', follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,
    }

    def parse_item(self, response):
        next_url = response.xpath(r'//*[@class="next"]/@href').extract_first()
        if next_url is not None:
            yield Request(next_url)
        else:
            loader = ItemLoader(item=SpiderItem(), response=response)
            content = ''
            try:
                title = response.xpath(r'//*[@class="left plleft"]/div[@class="zx3"]/h3//text()').extract_first()
                date = response.xpath(r'//*[@id="plshare"]/li[2]//text()').extract_first()
                date = date.split(u'：')[1]     # 过滤并获取日期
                content = response.xpath(r'//*[@id="article"]/div//text()').extract()
                if len(content) == 0:
                    content = response.xpath(r'//*[@id="article"]/p//text()').extract()
                # print title, date, len(content), "****************"
                loader.add_value('title', title)
                loader.add_value('date', date)
                loader.add_value("content", content)
            except Exception as e:
                self.logger.error('error url: %s error msg: %s' % (response.url, e))
                loader.add_value('date', '1970-01-01')
                loader.add_value('title', 'unknown')
                loader.add_value("content", "")
            finally:
                self.logger.info("crawled url: %s" % response.url)
                loader.add_value('url', response.url)
                loader.add_value('collection_name', self.name)
                loader.add_value("website", self.website)
                if content == '':
                    self.logger.warning(' url: %s msg: %s' % (response.url, 'content is None'))
                yield loader.load_item()
