import urllib
import logging

log = logging.getLogger('scrapy.scraperapi')

class ScraperApiProxy(object):
    """Proxy url rotation"""
    def __init__(self, settings):
        self.scraperapi_ena = settings.get('SCRAPERAPI_ENABLED', True)
        self.scraperapi_url = settings.get('SCRAPERAPI_URL', 'api.scraperapi.com')
        self.scraperapi_key = settings.get('SCRAPERAPI_KEY')

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        if not self.scraperapi_ena:
            log.warning("Skipping Scraper API CALL(disabled)!")
            return
        #Override request url
        if self.scraperapi_url not in request.url: 
            k_name = 'token' if ('proxycrawl' in self.scraperapi_url) else 'key'
            new_url = 'https://%s/?%s=%s&url=%s' % (self.scraperapi_url, k_name, self.scraperapi_key, urllib.parse.quote(request.url))
            log.debug('Using Scraper API, overridden URL is: %s' % (new_url))
            return request.replace(url=new_url)
        
