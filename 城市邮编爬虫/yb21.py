#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'Man Li' 

import os
import re
import sys
import time
import json
import random
import requests
from requests.exceptions import ReadTimeout, ConnectionError, RequestException
import csv

from lxml import etree


from multiprocessing import Process


from itertools import chain


defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


#USER_AGENTS 随机头信息
USER_AGENTS = [
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; AcooBrowser; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.0; Acoo Browser; SLCC1; .NET CLR 2.0.50727; Media Center PC 5.0; .NET CLR 3.0.04506)",
    "Mozilla/4.0 (compatible; MSIE 7.0; AOL 9.5; AOLBuild 4337.35; Windows NT 5.1; .NET CLR 1.1.4322; .NET CLR 2.0.50727)",
    "Mozilla/5.0 (Windows; U; MSIE 9.0; Windows NT 9.0; en-US)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 2.0.50727; Media Center PC 6.0)",
    "Mozilla/5.0 (compatible; MSIE 8.0; Windows NT 6.0; Trident/4.0; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET CLR 1.0.3705; .NET CLR 1.1.4322)",
    "Mozilla/4.0 (compatible; MSIE 7.0b; Windows NT 5.2; .NET CLR 1.1.4322; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 3.0.04506.30)",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN) AppleWebKit/523.15 (KHTML, like Gecko, Safari/419.3) Arora/0.3 (Change: 287 c9dfb30)",
    "Mozilla/5.0 (X11; U; Linux; en-US) AppleWebKit/527+ (KHTML, like Gecko, Safari/419.3) Arora/0.6",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.8.1.2pre) Gecko/20070215 K-Ninja/2.1.1",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9) Gecko/20080705 Firefox/3.0 Kapiko/3.0",
    "Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5",
    "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.8) Gecko Fedora/1.9.0.8-1.fc10 Kazehakase/0.5.6",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_3) AppleWebKit/535.20 (KHTML, like Gecko) Chrome/19.0.1036.7 Safari/535.20",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; fr) Presto/2.9.168 Version/11.52",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/2.0 Safari/536.11",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E; LBBROWSER)",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 LBBROWSER",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E; QQBrowser/7.0.3698.400)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; SV1; QQDownload 732; .NET4.0C; .NET4.0E; 360SE)",
    "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)",
    "Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/5.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; .NET4.0E)",
    "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.89 Safari/537.1",
    "Mozilla/5.0 (iPad; U; CPU OS 4_2_1 like Mac OS X; zh-cn) AppleWebKit/533.17.9 (KHTML, like Gecko) Version/5.0.2 Mobile/8C148 Safari/6533.18.5",
    "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:2.0b13pre) Gecko/20110307 Firefox/4.0b13pre",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:16.0) Gecko/20100101 Firefox/16.0",
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11",
    "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"
]

#构造请求头
HEADER = {
    'User-Agent': random.choice(USER_AGENTS),
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',

}




proxies = {
  "http": "http://119.101.115.209:9999",
  "https": "https://1.192.244.90:9999",
}

#Get网页，返回内容
def get_html( url_path, payload = '', cookies = '',proxies = ''):
    try:
        s = requests.Session()
        r = s.get(
                url_path,#路径
                headers=HEADER,#请求头
                params=payload,#传参 @payload 字典或者json
                cookies=cookies,#cookies
                verify=False,#SSL验证 @verify False忽略;True开启
                proxies=proxies,#代理
                timeout=30)#@timeout 超时单位 秒
        r.raise_for_status()
        #防止中文乱码
        r.encoding = 'gb2312'
        return r.text
    except ReadTimeout:
        print('Timeout')
        time.sleep(5)
        return get_html(url_path)
    except ConnectionError:
        print('Connection error')
        time.sleep(5)
        return get_html(url_path)
    except RequestException:
        print('RequestException')
        time.sleep(5)
        return get_html(url_path)



def get_headers( url_path, payload = '', cookies = '',proxies = ''):
    try:
        s = requests.Session()
        r = s.get(
                url_path,#路径
                headers=HEADER,#请求头
                params=payload,#传参 @payload 字典或者json
                cookies=cookies,#cookies
                verify=True,#SSL验证 @verify False忽略;True开启
                proxies=proxies,#代理
                timeout=30)#@timeout 超时单位 秒
        r.raise_for_status()
        #print r.headers#获取响应头
        #print r.cookies#获取cookies
        return r.headers
    except ReadTimeout:
        print('Timeout')
    except ConnectionError:
        print('Connection error')
    except RequestException:
        print('RequestException')

def get_now_Location( url_path, payload = '', cookies = '',proxies = ''):
    try:
        s = requests.Session()
        r = s.get(
                url_path,#路径
                headers=HEADER,#请求头
                params=payload,#传参 @payload 字典或者json
                cookies=cookies,#cookies
                verify=True,#SSL验证 @verify False忽略;True开启
                proxies=proxies,#代理
                timeout=30)#@timeout 超时单位 秒
        r.raise_for_status()
        #print r.headers#获取响应头
        #print r.cookies#获取cookies
        return r.url
    except ReadTimeout:
        print('Timeout')
    except ConnectionError:
        print('Connection error')
    except RequestException:
        print('RequestException')



#Post  
def post_html( url_path, datas, payload = '', cookies = '',proxies = ''):
    try:
        s = requests.Session()
        r = s.post(
                url_path,#路径
                headers=HEADER,
                data = datas,#请求头
                params=payload,#传参 @payload 字典或者json
                cookies=cookies,#cookies
                verify=True,#SSL验证 @verify False忽略;True开启
                proxies=proxies,#代理
                timeout=30)#@timeout 超时单位 秒
        #r.raise_for_status()
        #print r.headers#获取响应头
        #print r.cookies#获取cookies
        return r.text
    except ReadTimeout:
        print('Timeout')
    except ConnectionError:
        print('Connection error')
    except RequestException:
        print('RequestException')








#匹配所有<href>
def h1h1(html):
    reg = r"<h1.+?</ul>"
    reger = re.compile(reg)
    data = re.findall(reger, str(html))
    return data


def filter_td(html):
    html = str(html)
    reg = r"<td.+?>(.+?)</td>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data

def get_a(html):
    html = str(html)
    reg = r"<a.+?>(.+?)</a>"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

def filter_href(html):
    html = str(html)
    reg = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

def filter_href_2(html):
    html = str(html)
    reg = r"<a.+?href=(.+?)>"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

def filter_href_3(html):
    html = str(html)
    reg = r"<a.+?href=\"(.+?)\">"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

def get_span_title(html):
    html = str(html)
    reg = r"<span.+?title=\"(.+?)\">.+?</span>"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

def get_txt(html):
    #'>(.*)<'
    html = str(html)
    reg = r"<[^>]+>"
    reger = re.compile(reg)
    data = reger.sub("", html)
    return data


#获取邮编
def get_youbian(html):
    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('/html/body/table[2]/tbody/tr[1]/td/h1/text()')
    #print(info)
    #t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
    
    return info[0]


#获取城市
def get_chengshi(html):
    #/html/body/table[2]/tbody/tr[2]/td[2]
    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('/html/body/table[2]/tbody/tr[2]/td[2]')
    #print(info)
    t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
    
    return t.decode("utf-8")


#获取地区
def get_diqu(html):
    #/html/body/table[2]/tbody/tr[3]/td/table/tbody
    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('/html/body/table[2]/tbody/tr[3]/td/table/tbody')
    #print(info)
    t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
    
    return t.decode("utf-8")


'''
#首页遍历到各个城市
print()
aaa = filter_href_2(datas)
for aa in aaa:
    hrefs = "http://www.yb21.cn"+aa
    print(hrefs,"\n")
'''

'''
#城市遍历到各个邮编
urltest2 = "http://www.yb21.cn/post/city/1101.html"
datas2 = get_html(urltest2)
bbb = filter_href_3(datas2)
for bb in bbb:
    if "code" in bb:
        hrefs = "http://www.yb21.cn"+bb
        print(hrefs,"\n")
'''


urltest3 = "http://www.yb21.cn/post/code/838200.html"


#获取数据的总接口
def get_datas_info(urls):
    datas3 = get_html(urls)
    youbiannumber = get_youbian(datas3) #邮政编码
    print("[邮政编码] = "+youbiannumber)
    #/html/body/table[2]/tbody/tr[1]/td/h1
    #print(get_chengshi(datas3))
    chengshi = get_txt(get_chengshi(datas3))
    print("[城市] = "+chengshi)
    shen = chengshi.split("-")[0].strip()
    shi = chengshi.split("-")[1].strip()
    xian = chengshi.split("-")[2].strip()
    
    #print(get_diqu(datas3))
    diqu = filter_td(get_diqu(datas3))
    print("[地区] = "+str(diqu))
    for adddatas in diqu:
        if ('\xa0' in adddatas) and ('<td>' not in adddatas):
            diqu_val = adddatas.strip()
            print("[邮政编码] = "+youbiannumber)
            print("[省] = "+shen)
            print("[市] = "+shi)
            print("[县] = "+xian)
            print("[地区] = "+diqu_val)
            #写入数据到csv
            addlist = [youbiannumber,shen,shi,xian,diqu_val]
            print(addlist)
            with open("D:/youbian_2.csv", 'a', newline='', encoding='utf-8') as f:
                print(" ===>   add ok !!!")
                csv_write = csv.writer(f,dialect='excel')
                csv_write.writerow(addlist)
            print("__________________________________\n")


#get_datas_info(urltest3)


#2级运行函数
def run2(urls): 
    datas2 = get_html(urls)
    bbb = filter_href_3(datas2)
    for bb in bbb:
        if "code" in bb:
            hrefs = "http://www.yb21.cn"+bb
            print(hrefs,"\n")
            get_datas_info(hrefs)


#run2("http://www.yb21.cn/post/city/1101.html")

#1级主运行函数
def run1():
    testurl = "http://www.yb21.cn/post/"
    datas = get_html(testurl)
    aaa = filter_href_2(datas)
    for aa in aaa:
        hrefs = "http://www.yb21.cn"+aa
        print(hrefs,"\n")
        run2(hrefs)



run1()

