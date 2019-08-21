# -*- coding: utf-8 -*-
import os
import pymysql
from .items import EventmonitorItem
import traceback
import logging
from EventMonitor.middlewares import UrlFilterAndAdd, URLRedisFilter
from twisted.enterprise import adbapi

logger = logging.getLogger(__name__)


class EventmonitorPipeline(object):
    commit_sql_str = '''insert into news(keyword,news_url,news_title,news_date,news_content) values ("{keyword}","{news_url}","{news_title}","{news_date}","{news_content}");'''
    total = 0

    def __init__(self, settings):
        self.settings = settings
        self.dupefilter = UrlFilterAndAdd()

    def process_item(self, item, spider):
        self.dupefilter.add_url(item['news_url'])
        try:
            sqltext = self.commit_sql_str.format(
                keyword=pymysql.escape_string(item["keyword"]),
                news_url=item["news_url"],
                news_title=pymysql.escape_string(item["news_title"]),
                news_date=item["news_date"],
                news_content=item["news_content"],
            )

            self.cursor.execute(sqltext)
        except Exception as e:
            logger.warning(e)
        self.total += 1
        print("total", self.total)
        print("详情页：", item["news_url"])

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def open_spider(self, spider):
        self.connect = pymysql.connect(
            host=self.settings.get("MYSQL_HOST"),
            port=self.settings.get("MYSQL_PORT"),
            db=self.settings.get("MYSQL_DBNAME"),
            user=self.settings.get("MYSQL_USER"),
            passwd=self.settings.get("MYSQL_PASSWD"),
            charset='utf8mb4',
            use_unicode=True
        )

        self.cursor = self.connect.cursor()
        self.connect.autocommit(True)

    def close_spider(self, spider):
        self.cursor.close()
        self.connect.close()
