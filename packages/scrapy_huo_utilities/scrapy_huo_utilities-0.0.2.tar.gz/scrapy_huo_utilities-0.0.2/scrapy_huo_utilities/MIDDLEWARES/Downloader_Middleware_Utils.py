from FakeAgent import Fake_Agent
from loguru import logger
from scrapy import signals


class RandomUserAgent_DOWNLOADER_MIDDLEWARES:
    '''
    使用方法：
    在`settings.py`的`DOWNLOADER_MIDDLEWARES`中修改添加：
   `"scrapy_huo_utilities.MIDDLEWARES.Downloader_Middleware_Utils.RandomUserAgent_DOWNLOADER_MIDDLEWARES": 543,`


    '''

    def __init__(self):
        self.ua = Fake_Agent()
        logger.info(f'RandomUserAgent_DOWNLOADER_MIDDLEWARES 初始化')

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        return middleware

    def spider_opened(self, spider):
        pass

    def process_request(self, request, spider):
        self.user_agent = self.ua.random()
        logger.info(f'RandomUserAgent_DOWNLOADER_MIDDLEWARES {request.url} User-Agent: {self.user_agent}')
        request.headers.setdefault(b'User-Agent', self.user_agent)
