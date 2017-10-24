# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import datetime
import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from scrapy.loader import ItemLoader
import re


def time_convert(value):
    try:
        create_time = datetime.datetime.strptime(value, "%Y/%m/%d").date()
    except Exception as e:
        create_time = datetime.datetime.now().date()
    return create_time


def get_nums(value):
    match_re = re.match('.*?(\d+).*', value)
    if match_re:
        nums = match_re.groups(1)
    else:
        nums = 0
    return  nums


def remove_commont_tags(value):
    if "评论" in value:
        return ""
    else:
        return value


def retur_value(value):
    return value


class ArticleItemloader(ItemLoader):
    default_output_processor=TakeFirst()


class JobBolespiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()

    title = scrapy.Field()
    create_time = scrapy.Field(
        input_processor=MapCompose(time_convert)
    )
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    front_image_url = scrapy.Field(
        output_processor=(retur_value)
    )
    front_image_path = scrapy.Field(

    )
    prases_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    fav_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    comment_nums = scrapy.Field(
        input_processor=MapCompose(get_nums)
    )
    content = scrapy.Field()
    tags = scrapy.Field(
        input_processor=MapCompose(remove_commont_tags),
        output_processor=Join(',')
    )
