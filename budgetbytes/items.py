# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BudgetbytesItem(scrapy.Item):
    # define the fields for your item here like:
    category = scrapy.Field()
    recipe_name = scrapy.Field()
    recipe_price = scrapy.Field()
    serving_price = scrapy.Field()
    time_hrs = scrapy.Field()
    time_mins = scrapy.Field()
    rating = scrapy.Field()
    votes = scrapy.Field()

