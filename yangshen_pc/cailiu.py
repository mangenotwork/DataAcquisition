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
	except ConnectionError:
		print('Connection error')
	except RequestException:
		print('RequestException')



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
def filter_href(html):
    reg = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
    reger = re.compile(reg)
    data = re.findall(reger, str(html))
    return data


#匹配所有 src:
def filter_src(html):
    reg = r"(?<=src=\").+?(?=\")|(?<=src=\').+?(?=\')"
    reger = re.compile(reg)
    data = re.findall(reger, str(html))
    return data




uerl_1 = "http://www.cnys.com/article/list_34_1.html"






def get_urllist(url):
    testdata = get_html(url)
    urllist = []
    for urldata in filter_href(testdata):
        if "/article/" in urldata and "_" not in urldata and urldata[-1] == "l":
            #print(urldata)
            urllist.append(urldata)
            #print("\n")
    return set(urllist)



#print(get_urllist(uerl_1))



#获取标题
def get_title(html):
    try:
        datas = etree.HTML(html)
        #print(datas)
        #/html/body/div[4]/div[2]/div[2]/h1
        info = datas.xpath('/html/body//h1/text()')
        #print(info)
        #return zhuanma2(info[0])
        return info[0]
    except:
        return "isnull"


#获取标题
def get_title1(html):
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@class="readbox"]//h1/text()')
    return info




#获取内容
def get_content(html):
    datas = etree.HTML(html)
    #print(datas)
    #/html/body/div[4]/div[1]/div[2]/h1
    info = datas.xpath('/html/body//div[@class="reads"]//p//text()')
    #print(info)
    conts = "".join(info)
    return conts



#获取导读
def get_digest(html):
    datas = etree.HTML(html)
    #print(datas)
    #/html/body/div[4]/div[1]/div[2]/h1
    info = datas.xpath('/html/body//div[@class="digest"]//p//text()')
    #print(info)
    conts = "".join(info)
    return conts




'''
uerl2 = "http://www.cnys.com/article/72548.html"  
#uerl2 = "http://www.cnys.com/article/158.html"
testdata = get_html(uerl2)
print(get_title(testdata))

print(get_content(testdata))
'''



def run(url,keys,csv_data_file):
    testdata = get_html(url)
    titles = get_title(testdata)
    print(titles)
    neirong = get_content(testdata)
    print(neirong)
    input_datas = [url,keys,titles,neirong]

    with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
        csv_write = csv.writer(f,dialect='excel')
        csv_write.writerow(input_datas)


#run("http://www.cnys.com/article/72548.html","a","F:/cainiu_chunjiys.csv")



def go():

    #春季养生  http://www.cnys.com/article/list_34_1.html    38
    # 夏季养生 http://www.cnys.com/article/list_35_1.html    52
    # 秋季养生  http://www.cnys.com/article/list_36_1.html    28
    # 冬季养生  http://www.cnys.com/article/list_37_1.html    43

    # 美容养生  http://www.cnys.com/article/list_29_1.html    79

    # 健康减肥  http://www.cnys.com/article/list_30_1.html    64

    # 按摩常识  http://www.cnys.com/article/list_31_1.html    73

    # 饮食养生  http://www.cnys.com/article/list_32_1.html    17

    # 养生食谱  http://www.cnys.com/article/list_9_1.html    101

    # 蔬菜水果  http://www.cnys.com/article/list_11_1.html   83

    # 养生总结  http://www.cnys.com/article/list_42_1.html    101

    # 养生常识  http://www.cnys.com/article/list_2_1.html   101

    # 中老年养生  http://www.cnys.com/article/list_26_1.html   38

    # 上班族养生  http://www.cnys.com/article/list_41_1.html   35

    # 儿童养生   http://www.cnys.com/article/list_27_1.html   53

    # 经络  http://www.cnys.com/article/list_19_1.html   24

    # 针灸  http://www.cnys.com/article/list_20_1.html   15

    # 穴位  http://www.cnys.com/article/list_21_1.html   69

    # 药膳  http://www.cnys.com/article/list_22_1.html    51

    # 瑜伽  http://www.cnys.com/article/list_14_1.html     37

    # 健身  http://www.cnys.com/article/list_15_1.html    71

    # 太极  http://www.cnys.com/article/list_16_1.html    13

    # 气功  http://www.cnys.com/article/list_17_1.html    11

    key = "养生总结"
    csv_data_file = "F:/cainiu_zongjie.csv"

    n=1
    while n<101:
        url = "http://www.cnys.com/article/list_42_"+str(n)+".html"
        print(url)
        for wenzhang in get_urllist(url):
            '''
            print("http://www.cnys.com"+wenzhang,key,csv_data_file)
            run("http://www.cnys.com"+wenzhang,key,csv_data_file)
            time.sleep(1)
            '''
            try:
                print("http://www.cnys.com"+wenzhang,key,csv_data_file)
                run("http://www.cnys.com"+wenzhang,key,csv_data_file)
                time.sleep(2)
            except Exception as e:
                print(e)


go()


