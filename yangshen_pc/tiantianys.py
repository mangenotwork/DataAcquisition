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



#test 1
# 营养科普
uerl_1 = "http://www.ttys5.com/shanshi/yingyang/index.html"

'''
testdata = get_html(uerl_1)
#print(filter_href(testdata))
for urldata in filter_href(testdata):
    if "/shanshi/yingyang/" in urldata and "h" == urldata[0] and "l"==urldata[-1] and len(urldata.split("/")) == 7:
        print(urldata)
        print("\n")
'''

def get_urllist(url,yanzheng):
    print("[get url] = "+str(url))
    testdata = get_html(url)
    urllist = []
    for urldata in filter_href(testdata):
        if yanzheng in urldata and "h" == urldata[0] and "l"==urldata[-1] and len(urldata.split("/")) == 7:
            #print(urldata)
            #print("\n")
            urllist.append(urldata)
    return set(urllist)

#print(get_urllist(uerl_1))




uerl2 = "http://www.ttys5.com/shanshi/yingyang/2018-10-30/160741.html"  
'''http://www.ttys5.com/shanshi/yingyang/2018-10-30/160741.html'''
'''
testdata = get_html(uerl_1)
print(filter_src(testdata))

for urldata in filter_src(testdata):
    if "/shanshi/yingyang/" in urldata:
        print(urldata)
        print("\n")
'''
#testdata = get_html(uerl2)

def getimages(data,yanzheng):
    imglist = []
    for urldata in filter_src(data):
        if yanzheng in urldata:
            #print(urldata)
            #print("\n")
            imglist.append(urldata)
    return "|".join(set(imglist))

#print(getimages(testdata))



def zhuanma(data):
    data = data.replace("\xa0","")
    for bm in ["gb2312","gbk",'utf-8']:
            try:
                a = data.encode('raw_unicode_escape')
                #print(a)
                a = a.replace(b"\r\n\t",b"")

                aa = a.decode(bm)
                #print(aa)
                return aa
            except:
                continue;
    

def zhuanma2(data):
    data = data.replace("\xa0","")
    for bm in ['utf-8',"gb2312","gbk"]:
            try:
                a = data.encode('raw_unicode_escape')
                #print(a)
                a = a.replace(b"\r\n\t",b"")

                aa = a.decode(bm)
                #print(aa)
                return aa
            except Exception as e:
                print("\n\n***********************ERROR****************************")
                print(e)
                print("***********************ERROR****************************\n\n")
                continue;






def get_title(html):
    try:
        datas = etree.HTML(html)
        #print(datas)
        #/html/body/div[4]/div[1]/div[2]/h1
        #/html/body/div[6]/div[2]/div[1]/h1
        info = datas.xpath('/html/body//h1/text()')
        #print(info)
        return zhuanma2(info[0])
    except:
        return "isnull"

#print(get_title(testdata))


def get_content(html):
    datas = etree.HTML(html)
    #print(datas)
    #/html/body/div[4]/div[1]/div[2]/h1
    info = datas.xpath('/html/body//div[@class="content"]//p//text()')
    #print(info)
    conts = "".join(info[1:])
    return zhuanma(conts)



#print(get_content(testdata))


def get_content_sipu(html):
    datas = etree.HTML(html)
    #print(datas)
    #/html/body/div[4]/div[1]/div[2]/h1
    #/html/body/div[6]/div[1]/div[1]
    info = datas.xpath('/html/body//div[@class="content"]//p//text()')
    #print(info)
    #print(info)
    conts = "".join(info[1:])
    return zhuanma(conts)




def getinfo(url,keys,csv_data_file,yanzheng):
    testdata2 = get_html(url)
    print(url)
    imgs = getimages(testdata2,yanzheng)
    print(imgs)
    titles = get_title(testdata2)
    print(titles)

    neirong = get_content(testdata2)
    #neirong = get_content_sipu(testdata2)
    print(neirong)

    if neirong == "":
        neirong = "isnull"
    
    
    input_datas = [url,keys,imgs,titles,neirong]

    with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
        csv_write = csv.writer(f,dialect='excel')
        csv_write.writerow(input_datas)
    





#营养科普   2198   



def run(keys):
    
    '''
    mainurl = "http://www.ttys5.com/shanshi/yingyang/index.html"
    csv_data_file = "F:/tantanys_yingyang.csv"

    for urls in get_urllist(mainurl,"/shanshi/yingyang"):
            #print(urls)
            getinfo(urls,"营养科普",csv_data_file,"/shanshi/yingyang")

    '''


    '''

    #养生食谱    shanshi/shipu/    916
    mainurl = "http://www.ttys5.com/shanshi/shipu/index.html"
    csv_data_file = "F:/tantanys_shipu.csv"

    for urls in get_urllist(mainurl,"/shanshi/shipu"):
            #print(urls)
            getinfo(urls,"养生食谱",csv_data_file,"/shanshi/shipu")
    '''


    #养生问答  http://www.ttys5.com/shanshi/shunshi/index_408.html   408
    mainurl = "http://www.ttys5.com/shanshi/shunshi/index.html"
    csv_data_file = "F:/tantanys_wenda.csv"

    for urls in get_urllist(mainurl,"/shanshi/shunshi"):
            #print(urls)
            getinfo(urls,"养生问答",csv_data_file,"/shanshi/shunshi")



    n=2
    while n<409:
        #营养科普
        url = "http://www.ttys5.com/shanshi/shunshi/index_"+str(n)+".html"

        #养生食谱
        #url = "http://www.ttys5.com/shanshi/shipu/index_"+str(n)+".html"


        #print(get_urllist(url,"/shanshi/yingyang"))

        '''
        for urls in get_urllist(url,"/shanshi/yingyang"):
            #print(urls)
            getinfo(urls,"营养科普",csv_data_file)
        '''
        for urls in get_urllist(url,"/shanshi/shunshi"):
            #print(urls)
            try:
                getinfo(urls,"养生问答",csv_data_file,"/shanshi/shunshi")
            except:
                print("网络错误！")
            

        n+=1


run("aaa")