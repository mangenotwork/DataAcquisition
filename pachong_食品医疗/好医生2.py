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
                verify=False,#SSL验证 @verify False忽略;True开启
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


test1 = "https://www.haodf.com/hospital/DE4rO-XCoLU0KXRG0lPR5qqdfm.htm"
#datas1 = get_html(test1)
#print(datas1)


def get_yy_name(html):
    html = str(html)
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//h1[@class="hospital-name"]//text()')
    return info

#print(get_yy_name(datas1))


def get_yy_biaoqian(html):
    html = str(html)
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//span[@class="hospital-label-item"]//text()')
    return info

#print(get_yy_biaoqian(datas1))

#time.sleep(3)



testmap = "https://map.haodf.com/hospital/DE4rO-XCoLU0KXRG0lPR5qqdfm/map.htm"
testmap1 = "https://www.haodf.com/hospital/DE4roiYGYZwXCabML76GGU71e/map.htm"
#请求地图
#datasmap = get_html(testmap)
#print(datasmap)

#获取医院地址 联系方式
#//*[@id="gray"]/div[5]/table[2]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/table/tbody
def get_yy_info1(html):
    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('//table//table//table//table')
    print(info)
    t = etree.tostring(info[2], encoding="utf-8", pretty_print=True)
    
    return t.decode("utf-8")
#获取医院地址 联系方式
#print(get_yy_info1(datasmap))


#获取医院 科室信息
#https://www.haodf.com/hospital/DE4rO-XCoLU0KXRG0lPR5qqdfm/keshi.htm
#testkesi = "https://www.haodf.com/hospital/DE4rO-XCoLU0KXRG0lPR5qqdfm/keshi.htm"
#dataskesi = get_html(testkesi)
#//*[@id="gray"]/div[5]/table[3]/tbody/tr/td/table/tbody/tr/td[1]/table/tbody/tr[3]/td[2]/table
#/html/body//div[@class="m-hospital"]
def get_yy_info2(html):
    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('//table//table//table//table')
    print(info)
    if info != []:
        t = etree.tostring(info[1], encoding="utf-8", pretty_print=True)
        return t.decode("utf-8")
    else:
        return ""
#print(get_yy_info2(dataskesi))
#keshialldata = get_yy_info2(dataskesi)

#列出td的内容
def filter_td(html):
    html = str(html)
    reg = r"<td.+?>.+?</td>"
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
def get_span_title(html):
    html = str(html)
    reg = r"<span.+?title=\"(.+?)\">.+?</span>"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#print(filter_td(keshialldata))
'''
for ccc in filter_td(keshialldata):
    #print(ccc.replace("\t",""))
    dataccc = ccc.replace("\t","")
    if "</a>" in dataccc:
        print(dataccc)
        print(get_a(dataccc))
        print(filter_href(dataccc))
        print(get_span_title(dataccc))
        print("\n")
'''

#yisheninfo = "https://www.haodf.com/faculty/DE4r0BCkuHzduSn-68JtvC5s9enjZ.htm"
#yisheninfo_data = get_html(yisheninfo)

#yishen info  医生信息
def get_yishen_info(html):

    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('//table')
    print(info)
    if len(info) >= 3:
        t = etree.tostring(info[2], encoding="utf-8", pretty_print=True)
        
        return t.decode("utf-8")
    else:
        return False

#print(get_yishen_info(yisheninfo_data))

#yisheninfo_listdata = get_yishen_info(yisheninfo_data)


#列出tr的内容
def filter_tr(html):
    html = str(html)
    reg = r"<tr>.+?</tr>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data

def filter_p(html):
    html = str(html)
    reg = r"<p>(.+?)</p>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data


#print(filter_tr(yisheninfo_listdata))
'''
for ddd in filter_tr(yisheninfo_listdata):
    #print(ccc.replace("\t",""))
    dataddd = ddd.replace("\t","")
    
    if "</a>" in dataddd:
        #print(dataddd)
        print(get_a(dataddd)[0])
        print(filter_href(dataddd)[0])
        print(filter_p(dataddd)[0])
        print("\n")
'''
csv_data_file = "E:/hys_yishen_2.csv"

def ys_run(urlss,addlist):
    yisheninfo = urlss
    yisheninfo_data = get_html(yisheninfo)
    yisheninfo_listdata = get_yishen_info(yisheninfo_data)
    if yisheninfo_listdata != False:
        for ddd in filter_tr(yisheninfo_listdata):
            #print(ccc.replace("\t",""))
            dataddd = ddd.replace("\t","")
            if "</a>" in dataddd:
                #print(dataddd)
                print(get_a(dataddd)[0])
                #print(addlist)
                print(filter_href(dataddd)[0])
                print(filter_p(dataddd)[0])
                user_datas = [get_a(dataddd)[0], filter_p(dataddd)[0], "https:"+filter_href(dataddd)[0]]
                input_datas = user_datas+addlist
                #input_datas.append(get_a(dataddd)[0])
                #input_datas.append(filter_p(dataddd)[0])
                #input_datas.append("https:"+filter_href(dataddd)[0])
                with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
                    print(" ===>   add ok !!!")
                    csv_write = csv.writer(f,dialect='excel')
                    csv_write.writerow(input_datas)
                user_datas = []
                input_datas = []

                print("\n")
    else:
        print("This is Null.")



def run(urls,row,debuginfo):
    deinx_datas = get_html(urls)
    #医院名称
    yy_names = get_yy_name(deinx_datas)
    #医院标签
    yy_biaoqian = get_yy_biaoqian(deinx_datas)
    print(yy_names)
    print(yy_biaoqian)
    #地址信息电话信息 url
    map_urls = ".".join(urls.split(".")[:-1])+"/map.htm"
    print(map_urls)
    #keshi 科室信息科室url
    keshi_urls = ".".join(urls.split(".")[:-1])+"/keshi.htm"
    print(keshi_urls)
    #医院联系方式与地址信息
    datas_map = get_html(map_urls)
    yy_maps = get_yy_info1(datas_map).replace("\t","")
    print(yy_maps)
    #医院科室
    dataskesi = get_html(keshi_urls)
    keshialldata = get_yy_info2(dataskesi)
    for ccc in filter_td(keshialldata):
        print(debuginfo)
        #print(ccc.replace("\t",""))
        dataccc = ccc.replace("\t","")
        if "</a>" in dataccc:
            print(yy_names[0])#医院名称
            print("|".join(yy_biaoqian))#医院标签
            print(yy_maps)#医院联系方式与地址信息
            #print(dataccc)
            
            keshi_data = get_a(dataccc)[0]#科室名称
            print(keshi_data)
            keshi_userdata = get_span_title(dataccc)[0]#科室人数
            print(keshi_userdata)



            print(filter_href(dataccc))
            yishen_urls = "https:"+filter_href(dataccc)[0]
            #获取医生信息
            addlist =[ yy_names[0], "|".join(yy_biaoqian), yy_maps, keshi_data, keshi_userdata, yishen_urls]
            addlist = row + addlist
            ys_run(yishen_urls,addlist)
            print("\n")
    time.sleep(1)


def run3(urls,row,debuginfo):
    print(urls)
    print(debuginfo)
    #keshi 科室信息科室url
    keshi_urls = ".".join(urls.split(".")[:-1])+"/keshi.htm"
    print(keshi_urls)
    #医院科室
    dataskesi = get_html(keshi_urls)
    keshialldata = get_yy_info2(dataskesi)
    for ccc in filter_td(keshialldata):
        print(debuginfo)
        #print(ccc.replace("\t",""))
        dataccc = ccc.replace("\t","")
        if "</a>" in dataccc:
            #print(dataccc)
            if len(get_a(dataccc)) != 0:
                keshi_data = get_a(dataccc)[0]#科室名称
            else:
                keshi_data = ""
            print(keshi_data)
            keshi_userdata = get_span_title(dataccc)[0]#科室人数
            print(keshi_userdata)

            print(filter_href(dataccc))
            yishen_urls = "https:"+filter_href(dataccc)[0]
            #获取医生信息
            addlist =[ keshi_data, keshi_userdata, yishen_urls]
            addlist = row + addlist
            ys_run(yishen_urls,addlist)
            print("\n")



def run2(urls,row,debuginfo):
    deinx_datas = get_html(urls)
    #医院名称
    yy_names = get_yy_name(deinx_datas)
    #医院标签
    yy_biaoqian = get_yy_biaoqian(deinx_datas)
    #print(yy_names)
    #print(yy_biaoqian)
    #地址信息电话信息 url
    map_urls = ".".join(urls.split(".")[:-1])+"/map.htm"
    #print(map_urls)
    #keshi 科室信息科室url
    keshi_urls = ".".join(urls.split(".")[:-1])+"/keshi.htm"
    #print(keshi_urls)
    #医院联系方式与地址信息
    datas_map = get_html(map_urls)
    yy_maps = get_yy_info1(datas_map).replace("\t","")
    #print(yy_maps)
    #医院科室
    dataskesi = get_html(keshi_urls)
    keshialldata = get_yy_info2(dataskesi)
    
    addlist =[ yy_names[0], "|".join(yy_biaoqian), yy_maps]
    addlist = row + addlist
    print(addlist)
    with open("E:/haoyishen_5.csv", 'a', newline='', encoding='utf-8') as f:
        print(" ===>   add ok !!!")
        csv_write = csv.writer(f,dialect='excel')
        csv_write.writerow(addlist)


#run(test1)


#ys_run("//www.haodf.com/faculty/DE4r0BCkuHzduSn-68JtvC5s9enjZ.htm")



#读取数据
csv_path = "E:/haoyishen_3.csv"


with open(csv_path, 'r',encoding='utf-8') as f:
    data = csv.reader((line for line in f), delimiter=",")
    #data = csv.reader((line for line in f), delimiter=",")
    #print(len(data))
    n=1
    
    for row in data:
        
        #8080
        #2019 09 12 09:33   6171
        
        if n>=6237:
            debuginfo = "*** [ Len info ] *** : Data len is -> "+str(n)
            print(debuginfo)
            print(row)
            urls = row[3]
            print(urls)
            print(row[0])
            yyinfo = [row[0],row[1]]
            run3(urls,yyinfo,debuginfo)
            print("\n\n\n\n")
            time.sleep(1)
        
        n+=1
    print(n)



'''
#给医院数据添加一个uuid


def set_user_uuid(src):
    m2 = hashlib.md5()   
    m2.update(src.encode('utf-8'))   
    useruuid = m2.hexdigest()
    return useruuid


with open(csv_path, 'r',encoding='utf-8') as f:
    data = csv.reader((line for line in f), delimiter=",")
    #data = csv.reader((line for line in f), delimiter=",")
    #print(len(data))
    n=1
    
    for row in data:
        uuids = set_user_uuid(row[0]+str(time.time()))
        row.insert(0,uuids)
        print(row)
        with open("E:/haoyishen_3.csv", 'a', newline='', encoding='utf-8') as f:
            print(" ===>   add ok !!!")
            csv_write = csv.writer(f,dialect='excel')
            csv_write.writerow(row)
        n+=1
    print(n)


'''
