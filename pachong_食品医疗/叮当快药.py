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
        get_html(url_path)
    except ConnectionError:
        print('Connection error')
        time.sleep(5)
        get_html(url_path)
    except RequestException:
        print('RequestException')
        time.sleep(5)
        get_html(url_path)



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










#print(type(get_html(test1)))



def get_productList(html):
    #reg = r"\{\"sku_cid3\":.*?\{\"sku_cid3"
    reg = r"\"productList\":\[.*?\}\],\"totalCount\""
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data


def get_a(html):
    reg = r"\{\"b2cDirectoryId\".*?\},"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

#id
def get_id(html):
    reg = r"\"id\":(.*?),"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data[0]

#skuId
def get_skuId(html):
    reg = r"\"skuId\":.*?,"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

#name
def get_name(html):
    reg = r"\"name\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

#imgUrl
def get_imgUrl(html):
    reg = r"\"imgUrl\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

#productDescription
def get_productDescription(html):
    reg = r"\"productDescription\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

#productMarketPrice
def get_productMarketPrice(html):
    reg = r"\"productMarketPrice\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data


#productPrice
def get_productPrice(html):
    reg = r"\"productPrice\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data


#productSpecifications
def get_productSpecifications(html):
    reg = r"\"productSpecifications\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data


#productionAddress
def get_productionAddress(html):
    reg = r"\"productionAddress\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data


#


#儿童药    010502,010503,010504,010505,010506,010507                           ok        
#感冒药    010101,010104                                                       ok
#风湿伤骨  010401,010402,010403,010404,010406,010407                            ok
#两性健康  010801,010802,010803,010804,010901,010902,010807                     ok
#三高用药  011303,010609                                                        ok
#其他药品  011501,011502,011503,011504,011505,010301,010302,010303,010305,010306,010307,011601,011602,011603,011605,010201,     ok
#         010202,010203,011401,011402,011403,011404,010701,010702,010703,010704,010706,010707,010709,010710,010711,011101,011106    ok
#名贵滋补  020101,020103,020105,020201,020202,020203            ok
#中药饮片  020301,020307,020310,020311,020315                   ok
#医疗器械  050301,050303,050305,050401,050601,050602,050604,050605,050606,050101,050106,050102  ok
#营养补品  030101,030102,030103,030107,030108,030109,030110,030111,030113           ok
#成人用品  030201,030202,030204                                                     ok
#彩妆护理  040101,040501,040502,040404,040201,040204                                ok
#婴幼用品  060901,061103,060603,060604,060607,060609,060610,060505,060301,060302,060304,060306,060803,060804,060805,060402,060403,060201,060701,060702


#print(get_productList(datas))
#datas2 = get_productList(datas)
#print(get_a(datas2[0]))

test1 = "http://product.ddky.com/product/queryOrgcodeProductListForB2C.htm?orderTypeId=0&orgcode=060901,061103,060603,060604,060607,060609,060610,060505,060301,060302,060304,060306,060803,060804,060805,060402,060403,060201,060701,060702&pageNo=1&pageSize=1000&shopId=-1"
csv_data_file = "F:/yaopinginfo_3.csv"



datas =get_html(test1)


n=1
for aaa in get_a(datas):
    print(n)
    print(aaa)
    print("婴幼用品")
    yptype = "婴幼用品"
    print(get_id(aaa))
    print(get_skuId(aaa))
    #药品名称
    yp_name = get_name(aaa)[0]
    yp_name = yp_name.replace("'","-")
    print(yp_name)
    #药品图片
    imgurl = get_imgUrl(aaa)[0]
    print(imgurl)
    #药品介绍
    pd = get_productDescription(aaa)[0]
    pd = pd.replace("'","-")
    print(pd)
    #药品市场价格
    pmprice = get_productMarketPrice(aaa)[0]
    print(pmprice)
    #药品价格 price
    price = get_productPrice(aaa)[0]
    print(price)
    #产品规格；制品技术规格
    sf = get_productSpecifications(aaa)[0]
    sf = sf.replace("'","-")
    print(sf)
    #生产地址
    address = get_productionAddress(aaa)[0]
    address = address.replace("'","-")
    print(address)
    ids= get_id(aaa)
    smshu = "http://api.ddky.com/product/productInstruction.htm?id="+ids
    smshudatas = get_html(smshu)
    #说明书地址
    print(smshu)
    #说明书
    print(smshudatas)
    print()
    input_datas = [yp_name, yptype, imgurl, pd, pmprice, price, sf, address, smshu, smshudatas]
    with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
        print(" ===>   add ok !!!")
        csv_write = csv.writer(f,dialect='excel')
        csv_write.writerow(input_datas)

    n+=1



'''


test333 = "http://api.ddky.com/product/productInstruction.htm?id=500616"

data333 = get_html(test333)
print(data333)
'''
