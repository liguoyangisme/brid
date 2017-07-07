# -*- coding: utf-8 -*-
import logging

import time

from FreeProxy import fetch_all
# 获得日志
from twisted.internet.error import ConnectionRefusedError, ConnectionDone, TimeoutError


logger = logging.getLogger(__name__)

"""
HTTP代理中间件
"""
class ProxyMiddleware(object):

    # 当前代理序号
    proxy_index = 0
    # 代理列表
    proxy_list = fetch_all()

    """
    通过代理请求
    """
    def process_request(self, request, spider):
        # 切换代理
        proxy = self.nextProxy()

        # 设置代理
        request.meta["proxy"] = "http://" + proxy

        # logger.debug("proxy: %s %s" % (proxy, request.url))

    """
    检查请求结果
    """
    def process_response(self, request, response, spider):
        # logger.debug("response：%d %s" % (response.status, request.url))
        return response

    """
    请求异常更换代理
    """
    def process_exception(self, request, exception, spider):

        time.sleep(30)

        if isinstance(exception,ConnectionRefusedError) or isinstance(exception,TimeoutError) or isinstance(exception,ConnectionDone):
            logger.error("! %s %s" % (exception.message, request.meta["proxy"]))
            return request
        else:
            logger.error("error：%s %s" % (exception.message, request.url))
            return request

    """
    切换下一个代理
    """
    def nextProxy(self):
        # 获得下个代理
        proxy = self.proxy_list[self.proxy_index]

        # 代理序号自增
        if self.proxy_index+1 >= self.proxy_list.__len__():
            self.proxy_index = 0
        else:
            self.proxy_index += 1
        return proxy
