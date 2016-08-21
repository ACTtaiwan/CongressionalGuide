# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#CREATE TABLE candidates (firstName TEXT, lastName TEXT, prefix TEXT, suffix TEXT, party TEXT, chamber TEXT, state TEXT, district INT, incumbent BOOLEAN, bioguideId TEXT, fecId TEXT, note BLOB, website TEXT, email TEXT, facebook TEXT, twitter TEXT, youtube TEXT, img_src TEXT);

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
    chamber = scrapy.Field()
    incumbent = scrapy.Field()
    youtube = scrapy.Field()
    email = scrapy.Field()
