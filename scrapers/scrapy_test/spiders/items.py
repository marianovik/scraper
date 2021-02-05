# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyTestItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class FaireBrandItem(scrapy.Item):
    name = scrapy.Field()
    desc = scrapy.Field()
    img = scrapy.Field()
    main_brand_url = scrapy.Field()
    faire_url = scrapy.Field()
    inst_handler = scrapy.Field()


class SalesBrandItem(scrapy.Item):
    amazon_url = scrapy.Field()
    etcy_url = scrapy.Field()
    name = scrapy.Field()
    etcy_sales = scrapy.Field()
    main_brand_url = scrapy.Field()
    etcy_name = scrapy.Field()


class SocialBrandItem(scrapy.Item):
    main_brand_url = scrapy.Field()
    name = scrapy.Field()
    inst_name = scrapy.Field()
    inst_handler = scrapy.Field()
    inst_img = scrapy.Field()
    inst_followers = scrapy.Field()
    fb_name = scrapy.Field()
    fb_handler = scrapy.Field()
    fb_img = scrapy.Field()
    fb_followers = scrapy.Field()
    pr_name = scrapy.Field()
    pr_handler = scrapy.Field()
    pr_img = scrapy.Field()
    pr_followers = scrapy.Field()
    tt_name = scrapy.Field()
    tt_handler = scrapy.Field()
    tt_img = scrapy.Field()
    tt_followers = scrapy.Field()
    date = scrapy.Field()


class InstagramBrandItem(scrapy.Item):
    name = scrapy.Field()
    handler = scrapy.Field()
    img = scrapy.Field()
    followers = scrapy.Field()


class ProfileItem(scrapy.Item):
    name = scrapy.Field()
    gender = scrapy.Field()
    birthday = scrapy.Field()
    current_city = scrapy.Field()
    hometown = scrapy.Field()
    work = scrapy.Field()
    education = scrapy.Field()
    interested_in = scrapy.Field()
    page = scrapy.Field()


class HTMLitem(scrapy.Item):
    HTML = scrapy.Field()
    main_brand_url = scrapy.Field()
