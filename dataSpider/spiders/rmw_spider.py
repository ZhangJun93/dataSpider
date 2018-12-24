# -*- coding: utf-8 -*-
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.spiders import CrawlSpider, Request
from ..items import SpiderItem,spidermd5, removern
from dataSpider.items import SpiderItem
from dataSpider.misc.baseSpider import BaseSpider
import time
import re


class RMWSpider(BaseSpider):
    name = "rmw_spider"
    website = u"人民网金融"
    allowed_domains = ['money.people.com.cn', 'finance.people.com.cn']
    start_urls = ['http://money.people.com.cn/bank/', 'http://money.people.com.cn/insurance/',
                  'http://money.people.com.cn/GB/392426/index.html', 'http://finance.people.com.cn/fund/',
                  'http://money.people.com.cn/GB/397730/index.html', 'http://money.people.com.cn/stock/GB/index.html']



    rules = [
       # Rule(LinkExtractor(allow=(r'money|finance.*/n1/', r'')), callback='parse_item', follow=True),
        Rule(LinkExtractor(allow=(r'/')), callback='parse_item', follow=True),
    ]

    custom_settings = {
        'CLOSESPIDER_TIMEOUT': 3600,
    }

    def parse_item(self, response):
        if response.body.find(u'下一页') != -1:
            # 提取下一页url
            next_urls = response.xpath(r'//*[@class="page_n clearfix"]/a/@href').extract()

            if len(next_urls) > 0:
                if re.search("index", response.url):
                    match = re.match("(.*/)index.*", response.url)
                    next_url = match.group(1) + next_urls[-1]
                else:
                    next_url = response.url + next_urls[-1]
                yield Request(next_url)
        else:
            loader = ItemLoader(item=SpiderItem(), response=response)
            content = ''
            try:
                # 抓取网页信息
                title = response.xpath(r'//*[@class="clearfix w1000_320 text_title"]/h1//text()').extract()
                content = response.xpath(r'//*[@id="rwb_zw"]/p//text()').extract()
                date = response.xpath(r'//*[@class="box01"]/div[@class="fl"]//text()').extract_first()

                if title is None or len(title) == 0:
                    title = response.xpath(r'//*[@id="p_title"]//text()').extract()  # 匹配不同模版
                    # eg. http://finance.people.com.cn/fund/n/2015/0918/c201329-27601887.html
                if content is None or len(content) == 0:
                    content = response.xpath(r'//*[@id="p_content"]/p//text()').extract()
                if date is None or len(date) == 0:
                    date = response.xpath(r'//*[@id="p_publishtime"]//text()').extract_first()
                if date is None:
                    date = '1970-01-01'
                else:
                    date = date.split()[0]
                    match = re.match(u'(.*日).*', date)
                    date = match.group(1)
                    # 转换时间格式
                    date = time.strptime(date, u"%Y年%m月%d日")
                    date = time.strftime("%Y-%m-%d", date)

                loader.add_value('date', date)
                loader.add_value('title', title)
                loader.add_value('content', content)
            except Exception as e:
                self.logger.error('error url: %s error msg: %s' % (response.url, e))
                loader.add_value('date', '1970-01-01')
                loader.add_value('title', "unknown")
                loader.add_value('content', '')
            finally:
                self.logger.info("crawled url: %s" % response.url)
                loader.add_value('url', response.url)
                loader.add_value('collection_name', self.name)
                loader.add_value("website", self.website)
                if content == '':
                    self.logger.warning(' url: %s msg: %s' % (response.url, ' content is None'))
                yield loader.load_item()