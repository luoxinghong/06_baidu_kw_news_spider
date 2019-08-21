#!/usr/bin/env python3
# coding: utf-8
import scrapy
from lxml import etree
import requests
import urllib.parse
from .extract_news import *
from EventMonitor.items import EventmonitorItem
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
import logging

logger = logging.getLogger(__name__)


class NewsSpider(scrapy.Spider):
    name = 'eventspider'

    def __init__(self, keyword):
        self.baidu_homepage = "https://news.baidu.com/ns?word={}&pn={}"
        self.keyword = keyword
        self.parser = NewsParser()

    '''获取搜索页'''

    def get_html(self, url):
        html = requests.get(url).content.decode('utf-8')
        return html

    '''获取新闻列表'''

    def collect_newslist(self, html):
        selector = etree.HTML(html)
        urls = selector.xpath('//h3[@class="c-title"]/a/@href')
        return set(urls)

    '''采集主函数'''

    def start_requests(self):
        word = urllib.parse.quote_plus(self.keyword)
        for page_num in range(20, 500, 20):
            print("*" * 100)
            url = self.baidu_homepage.format(word, page_num)
            print("目前爬取的SEARCH页", url)
            yield scrapy.Request(url, callback=self.get_url, errback=self.errback_httpbin,dont_filter=True)

    def get_url(self, response):
        news_links = self.collect_newslist(response.text)
        for news_link in news_links:
            yield scrapy.Request(news_link, callback=self.page_parser, errback=self.errback_httpbin)

    def page_parser(self, response):
        data = self.parser.extract_news(response.text)
        if data:
            item = EventmonitorItem()
            item['keyword'] = self.keyword
            item['news_url'] = response.url
            item['news_date'] = data['news_date']
            item['news_title'] = data['news_title']
            item['news_content'] = data['news_content']
            yield item

        return

    def errback_httpbin(self, failure):
        self.logger.error(repr(failure))

        if failure.check(HttpError):
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
