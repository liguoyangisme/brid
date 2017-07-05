# -*- coding: utf-8 -*-
from scrapy import Spider, Request

from bird.items import LineItem


# 线路爬虫
class LineSpider(Spider):
    # 爬虫名称
    name = 'line'
    # 允许访问域名
    allowed_domains = ["flights.ctrip.com"]

    # 开始爬虫地址
    def start_requests(self):
        # 每页线路列表
        return [Request("http://flights.ctrip.com/booking/top/jinqiremen-p%d" % i, callback=self.parse_line) for i in
                range(1, 96)]

    # 解析线路
    def parse_line(self, response):
        # 提取行
        list = response.selector.xpath("//div[@class='mod_box rank_table']//tr[position()>1][position()<last()]")

        for h in list:
            item = LineItem()
            # 提取出发地
            item['fromCity'] = h.xpath("td[6]/text()").extract()[0].encode('utf-8').strip()
            # 提取目的地
            item['toCity'] = h.xpath("td[7]/text()").extract()[0].encode('utf-8').strip()
            yield item
