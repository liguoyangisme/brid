# -*- coding: utf-8 -*-
import logging

from bird.fetch_free_proxyes import fetch_all

logger = logging.getLogger(__name__)

"""
HTTP代理中间件
"""
class ProxyMiddleware(object):

    proxy_index = 0
    proxy_list = fetch_all()

    """
    通过代理请求
    """
    def process_request(self, request, spider):
        proxy = self.nextProxy()
        logger.debug("proxy: %s %s" % (proxy, request.url))
        request.meta["proxy"] = "http://" + proxy

    """
    检查请求结果
    """
    def process_response(self, request, response, spider):
        logger.debug("response：%d %s" % (response.status, request.url))
        return response

    """
    请求异常更换代理
    """
    def process_exception(self, request, exception, spider):
        logger.debug("error：%s" % request.url)
        return None

    def nextProxy(self):
        # 获得下个代理
        proxy = self.proxy_list[self.proxy_index]

        # 代理序号自增
        if self.proxy_index+1 >= self.proxy_list.__len__():
            self.proxy_index = 0
        else:
            self.proxy_index += 1
        return proxy
