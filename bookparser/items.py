# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BookparserItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    discount_price = scrapy.Field()
    base_price = scrapy.Field()
    current_price = scrapy.Field()
    rate = scrapy.Field()
    _id = scrapy.Field()
