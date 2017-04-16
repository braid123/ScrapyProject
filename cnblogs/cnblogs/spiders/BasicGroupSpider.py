from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
from ..items import CnblogsItem
# 用相对路径导入模块包,不容易环境报错
class CnblogsSpider(BaseSpider):
    name = "cnblogs" #spider的名字
    allowed_domains = ["cnblogs.com"]
    start_urls = [
        'http://www.cnblogs.com/'
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