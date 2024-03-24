# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HomeresourceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    location = scrapy.Field()
    cp = scrapy.Field()
    information = scrapy.Field()
    picture = scrapy.Field()
    picture1 = scrapy.Field()
    area = scrapy.Field()
    locate = scrapy.Field()
    pass
