# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.utils.response import response_status_message
from scrapy.downloadermiddlewares.httpproxy import HttpProxyMiddleware
from collections import defaultdict





class DeecampScraperSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class DeecampScraperDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class RandomProxyUserAgentMiddleware(HttpProxyMiddleware):
    def __init__(self, auth_encoding='utf-8', proxy_list_file=None, ua_list_file=None):
        self.auth_encoding=auth_encoding
        self.proxies=defaultdict(list)

        with open(proxy_list_file) as f:
            proxy_list = f.readlines()
            scheme = "http"
            for proxy in proxy_list:
                url = proxy
                self.proxies[scheme].append(self._get_proxy(url,scheme))
        
        with open(ua_list_file) as f:
            self.ua_list = [line.strip('\n') for line in f.readlines()]


    @classmethod
    def from_crawler(cls, crawler):
        auth_encoding = crawler.settings.get('HTTPPROXY_AUTH_ENCODING','utf-8')
        proxy_list_file = crawler.settings.get('PROXY_LIST_FILE')
        ua_list_file = crawler.settings.get("USER_AGENT_LIST_FILE")

        return cls(auth_encoding, proxy_list_file, ua_list_file)

    def _set_proxy(self, request, scheme):
        ua = random.choice(self.ua_list)
        request.headers.setdefault('User-Agent', ua)

        creds,proxy = random.choice(self.proxies[scheme])
        request.meta['proxy']=proxy
        if creds:
            request.headers['Proxy-Authorization']=b'Basic'+creds




