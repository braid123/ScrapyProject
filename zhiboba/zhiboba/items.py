# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhibobaItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    label = scrapy.Field()
    sdate = scrapy.Field()
    linkurl = scrapy.Field()
    home_team = scrapy.Field()
    home_score = scrapy.Field()
    visit_team = scrapy.Field()
    visit_score = scrapy.Field()



