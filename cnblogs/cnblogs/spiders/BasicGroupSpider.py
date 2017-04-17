# -*- coding: utf-8 -*-

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ..items import CnblogsItem
# 用相对路径导入模块包,不容易环境报错
from scrapy.http import Request
from scrapy import log
import sys
import importlib
importlib.reload(sys)
"""
not used in python 3.x
reload(sys)
sys.setdefaultencoding('utf8')
"""

class CnblogsSpider(BaseSpider):
    name = "cnblogs" #spider的名字
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        'http://www.cnblogs.com/#p%s' % p for p in range(1, 11)
        ]  #待抓取的列表

    def parse(self, response):
        self.log("Fetch douban homepage page: %s" % response.url)
        hxs = HtmlXPathSelector(response)

        #authors = hxs.select('//a[@class="titlelnk"]')

        items = hxs.select('//a[contains(@class, "titlelnk")]')

        listitems = []

        for author in items:
            #print author.select('text()').extract()
            item = CnblogsItem()
            #property
            item['Title'] = author.select('text()').extract()
            item['TitleUrl'] =author.select('@href').extract()
            listitems.append(item)

        return listitems



class BlogsSpider(BaseSpider):
    name = "cnblogs_blogs"
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        'http://www.cnblogs.com/fnng/default.aspx?page=1'
        ]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)
        # authors = hxs.select('//a[@class="titlelnk"]')
        # sel.xpath('//a[@class="PostTitle"]').xpath('text()')
        items = hxs.select('//a[@class="PostTitle"]')
        a_page = hxs.select('//div[@id="pager"]/a')
        for a_item in items:
            item = CnblogsItem()
            # property
            item['Title'] = ''.join(a_item.xpath('text()').extract())
            item['TitleUrl'] = a_item.xpath('@href').extract()
            yield item

        # get the page index
        log.msg(len(a_page))
        if len(a_page) > 0:
            for a_item in a_page:
                page_text = ''.join(a_item.xpath('text()').extract())
                if page_text == '下一页'.encode('utf-8') or 'Next' in page_text:
                    next_url = ''.join(a_item.xpath('@href').extract())
                    log.msg(next_url)
                    yield Request(next_url, callback=self.parse)
                    break