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


    #知乎question
class ZhihuQuestionItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    topics = scrapy.Field()
    url = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()
    answer_num = scrapy.Field()
    comment_nums = scrapy.Field()
    watch_nums = scrapy.Field()
    clinic_nums = scrapy.Field()
    crawl_time = scrapy.Field()


class ZhihuAnswerItem(scrapy.Item):
    zhihu_id = scrapy.Field()
    url = scrapy.Field()
    question_id = scrapy.Field()
    author_id = scrapy.Field()
    content = scrapy.Field()
    parise_num = scrapy.Field()
    comments_num = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
    crawl_time = scrapy.Field()


    #拉钩网
class LagouItem(scrapy.Item):
    title = scrapy.Field()
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    salary = scrapy.Field()
    job_city = scrapy.Field()
    work_years = scrapy.Field()
    degree_need = scrapy.Field()
    job_type = scrapy.Field()
    publish_time = scrapy.Field()
    job_advantage = scrapy.Field()
    job_desc = scrapy.Field()
    job_addr = scrapy.Field()
    company_name = scrapy.Field()
    company_utrl = scrapy.Field()
    tags = scrapy.Field()
    crawl_time = scrapy.Field()


class LagouItemloader(ItemLoader):
    default_output_processor=TakeFirst()