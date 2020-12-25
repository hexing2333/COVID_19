# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Covid19Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    country = scrapy.Field()
    increased = scrapy.Field()
    total = scrapy.Field()
    cure = scrapy.Field()
    dead = scrapy.Field()
    pass
