# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy.http import Request
from urllib import parse
from ..items import JobBolespiderItem, ArticleItemloader
from ..utils.common import get_md5
import datetime
from scrapy.loader import ItemLoader
from selenium import webdriver
from scrapy.xlib.pydispatch import dispatcher
from scrapy import signals


class JobboleSpider(scrapy.Spider):
    name = "jobbole"
    allowed_domains = ["blog.jobbole.com"]
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def __init__(self):
        self.browser = webdriver.Chrome(executable_path="H:/chormdriver/chromedriver.exe")
        super(JobboleSpider, self).__init__()
        dispatcher.connect(self.spide_closed, signals.spider_closed)

        # 当爬虫退出的时候关闭浏览器
    def spide_closed(self, spider):
        print("spider closed")
        self.browser.quit()

    def parse(self, response):
        post_nodes = response.css('#archive .floated-thumb .post-thumb a')
        for post_node in post_nodes:
            image_url = post_node.css("img::attr(src)").extract_first("")
            post_url = post_node.css("::attr(href)").extract_first("")
            yield Request(url=parse.urljoin(response.url, post_url), meta={"front_image_url": image_url}, callback=self.parse_detail)
        next_url = response.css('.margin-20 a.page-numbers::attr(href)').extract_first()
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):

        # article_items = JobBolespiderItem()
        # # 解析具体文章

        # title = response.css('.entry-header h1::text').extract_first("")
        # create_time = response.css('.entry-meta p::text').extract_first("").strip().replace('.','').strip()
        # prases_nums = response.css('.vote-post-up h10::text').extract_first("")
        # fav_nums = response.css('.bookmark-btn::text').extract_first("")
        # match_re=re.match('.*?(\d+).*',fav_nums)
        # if match_re:
        #     fav_nums=match_re.groups(1)
        # else:
        #     fav_nums=0
        # comment_nums = response.css('a[href="#article-comment"] span::text').extract_first("")
        # match_re = re.match('.*?(\d+).*', comment_nums)
        # if match_re:
        #     comment_nums=match_re.groups(1)
        # else:
        #     comment_nums=0
        # content = response.css('div .entry').extract_first("")
        # tags_list = response.css('p.entry-meta-hide-on-mobile a::text').extract()
        # tags = ''.join(tags_list)

        # article_items["url_object_id"] = get_md5(response.url)
        # article_items["title"] = title
        # article_items["url"] =response.url
        # try:
        #     create_time = datetime.datetime.strptime(create_time,"%Y/%m/%d").date()
        # except Exception as e:
        #     create_time = datetime.datetime.now().date()
        # article_items["create_time"] = create_time
        # article_items["front_image_url"] = [front_image_url]
        # article_items["prases_nums"] = prases_nums
        # article_items["fav_nums"] = fav_nums
        # article_items["comment_nums"] = comment_nums
        # article_items["content"] = content
        # article_items["tags"] = tags

        item_loader = ArticleItemloader(item=JobBolespiderItem(), response=response)
        front_image_url = response.meta.get("front_image_url", "")
        item_loader.add_css('title', '.entry-header h1::text')
        item_loader.add_value('url', response.url)
        item_loader.add_value('url_object_id', get_md5(response.url))
        item_loader.add_value('front_image_url', [front_image_url])
        item_loader.add_css('create_time', '.entry-meta p::text')
        item_loader.add_css('prases_nums', '.vote-post-up h10::text')
        item_loader.add_css('fav_nums', '.bookmark-btn::text')
        item_loader.add_css('comment_nums', 'a[href="#article-comment"]')
        item_loader.add_css('content', 'div.entry')
        item_loader.add_css('tags', 'p.entry-meta-hide-on-mobile a::text')
        article_items = item_loader.load_item()
        yield article_items











