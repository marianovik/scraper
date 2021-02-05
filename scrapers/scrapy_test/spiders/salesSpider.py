import sqlite3

import requests
import scrapy
from .items import FaireBrandItem


class SalesSpider(scrapy.Spider):
    name = 'salesSpider'

    connection = sqlite3.connect("brands.db")
    cursor = connection.cursor()
    custom_settings = {
        'ROBOTSTXT_OBEY': False,
        'ITEM_PIPELINES': {'scrapy_test.pipelines.SalesPipeline': 300}
    }

    def start_requests(self):
        """Getting shop links from db"""
        brand_data = self.cursor.execute(
            """select id, main_brand_url FROM brands_tb WHERE main_brand_url IS NOT NULL""").fetchall()
        brand_data = [x for x in brand_data]
        for brand in brand_data:
            item = SalesBrandItem()
            item['name'] = brand[0]
            item['main_brand_url'] = brand[1]
            yield scrapy.Request(url=brand[1], callback=self.parse, meta={'item': item})

    def parse(self, response):
        """Looking for etcy and amazon urls on main pages"""
        item = response.meta['item']
        amazon_url = response.xpath('//a[contains(@href, "amazon.com")]/@href').get()
        etcy_url = response.xpath('//a[contains(@href, "etcy.com")]/@href').get()
        if not amazon_url:
            amazon_url = get_shop_link(item['name'], 'A')
        item['amazon_url'] = amazon_url
        if not etcy_url:
            etcy_url = get_shop_link(item['name'], 'E')
        item['etcy_url'] = etcy_url
        if etcy_url:
            yield scrapy.Request(etcy_url, callback=self.parse_etcy, meta={'item': item})
        else:
            yield item


    def parse_etcy(self, response):
        item = response.meta['item']
        item['etcy_sales'] = response.css('span:contains("Sales")::text, a:contains("Sales")::text').get()
        item['etcy_name'] = response.css('div.shop-name-and-title-container>h1::text').get()
        yield item


def get_platform_link(brand_name, platform):
    """Generating the links in case none was found on main page"""
    if platform == 'A':
        base_url = 'https://www.amazon.com/shop/'
    elif platform == 'E':
        base_url = 'https://www.etsy.com/shop/'
    elif platform == 'K':
        base_url == 'https://www.kickstarter.com/profile/'
    name_control_list = ['llc', 'lc', 'ltd', 'co', 'inc', 'llc.', 'lc.', 'ltd.', 'co.', 'inc.']
    coma_control = [',', '.', ')', ':', " ", '', "'"]
    brand_letter_split = list(brand_name)
    [brand_letter_split.remove(i) for i in brand_letter_split if i in coma_control]
    r = requests.get(base_url + ''.join(brand_letter_split))
    if r:
        return base_url + ''.join(brand_letter_split)
    brand_word_split = brand_name.lower().split(" ")
    [brand_word_split.remove(i) for i in brand_word_split if i in name_control_list]
    brand_letter_split = list(''.join(brand_word_split))
    [brand_letter_split.remove(i) for i in brand_letter_split if i in coma_control]
    r = requests.get(base_url + ''.join(brand_letter_split))
    if r:
        return base_url + ''.join(brand_letter_split)
    return None
