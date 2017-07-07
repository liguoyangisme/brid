#!/usr/bin/python
# -*- coding: utf-8 -*-
import os

from bs4 import BeautifulSoup
import urllib2
import logging

logger = logging.getLogger(__name__)

def get_html(url):
    request = urllib2.Request(url)
    request.add_header("User-Agent", "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36")
    html = urllib2.urlopen(request)
    return html.read()

def get_soup(url):
    soup = BeautifulSoup(get_html(url), "lxml")
    return soup


def img2port(img_url):
    """
    mimvp.com的端口号用图片来显示, 本函数将图片url转为端口, 目前的临时性方法并不准确
    """
    code = img_url.split("=")[-1]
    if code.find("AO0OO0O")>0:
        return 80
    elif code.find("TI4")>0:
        return 3128
    elif code.find("Dgw")>0:
        return 8080
    elif code.find("DgO0O")>0:
        return 808
    elif code.find("Tk5")>0:
        return 9999
    elif code.find("Dg5")>0:
        return 8889
    else:
        return None

"""
从http://proxy.mimvp.com/free.php抓免费代理
"""
def fetch_mimvp():

    proxyes = []
    try:
        url = "http://proxy.mimvp.com/free.php?proxy=in_hp&sort=&page=%d" % 1
        soup = get_soup(url)
        table = soup.find("div", attrs={"id": "list"}).table
        tds = table.tbody.find_all("td")
        for i in range(0, len(tds), 10):
            # id = tds[i].text
            ip = tds[i+1].text
            port = img2port(tds[i+2].img["src"])
            response_time = tds[i+7]["title"][:-1]
            # transport_time = tds[i+8]["title"][:-1]
            if port is not None and float(response_time) < 1 :
                proxy = "%s:%s" % (ip, port)
                proxyes.append(proxy)
    except:
        logger.warning("fail to fetch from mimvp")
    return proxyes

"""
http://www.xicidaili.com/nn/
"""
def fetch_xici():

    proxyes = []
    try:
        url = "http://www.xicidaili.com/nn/%d" % 1
        soup = get_soup(url)
        table = soup.find("table", attrs={"id": "ip_list"})
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            tr = trs[i]
            tds = tr.find_all("td")
            ip = tds[1].text
            port = tds[2].text
            speed = tds[6].div["title"][:-1]
            latency = tds[7].div["title"][:-1]
            if float(speed) < 3 and float(latency) < 1:
                proxyes.append("%s:%s" % (ip, port))
    except:
        logger.warning("fail to fetch from xici")
    return proxyes

"""
http://www.httpdaili.com/mfdl/
更新比较频繁
"""
def fetch_httpdaili():

    proxyes = []
    try:
        url = "http://www.httpdaili.com/mfdl/"
        soup = get_soup(url)
        table = soup.find("div", attrs={"kb-item-wrap11"}).table
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            try:
                tds = trs[i].find_all("td")
                ip = tds[0].text
                port = tds[1].text
                type = tds[2].text
                if type == u"匿名":
                    proxyes.append("%s:%s" % (ip, port))
            except:
                pass
    except Exception as e:
        logger.warning("fail to fetch from httpdaili: %s" % e)
    return proxyes


"""
http://www.proxy360.cn/Proxy
"""
def fetch_proxy360():
    proxyes = []
    try:
        url = "http://www.proxy360.cn/Proxy"
        soup = get_soup(url)
        for tr in soup.findAll("div", attrs={"name":"list_proxy_ip"}):
            try:
                tds = tr.div.contents
                ip = tds[1].text.strip()
                port = tds[3].text.strip()
                type = tds[5].text.strip()
                if type == u"高匿":
                    proxyes.append("%s:%s" % (ip, port))
            except:
                pass
    except Exception as e:
        logger.warning("fail to fetch from httpdaili: %s" % e)
    return proxyes

def fetch_kuaidaili():
    proxyes = []
    try:
        url = "http://www.kuaidaili.com/free/inha/%d/" % 1
        soup = get_soup(url)
        trs = soup.findAll("div", attrs={"id":"list"})[0].find_all("tr")
        for i in range(1, len(trs)):
            try:
                td = trs[i].findAll("td")
                ip = td[0].text.strip()
                port = td[1].text.strip()
                type = td[2].text.strip()
                if type == u"高匿名":
                    proxyes.append("%s:%s" % (ip, port))
            except:
                pass
    except Exception as e:
        logger.warning("fail to fetch from kuaidaili: %s" % e)
    return proxyes
"""
代理检查
"""
def check(proxy):
    import urllib2
    url = "http://www.ip181.com/"

    request = urllib2.Request(url)
    request.set_proxy(proxy,"http")
    request.add_header("User-Agent",
                       "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36")
    try:
        # 连续三次请求可用，才可以认证为可用代理
        i = 0
        while i < 3:
            response = urllib2.urlopen(request,timeout=2)
            html = response.read()
            if html.find("i.ip181.com")!=-1 and response.code == 200 and html.find("Unauthorized")==-1:
                pass
            else:
                logger.debug("fail agent %s" % proxy)
                return False
            i += 1
        logger.debug("success agent %s" % proxy)
        return True
    except Exception:
        logger.debug("fail agent %s" % proxy)
        return False

"""
搜索代理
"""
def fetch_all():
    valid_proxyes = []
    # 代理列表
    file_name = "datas/proxy.txt"

    while valid_proxyes.__len__() <= 3:
        logger.info("搜索验证代理")

        if os.path.exists(file_name):
            # 读取代理列表
            file = open(file_name, "r")
            for line in file.readlines():
                proxy = line.strip()
                if check(proxy):
                    valid_proxyes.append(proxy)

            # 删除文件
            if valid_proxyes.__len__() <= 3:
                os.remove(file_name)

        else:

            # 搜索代理
            proxyes = []
            proxyes += fetch_kuaidaili()
            proxyes += fetch_mimvp()
            proxyes += fetch_xici()
            proxyes += fetch_httpdaili()
            proxyes += fetch_proxy360()


            # 验证&保存代理
            file = open(file_name, "w")
            for p in proxyes:
                if check(p):
                    valid_proxyes.append(p)
                    file.write(p+'\n')

    logger.info("可用代理数：%s" % valid_proxyes.__len__())
    return valid_proxyes

if __name__ == '__main__':
    import sys
    root_logger = logging.getLogger("")
    stream_handler = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter('%(name)-8s %(asctime)s %(levelname)-8s %(message)s', '%a, %d %b %Y %H:%M:%S',)
    stream_handler.setFormatter(formatter)
    root_logger.addHandler(stream_handler)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)

    proxyes = fetch_all()
    for p in proxyes:
        print p
