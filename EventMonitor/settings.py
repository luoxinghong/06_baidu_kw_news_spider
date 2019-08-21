# -*- coding: utf-8 -*-

BOT_NAME = 'EventMonitor'
SPIDER_MODULES = ['EventMonitor.spiders']
NEWSPIDER_MODULE = 'EventMonitor.spiders'
ROBOTSTXT_OBEY = False


import datetime
to_day = datetime.datetime.now()
log_file_path = "./logs/{}_{}_{}.log".format(to_day.year, to_day.month, to_day.day)
LOG_LEVEL = "INFO"
LOG_FILE = log_file_path

# 增加爬虫速度及防ban配置
DOWNLOAD_DELAY = 0
DOWNLOAD_FAIL_ON_DATALOSS = False
CONCURRENT_REQUESTS = 50
CONCURRENT_REQUESTS_PER_DOMAIN = 50
CONCURRENT_REQUESTS_PER_IP = 50
COOKIES_ENABLED = False
DOWNLOAD_TIMEOUT = 30

DOWNLOADER_MIDDLEWARES = {
    'EventMonitor.middlewares.EventmonitorSpiderMiddleware': 543,
    'scrapy.downloadermiddlewares.httpcompression.HttpCompressionMiddleware': 810,
    'EventMonitor.middlewares.RandomUserAgentMiddleware': 1,
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # 这里要设置原来的scrapy的useragent为None，否者会被覆盖掉
}

ITEM_PIPELINES = {
    'EventMonitor.pipelines.EventmonitorPipeline': 300,
}

# 配置自己重写的RFPDupeFilter

DUPEFILTER_CLASS = 'EventMonitor.middlewares.URLRedisFilter'

#redis数据库配置
REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_PASSWD = "lxh123"
REDIS_DBNAME = 0
REDIS_KEY = "baidu_news"

# msyql数据库配置
MYSQL_HOST = "localhost"
MYSQL_DBNAME = "baidu_news"
MYSQL_USER = "root"
MYSQL_PASSWD = "lxh123"
MYSQL_PORT = 3306

# 设置
RANDOM_UA_TYPE = 'random'