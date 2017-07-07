# -*- coding: utf-8 -*-

from datetime import timedelta, datetime


# 格式化为日期字符串
def formatDate(date):
    return date.strftime('%Y-%m-%d')

# 格式化为时间字符串
def formatTime(time):
    return time.strftime('%Y-%m-%d %H:%M:%S')

# 今日
def todayStr():
    return formatDate(datetime.now())

# 当前时间
def nowStr():
    return formatTime(datetime.now())

# 加日期
def addDayStr(days):
    return formatDate(datetime.now() + timedelta(days=days))
