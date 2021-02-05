import scrapy
import sqlite3
from .items import HTMLitem


class MainStoreSpider(scrapy.Spider):
    name = 'mainStoreSpider'
    connection = sqlite3.connect("brands.db")
    cursor = connection.cursor()
    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_test.pipelines.HTMLPipeline': 300},
        'DOWNLOADER_MIDDLEWARES': {'scrapy_proxy_pool.middlewares.ProxyPoolMiddleware': 610}
    }

    def start_requests(self):
        """Getting shop links from db"""
        brand_urls = self.cursor.execute(
            """select main_brand_url FROM brands_tb WHERE main_brand_url IS NOT NULL""").fetchall()
        urls = [x[0] for x in brand_urls]
        for url in urls:
            item = HTMLitem()
            item['main_brand_url'] = url
            if url:
                yield scrapy.Request(url=url, callback=self.parse, meta={'item': item})

    def parse(self, response):
        """Parsing HTML"""
        item = response.meta['item']
        item['HTML'] = response.xpath("//html").extract()
        yield item


