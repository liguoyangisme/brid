# -*- coding: utf-8 -*-
from time import strftime,time

from datetime import timedelta, datetime


class DateUtils:

    # 格式化为日期字符串
    def formatDate(self, date):
        return date.strftime('%Y-%m-%d')

    # 格式化为时间字符串
    def formatTime(self, time):
        return time.strftime('%Y-%m-%d %H:%M:%S')

    # 今日
    def todayStr(self):
        return self.formatDate(datetime.now())

    # 当前时间
    def nowStr(self):
        return self.formatTime(datetime.now())

    # 加日期
    def addDayStr(self,days):
        return self.formatDate(datetime.now() + timedelta(days=days))
