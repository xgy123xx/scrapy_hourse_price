# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BeijinghousingpriceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    telephone = scrapy.Field()
    house_highlight = scrapy.Field()
    house_desc = scrapy.Field()

    method = scrapy.Field()
    house_type = scrapy.Field()
    face_floor = scrapy.Field()
    village = scrapy.Field()
    area = scrapy.Field()
    address = scrapy.Field()

