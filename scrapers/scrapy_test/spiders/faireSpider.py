import logging

import js2xml
import scrapy
from scrapy.spiders import SitemapSpider
from js2xml.utils.vars import get_vars

from .items import FaireBrandItem


class FaireSpider(SitemapSpider):
    """Using sitemap of getting all the brand urls from Faire.com"""
    name = 'faireSpider'
    sitemap_rules = [('/brand/', 'parse')]
    sitemap_urls = ['https://www.faire.com/sitemap.xml.gz']

    custom_settings = {
        'ITEM_PIPELINES': {'scrapy_test.pipelines.FairePipeline': 300},
        'ROBOTSTXT_OBEY': False,
        'CLOSESPIDER_PAGECOUNT': 1000
    }

    def parse(self, response):
        item = FaireBrandItem()
        snippet = response.css('script:contains("brandView")::text').get()
        vars = get_vars(js2xml.parse(snippet))
        brandView = vars['brandView']['brand']
        try:
            item['faire_url'] = 'https://www.faire.com/brand/' + response.url.split('/')[-1]
            item['name'] = brandView.get('name')
            item['desc'] = brandView.get('description')
            item['img'] = brandView.get('profile_image').get('url')
            item['main_brand_url'] = brandView.get('url')
            item['inst_handler'] = brandView.get('instagram_handle')

        except (IndexError, KeyError):
            logging.warning("Cannot catch a field on %s", response.url)
        finally:
            yield item

# def run_crawl(spider):
#     """For using several scripts simultaneously (not working yet)"""
#     runner = CrawlerRunner(get_project_settings())
#     deferred = runner.crawl(spider)
#     deferred.addCallback(reactor.callLater, 5, run_crawl)
#     return deferred
#
# if __name__ == "__main__":
#     process = CrawlerProcess()
#     process.crawl(FaireSpider)
#     process.start()
