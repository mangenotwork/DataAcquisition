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
    'Accept-Language': 'en-US,en;q=0.5',
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
                verify=True,#SSL验证 @verify False忽略;True开启
                proxies=proxies,#代理
                timeout=30)#@timeout 超时单位 秒
        r.raise_for_status()
        #print r.headers#获取响应头
        #print r.cookies#获取cookies
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



#test_1 = "http://www.35yao.com/invest/search.php?kw=公司&fields=4&catid=0&fromdate=&todate=&areaid=0&order=0&page=1"



def get_infolist(html):
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@class="list"]')
    print(info)
    for aa in info:
        t = etree.tostring(aa, encoding="utf-8", pretty_print=True)
        #t.decode("utf-8")
        all_list_datas.append(t.decode("utf-8"))
    return all_list_datas






def filter_a(html):
    html = str(html)
    reg = r'<a .*?>(.*?)</a>'
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data


def filter_a1(html):
    html = str(html)
    reg = r'<a .*?>.*?</a>'
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data


def filter_src(html):
    html = str(html)
    reg = r"(?<=src=\").+?(?=\")|(?<=src=\').+?(?=\')"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data


def filter_imgsrc(html):
    html = str(html)
    reg = r"<img.+?src=\"(.+?)\""
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data




#original
def filter_original(html):
    html = str(html)
    reg = r"(?<=original=\").+?(?=\")|(?<=original=\').+?(?=\')"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data


def filter_href(html):
    html = str(html)
    reg = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data




#print(get_infolist(txtx1))



'''

'''






#print(txtx2)



def get_title(html):
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//h1/text()')
    return info[0]


#/html/body/div[8]/div[1]/div[1]/table/tbody/tr/td[3]/ul

def get_info1(html):
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@class="info_main"]//ul//li')
    print(info)
    t1 = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
    t2 = etree.tostring(info[1], encoding="utf-8", pretty_print=True)
    t3 = etree.tostring(info[2], encoding="utf-8", pretty_print=True)
    all_list_datas = [t1.decode("utf-8"),t2.decode("utf-8"),t3.decode("utf-8")]
    return all_list_datas

def get_info2(html):
    try:
        print(html)
        datas = etree.HTML(html)
        info = datas.xpath('/html/body//div[@class="content"]')
        print(info)
        t1 = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
        return t1.decode("utf-8")
    except Exception as e:
        return "isNull"
    

'''

'''



def getgongsi(html):
    try:
        datas = etree.HTML(html)
        info = datas.xpath('/html/body//div[@class="brief_con"]')
        print(info)
        t1 = etree.tostring(info[1], encoding="utf-8", pretty_print=True)
        '''
        t2 = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
        all_list_datas = [t1.decode("utf-8"),t2.decode("utf-8")]
        return ''.join(all_list_datas)
        '''
        return t1.decode("utf-8")
    except Exception as e:
        return "isNull"
    




#


def get_imgaa(txtx2):
    for imgaa in filter_imgsrc(txtx2):
        if ".middle." in imgaa:
            print(imgaa)
            return imgaa
    
    return "isNull"



def url_yaoping_info(test_2):

    #test_2 = "http://www.35yao.com/invest/show-9415.html"

    txtx2 = get_html(test_2)

    print(get_title(txtx2))

    imgssss = get_imgaa(txtx2)

    print(get_info1(txtx2))
    print()
    if "<img" in get_info2(txtx2):
        info2 = "isNull"
    else:
        info2 = get_info2(txtx2)
    #药品名称 药品图片 药品信息1  药品信息2
    return [get_title(txtx2),imgssss,get_info1(txtx2),info2]


#url_yaoping_info("http://www.35yao.com/invest/show-9415.html")


def get_gongsi_info(test_3):
    #test_3 = "http://www.35yao.com/index.php?homepage=ygyygy&file=introduce"
    txtx3 = get_html(test_3)
    print(getgongsi(txtx3))
    return [getgongsi(txtx3)]


#get_gongsi_info("http://www.35yao.com/index.php?homepage=ygyygy&file=introduce")


csv_data_file = "E:/zhaoyaowang_9.csv"


def run_pachong(txtx1):
    for bb in get_infolist(txtx1):
        #print(bb)
        yp_url = filter_href(bb)[0]
        print(yp_url)
        #获取药品信息
        a_111111111 = url_yaoping_info(yp_url)
        all_a = filter_a(bb)
        print(all_a[-1])
        all_href = filter_href(bb)
        print(all_href[-1])
        #a_222222222 = get_gongsi_info(all_href[-1]+"&file=introduce")
        print()
        input_datas = a_111111111
        input_datas.append(all_a[-1])
        #input_datas+=a_222222222
        with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
            print(" ===>   add ok !!!")
            csv_write = csv.writer(f,dialect='excel')
            csv_write.writerow(input_datas)



n=1
while n<=1248:
    test_1 = "http://www.35yao.com/invest/search.php?kw=公司&fields=4&catid=0&fromdate=&todate=&areaid=0&order=0&page="+str(n)
    print("[DEBUG] =====>  "+test_1)

    txtx1 = get_html(test_1)
    run_pachong(txtx1)
    print("\n\n\n")
    n+=1









