"""This script needs additional
work on rendering the JS before scraping"""

import scrapy

from scrapy.http import FormRequest


class FacebookSpider(scrapy.Spider):
    email = 'dmitryorehov2019@gmail.com'
    password = 'facebookrealpass2121'
    name = 'facebookSpider'
    custom_settings = {
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.BaseDupeFilter',
    }
    start_urls = ['https://mbasic.facebook.com/']
    profile_url = ['https://mbasic.facebook.com/nike']

    def parse(self, response):
        """Handle login with provided credentials"""

        if response.xpath('//form[contains(@action, "login")]'):
            return FormRequest.from_response(
                response,
                formxpath='//form[contains(@action, "login")]',
                formdata={'email': self.email, 'pass': self.password},
                callback=self.parse_home
            )
        href = self.profile_url[0]
        return scrapy.Request(url=href, callback=self.parse_profile, meta={'index': 1})

    def parse_home(self, response):
        '''
        This method has multiple purposes:
        1) Handle failed logins due to facebook 'save-device' redirection
        2) Set language interface, if not already provided
        3) Navigate to given page 
        '''
        # handle 'save-device' redirection
        if response.xpath("//div/a[contains(@href,'save-device')]"):
            self.logger.info('Going through the "save-device" checkpoint')
            return FormRequest.from_response(
                response,
                formdata={'name_action_selected': 'dont_save'},
                callback=self.parse_home
            )

        # navigate to provided page
        href = self.profile_url[0]
        self.logger.info('Scraping facebook page {}'.format(href))
        return scrapy.Request(url=href, callback=self.parse_profile, meta={'index': 1})

    def parse_profile(self, response):
        item = response.meta['item']
        self.logger.info('Crawling profile info')
        item['fb_followers'] = response.css('div:contains("people follow this")::text').get()
        item['fb_name'] = response.css('a._64-f:span::text').get()
        item['fb_handler'] = response.css('a._2wmb::text').get()
        item['fb_img'] = response.css('img._6tb5::attr(src)').get()

        yield item
