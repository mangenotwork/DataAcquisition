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


'''
testurl = "http://tiku.xj5u.com/zhishidian.aspx"

postdatas = {
    "stype": "sel_sj",
    "type": "nj",
    "id": 1
}


post_html(testurl,postdatas)

time.sleep(1)
'''



'''
postdatas2 = {
    "stype": "sel_sj",
    "type": "topic",
    "id": 51
}
post_html(testurl,postdatas2)
'''


'''
postdatas3 = {
    "stype": "sel_sj",
    "type": "page",
    "pageIndex": 2
}

datas = post_html(testurl,postdatas3)

print(datas)
'''



test1 = "http://tiku.xj5u.com/search.aspx?sc=1-0-0-0-0-1"

datas1 = get_html(test1)


#print(datas1)


def get_ul_list(html):
    #print(html)
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@id="ctl00_ContentPlaceHolder1_question"]')
    t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
    return t.decode("utf-8")

#print(get_ul_list(datas1))


def get_li1(html,ii):
    #ctl00_ContentPlaceHolder1_repeaterData_ctl01_Div1
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@id="ctl00_ContentPlaceHolder1_repeaterData_ctl0'+str(ii)+'_Div1"]')
    t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
    return t.decode("utf-8")


#lidata = get_li1(datas1)


def get_txt_li1(html):
    #ctl00_ContentPlaceHolder1_repeaterData_ctl01_Div1
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@id="ctl00_ContentPlaceHolder1_repeaterData_ctl01_Div1"]//text()')
    
    return info


def get_typeinfo(html):
    #ctl00_ContentPlaceHolder1_repeaterData_ctl01_Div1
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@class="topic-title clearfix"]//text()')
    
    return info



#infodatas1 = get_typeinfo(lidata)



#getdada = get_txt_li1(datas1)

#print(getdada)
'''
infoaaa = []
for aac in infodatas1:
    aab = aac.replace(" ","")
    if aab != "\r\n" and aab != "\r\n\r\n":
        print(aab)
        infoaaa.append(aab)
'''
#aaaa = "".join(getdada)
#print(aaaa.replace(" ",""))


def get_id(html):
    html = str(html)
    reg = r"\d+"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data





def get_ti(html,ids):
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@id="stem_'+str(ids)+'"]')
    print(info)
    t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
    return t.decode("utf-8")






#获取答案
def get_daan(html,ids):
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//span[@id="answer_'+str(ids)+'"]')
    t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
    return t.decode("utf-8")



csv_data_file = "F://tiku_yw_6_2.csv"

def run_pg(url):
    urls = url
    pgdatas = get_html(urls)
    i=0
    while i<10:
        #获取题目
        lidatas = get_li1(pgdatas,i)
        infodatas = get_typeinfo(lidatas)
        print(infodatas)
        infoaaa = []
        for aac in infodatas:
            aab = aac.replace(" ","")
            if aab != "\r\n" and aab != "\r\n\r\n":
                #print(aab)
                infoaaa.append(aab)
        #题目信息
        print(infoaaa)
        ids = get_id(infoaaa[0])[0]
        #题型
        ti_type = infoaaa[1]
        #考点
        kaodian = infoaaa[2]
        #难度
        nandu = infoaaa[3]
        #题目ID
        print(ids)
        #获取题目
        timu = get_ti(lidatas,ids)
        print(timu)
        #获取答案
        daan = get_daan(lidatas,ids)
        print(daan)
        

        if "测试&#13;" not in timu:
            input_datas = ["语文","六年级下",ti_type,kaodian,nandu,timu,daan]
            with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
                csv_write = csv.writer(f,dialect='excel')
                csv_write.writerow(input_datas)

        print("\n\n")
        i+=1





n=725
while n<798:
    urls = "http://tiku.xj5u.com/search.aspx?sc=12-0-0-0-0-"+str(n)
    print(urls)
    run_pg(urls)
    time.sleep(2)
    n+=1

