# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CandItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
    party = scrapy.Field()
    pic = scrapy.Field()
    dist = scrapy.Field()
    fb = scrapy.Field()
    twtr = scrapy.Field()
    camp = scrapy.Field()
    state = scrapy.Field()
