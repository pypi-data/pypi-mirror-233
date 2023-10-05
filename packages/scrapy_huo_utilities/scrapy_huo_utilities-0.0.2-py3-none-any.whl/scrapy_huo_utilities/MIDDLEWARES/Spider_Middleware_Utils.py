import hashlib

import plyvel
from loguru import logger
from scrapy import signals
from scrapy.utils.project import get_project_settings


def hash_url(url):
    return hashlib.sha256(url.encode()).hexdigest()


class DuplicateUrls_SPIDER_MIDDLEWARES:
    '''
    使用方法：
    在`settings.py`的`SPIDER_MIDDLEWARES`中修改添加：
   `"scrapy_huo_utilities.MIDDLEWARES.Spider_Middleware_Utils.DuplicateUrls_SPIDER_MIDDLEWARES": 543,`

    '''

    def __init__(self):
        self.db = None
        logger.info(f'DuplicateUrls_SPIDER_MIDDLEWARES 初始化')

    @classmethod
    def from_crawler(cls, crawler):
        middleware = cls()
        crawler.signals.connect(middleware.spider_opened, signal=signals.spider_opened)
        crawler.signals.connect(middleware.spider_closed, signal=signals.spider_closed)

        return middleware

    def spider_opened(self, spider):
        db_path = f"{get_project_settings().get('BOT_NAME')}_db"
        self.db = plyvel.DB(db_path.encode(), create_if_missing=True)
        logger.info(f'数据库 初始化')

    def spider_closed(self, spider):
        logger.info(f'数据库 关闭')

        self.db.close()

    def process_spider_input(self, response, spider):
        # logger.info(f'处理数据')
        url = response.url
        if self.db.get(url.encode()):
            # URL is already in the database, skip visiting
            logger.info(f'URL已在数据库，跳过。')
        else:
            # URL is not in the database, record it and proceed with the visit
            self.db.put(url.encode(), b'visited')
        return None
