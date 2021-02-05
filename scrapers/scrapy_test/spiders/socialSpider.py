import json
import sqlite3

import scrapy

from .items import SocialBrandItem


class SocialSpider(scrapy.Spider):
    name = 'socialSpider'

    connection = sqlite3.connect("brands.db")
    cursor = connection.cursor()
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_test.pipelines.InstagramPipeline': 300},
        'ITEM_PIPELINES': {'scrapy_test.pipelines.FairePipeline': 300},
        'ROBOTSTXT_OBEY': False,
    }

    def start_requests(self):
        """Getting shop links from db"""
        brand_data = self.cursor.execute(
            """select id, main_brand_url FROM brands_tb WHERE main_brand_url IS NOT NULL""").fetchall()
        brand_data = [x for x in brand_data]
        for brand in brand_data:
            item = SocialBrandItem()
            item['name'] = brand[0]
            item['main_brand_url'] = brand[1]
            yield scrapy.Request(url=brand[1], callback=self.get_social_urls, meta={'item': item})

    def get_social_urls(self, response):
        """"Looking for social links on main pages"""
        item = response.meta['item']
        fb_url = response.xpath('//a[contains(@href, "facebook.com")]/@href').get()
        if fb_url:
            pass
        pr_url = response.css('a:contains("pinterest.com")::attr(href)').get()
        if pr_url:
            pass
        inst_url = response.css('a:contains("instagram.com")::attr(href)').get()
        if inst_url:
            url = inst_url + '/?__a=1'
            scrapy.Request(url=url, callback=self.parse_inst, meta={'item': item})

    def parse_inst(self, response):
        item = response.meta['item']
        if response:
            user_json = json.loads(response.body)
            user_data = user_json['graphql']['user']
            item['inst_name'] = user_data['full_name']
            item['inst_img'] = user_data['profile_pic_url']
            item['inst_followers'] = user_data['edge_followed_by']['count']
        yield item
