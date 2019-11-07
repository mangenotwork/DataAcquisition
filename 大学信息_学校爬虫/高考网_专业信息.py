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
import hashlib
from lxml import etree
import redis
import urllib

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


def get_proxy():
        r = redis.StrictRedis(host='192.168.1.79',port='6379',db=1)
        ipnumber = r.zcard('proxy:ips')
        if ipnumber <= 1:
            number = 0
        else:
            number = random.randint(0, ipnumber-1)
        a = r.zrange('proxy:ips',0,-1,desc=True)
        print(a)
        print(a[number].decode("utf-8"))
        return a[number].decode("utf-8")



ip = get_proxy()
print(ip)
proxies = {"http":ip}


#Get网页，返回内容
def get_html( url_path, proxies = proxies, payload = '', cookies = ''):
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
        return get_html(url_path, {"http":get_proxy()})
    except ConnectionError:
        print('Connection error')
        time.sleep(5)
        return get_html(url_path, {"http":get_proxy()})
    except RequestException:
        print('RequestException')
        time.sleep(5)
        return get_html(url_path, {"http":get_proxy()})



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





#获取专业信息div
def get_zyinfo_div(html):
        #//*[@id="wrapper"]/div[4]/div[1]
        html = str(html)
        all_list_datas = []
        datas = etree.HTML(html)
        info = datas.xpath('/html/body//div[@class="scores_List"]')
        print(info)
        t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
        return t.decode("utf-8")



#分离出dl
def get_dl_data(html):
    reg = r"<dl.+?</dl>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data


#获取专业标题与链接
def get_a1_data(html):
    reg = r"<a.+?</a>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data[0]

def filter_href(html):
    html = str(html)
    reg = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#获取专业标题
def get_atxt_data(html):
    reg = r"<a.+?>(.+?)</a>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

#获取ul
def get_ul_data(html):
    reg = r"<ul.+?</ul>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data[0]

#获取li
def get_li_data(html):
    reg = r"<li>(.+?)</li>"
    reger = re.compile(reg)
    data = re.findall(reger, str(html))
    return data



'''
testulrs2 = "http://college.gaokao.com/speciality/355/"
datas2 = get_html(testulrs2)
#print(datas2)
'''


#获取主干学科和主要课程的html
def get_zhugan1_html(html):
    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@class="xuen_kc bk fll"]/p[1]/span/text()')
    #print(info)
    return info[0]
def get_zhugan2_html(html):
    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@class="xuen_kc bk fll"]/p[2]/span/text()')
    #print(info)
    return info[0]


'''
zuganxueke = get_zhugan1_html(datas2)
#print(zuganxueke)

zuyaokechen = get_zhugan2_html(datas2)
#print(zuyaokechen)


print("[主干学科] ： ",zuganxueke)
print("[主要课程] ： ",zuyaokechen)
'''

#获取专业概况
def get_zy_gaikuo(html):
    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info1 = datas.xpath('/html/body//div[@class="tab_con"]/div[2]/p[1]/text()')
    info2 = datas.xpath('/html/body//div[@class="tab_con"]/div[2]/p[2]/text()')
    info3 = datas.xpath('/html/body//div[@class="tab_con"]/div[2]/p[3]/text()')
    info4 = datas.xpath('/html/body//div[@class="tab_con"]/div[2]/p[4]/text()')
    data1 = "".join(info1).strip()
    data2 = "".join(info2).strip()
    data3 = "".join(info3).strip()
    data4 = "".join(info4).strip()
    return data1, data2, data3, data4

#print(get_zy_gaikuo(datas2))
'''
#教学实践,培养目标,培养要求,就业方向
jxsj,pymb,pyyq,jyfx = get_zy_gaikuo(datas2)

print("[教学实践] ： ",jxsj)
print("[培养目标] ： ",pymb)
print("[培养要求] ： ",pyyq)
print("[就业方向] ： ",jyfx)
'''


def get_zycode_qinxi(html):
    reg = r"专业代码：(.+?)$"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    if data == []:
        return ""
    else:
        return data[0]




#获取专业详细信息
def run2(urls, zy_name, xllv, menlei, xuewei, xueke, zycode, xjzy_list):

    print("[专业名] ： ",zy_name)
    print("[学历层次] ： ",xllv)
    print("[门类] ： ",menlei)
    print("[授予学位] ： ",xuewei)
    print("[学科] ： ",xueke)
    zycode = get_zycode_qinxi(zycode)
    print("[专业代码] ： ",zycode)
    print("[相近专业] ： ",xjzy_list)


    testulrs2 = urls
    datas2 = get_html(testulrs2)

    zuganxueke = get_zhugan1_html(datas2)
    #print(zuganxueke)

    zuyaokechen = get_zhugan2_html(datas2)
    #print(zuyaokechen)


    print("[主干学科] ： ",zuganxueke)
    print("[主要课程] ： ",zuyaokechen)


    #教学实践,培养目标,培养要求,就业方向
    jxsj,pymb,pyyq,jyfx = get_zy_gaikuo(datas2)

    print("[教学实践] ： ",jxsj)
    print("[培养目标] ： ",pymb)
    print("[培养要求] ： ",pyyq)
    print("[就业方向] ： ",jyfx)

    print("[专业详情链接] ： ",urls)


    #写入数据到csv
    addlist = [zy_name, xllv, menlei, xuewei, xueke, zycode, xjzy_list, zuganxueke, zuyaokechen, jxsj, pymb, pyyq, jyfx, urls]
    print(addlist)
    with open("D:/xuexuao_zhuanye_3.csv", 'a', newline='', encoding='utf-8') as f:
        print(" ===>   add ok !!!")
        csv_write = csv.writer(f,dialect='excel')
        csv_write.writerow(addlist)
    print("__________________________________\n")




def run(number):

    testurls1 = "http://college.gaokao.com/spelist/p"+str(number)+"/"
    datas1 = get_html(testurls1)
    #print(datas1)


    zyinfo_datas = get_zyinfo_div(datas1)
    #print(zyinfo_datas)
    zyinfo_list = get_dl_data(zyinfo_datas)
    #print(len(zyinfo_list))

    for zyinfo_val in zyinfo_list:
        #print(zyinfo_val,"\n")
        #专业标题与链接 html
        ai_html = get_a1_data(zyinfo_val)
        #print(ai_html)
        #专业详情链接
        zyxq_url = filter_href(ai_html)[0]
        #print("[专业详情链接] ： ",zyxq_url)

        zy_name = get_atxt_data(ai_html)[0]
        #print("[专业名] ： ",zy_name)

        #专业基础信息 html
        ul_html = get_ul_data(zyinfo_val)
        #print(ul_html)

        zyinfos_li = get_li_data(ul_html)
        #print("[专业基础信息] ： ",zyinfos_li)

        #学历层次
        xllv = zyinfos_li[0]
        #print("[学历层次] ： ",xllv)

        #门类
        menlei = zyinfos_li[1]
        #print("[门类] ： ",menlei)

        #授予学位
        xuewei = zyinfos_li[2]
        #print("[授予学位] ： ",xuewei)

        #学科
        xueke = zyinfos_li[3]
        #print("[学科] ： ",xueke)

        #专业代码
        zycode = zyinfos_li[4]
        #print("[专业代码] ： ",zycode)

        #相近专业
        xjzy_list = zyinfos_li[5]
        #print("[相近专业] ： ",xjzy_list)

        #zy_name,xllv,menlei,xuewei,xueke,zycode,xjzy_list
        run2(zyxq_url, zy_name, xllv, menlei, xuewei, xueke, zycode, xjzy_list)


        print("______________________________________\n\n")





n=1
while n<82:
    print("____________________***** "+str(n)+" *****____________________________")
    run(n)
    time.sleep(1)
    n+=1
