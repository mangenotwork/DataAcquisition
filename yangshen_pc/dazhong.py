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




#test 1
#饮食养生
#uerl_1 = "https://www.cndzys.com/yinshi/index.html"

'''
testdata = get_html(uerl_1)

#print(filter_href(testdata))

for urldata in filter_href(testdata):
    if "/yinshi/changshi/" in urldata and "/" == urldata[0] and "l"==urldata[-1]:
        print(urldata)
        print("\n")
'''






def get_title(html):
    datas = etree.HTML(html)
    #print(datas)
    #/html/body/div[4]/div[1]/div[2]/h1
    info = datas.xpath('/html/body//h1/text()')
    #print(info)
    return info

def get_content(html):
    datas = etree.HTML(html)
    #print(datas)
    #/html/body/div[4]/div[1]/div[2]/h1
    info = datas.xpath('/html/body//div[@class="content_text"]//text()')
    #print(info)
    return info



def zhuanma(data):
    a = data.encode('raw_unicode_escape')
    #print(a)
    a = a.replace(b"\r\n\t",b"")
    aa = a.decode('utf-8')
    #print(aa)
    return aa




#uerl_2 = "https://www.cndzys.com/yinshi/changshi/1882050.html"
'''
testdata2 = get_html(uerl_2)


title = get_title(testdata2)
print(title)

print(zhuanma(title[0]))
input_datas = [get_title(testdata2)]

cont = get_content(testdata2)

cotdadad = "".join(cont)
cotdadad = cotdadad.replace("\r\n\t","")
print(zhuanma(cotdadad))
'''





def getinfo(url,keys):
    testdata2 = get_html(url)
    title = get_title(testdata2)
    #print(title)
    print(zhuanma(title[0]))
    
    cont = get_content(testdata2)
    cotdadad = "".join(cont)
    cotdadad = cotdadad.replace("\r\n\t","")
    print(zhuanma(cotdadad))
    input_datas = [url,keys,zhuanma(title[0]),zhuanma(cotdadad)]

    with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
        csv_write = csv.writer(f,dialect='excel')
        csv_write.writerow(input_datas)


#getinfo(uerl_2)

#饮食养生爬虫
def getallurl(uerl):
    testdata = get_html(uerl)
    for urldata in set(filter_href(testdata)):

        if "/yinshi/" in urldata and "/" == urldata[0] and "l"==urldata[-1] and len(urldata.split("/")) == 4:
            print(urldata)
            getinfo("https://www.cndzys.com"+urldata,"饮食")
            print("\n")

#饮食养生爬虫
def getallurl2(uerl):
    testdata = get_html(uerl)
    for urldata in set(filter_href(testdata)):
        try:
            if "/yinshi/" in urldata and "/" == urldata[0] and "l"==urldata[-1] and len(urldata.split("/")) == 4:
                print(urldata)
                getinfo("https://www.cndzys.com"+urldata,"饮食")
                print("\n")
        except:
            print("aaa")

# 运动养生     
def getallurl_yund(uerl):
    testdata = get_html(uerl)
    for urldata in set(filter_href(testdata)):
        try:
            if "/yundong/" in urldata and "/" == urldata[0] and "l"==urldata[-1] and len(urldata.split("/")) == 4:
                print(urldata)
                getinfo("https://www.cndzys.com"+urldata,"运动")
                print("\n")
        except:
            print("aaa")




# 生活养生     
def getallurl_shenhuo(uerl):
    testdata = get_html(uerl)
    for urldata in set(filter_href(testdata)):
        try:
            if "/shenghuoyangsheng/" in urldata and "/" == urldata[0] and "l"==urldata[-1] and len(urldata.split("/")) == 4:
                print(urldata)
                getinfo("https://www.cndzys.com"+urldata,"生活")
                print("\n")
        except:
            print("aaa")



# 两性     
def getallurl_liangxin(uerl):
    testdata = get_html(uerl)
    for urldata in set(filter_href(testdata)):
        try:
            if "/liangxingyangsheng/" in urldata and "/" == urldata[0] and "l"==urldata[-1] and len(urldata.split("/")) == 4:
                print(urldata)
                getinfo("https://www.cndzys.com"+urldata,"两性健康")
                print("\n")
        except:
            print("aaa")




#人群  https://www.cndzys.com/renqun/   renqun   17702
def getallurl_renqun(uerl):
    testdata = get_html(uerl)
    for urldata in set(filter_href(testdata)):
        try:
            if "/renqun/" in urldata and "/" == urldata[0] and "l"==urldata[-1] and len(urldata.split("/")) == 4:
                print(urldata)
                getinfo("https://www.cndzys.com"+urldata,"人群")
                print("\n")
        except:
            print("aaa")





#中医  https://www.cndzys.com/zhongyi/index5847.html     zhongyi    5848
def getallurl_zhongyi(uerl):
    testdata = get_html(uerl)
    for urldata in set(filter_href(testdata)):
        try:
            if "/zhongyi/" in urldata and "/" == urldata[0] and "l"==urldata[-1] and len(urldata.split("/")) == 4:
                print(urldata)
                getinfo("https://www.cndzys.com"+urldata,"中医")
                print("\n")
        except:
            print("aaa")








#饮食养生
'''
url1 = "https://www.cndzys.com/yinshi/index.html"
getallurl2(url1)
'''

'''
#运动养生
#https://www.cndzys.com/yundong/
url1 = "https://www.cndzys.com/yundong/index.html"
getallurl_yund(url1)
'''

'''
#生活养生  shenghuoyangsheng
url1 = "https://www.cndzys.com/shenghuoyangsheng/index.html"
getallurl_shenhuo(url1)
'''

'''
#两性   liangxingyangsheng
url1 = "https://www.cndzys.com/liangxingyangsheng/index.html"
getallurl_liangxin(url1)
'''


#人群  https://www.cndzys.com/renqun/   renqun   17702
url1 = "https://www.cndzys.com/renqun/index.html"
getallurl_renqun(url1)

'''
#中医  https://www.cndzys.com/zhongyi/index5847.html     zhongyi    5848
url1 = "https://www.cndzys.com/zhongyi/index.html"
getallurl_zhongyi(url1)
'''

csv_data_file = "F:/dzys_renqun.csv"
n=2
while n<17702:
    #饮食养生   14256
    #urls = "https://www.cndzys.com/yinshi/index"+str(n)+".html"
    #getallurl2(urls)

    '''
    #运动养生   663
    urls = "https://www.cndzys.com/yundong/index"+str(n)+".html"
    getallurl_yund(urls)
    '''

    '''
    #生活养生   5186
    urls = "https://www.cndzys.com/shenghuoyangsheng/index"+str(n)+".html"
    getallurl_shenhuo(urls)
    '''

    '''
    #两性   251
    urls = "https://www.cndzys.com/liangxingyangsheng/index"+str(n)+".html"
    getallurl_liangxin(urls)
    '''

    
    #人群    17702
    urls = "https://www.cndzys.com/renqun/index"+str(n)+".html"
    getallurl_renqun(urls)
    

    '''
    #中医    5848
    urls = "https://www.cndzys.com/zhongyi/index"+str(n)+".html"
    getallurl_zhongyi(urls)
    '''

    n+=1





'''

'''



