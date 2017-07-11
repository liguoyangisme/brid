#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

import logging
import scrapy
from scrapy import Field

from core.mongo.Mongo import Mongo
from core.mongo.MongoDB import MongoObject
from core.utils.DateUtils import *


class SpiderSuper(scrapy.spiders.Spider):

    # 日志
    logger = logging.getLogger(__name__)

    # 网站
    name = None
    # 日期
    date = todayStr()
    # 允许访问域名
    allowed_domains = []

    # 获得任务
    def getTasks(self):

        try:

            task_con = MongoObject("task")
            url_con = MongoObject("urls")

            # 检查任务是否已存在
            if task_con.count({"site": self.name, "date": self.date, "status": "ready"}) == 0:

                # 插入爬虫url
                url_list = []

                for url in self._getUrls():
                    # 记录爬虫url
                    task = SpiderTask()
                    task.init(url=url, site=self.name, date=self.date)
                    url_list.append(url_con.save(task))

                # 记录任务准备好
                task_con.save({"site": self.name, "date": self.date, "status": "ready", "create_time": nowStr()})

                return url_list

            else:

                # 获得待处理的爬虫url
                return url_con.findRs({"site": self.name, "date": self.date, "status": "wait"})


        except Exception as e:

            # 记录任务为失败
            task_con.save({"site": self.name, "date": self.date, "status": "fail", "create_time": nowStr()})
            # 删除已插入任务记录
            url_con.delete({"site": self.name, "createDate": self.date})

            self.logger.error("生成URL爬虫列表失败！ %s", e)

            return []

        finally:

            # 关闭连接
            url_con.close()
            task_con.close()

    # 获得任务url
    def _getUrls(self):
        pass

    # 标记完成
    def completeUrl(self, id):
        url_con = MongoObject("urls")
        url_con.update({"_id": id}, {"status": "complete", "completeTime": nowStr()})
        url_con.close()


class SpiderTask(Mongo):

    # 网站
    site = Field()

    # URL
    url = Field()

    # 日期
    date = Field()

    # 状态
    status = Field()

    # 当前时间
    createTime = Field()

    # 完成时间
    completeTime = Field()


    def init(self, url, site, date):

        self["url"] = url

        self["site"] = site

        self["date"] = date

        self["status"] = "wait"