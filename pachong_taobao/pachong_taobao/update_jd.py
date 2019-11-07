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
import mandb
import redis
import time


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



def get_proxy1():
    try:
        r = redis.StrictRedis(host='192.168.1.62',port='6379',db=1)
        ipnumber = r.zcard('proxy:ips')
        if ipnumber <= 1:
            number = 0
        else:
            number = random.randint(0, ipnumber-1)
        a = r.zrange('proxy:ips',0,-1,desc=True)
        print(a)
        print(a[number].decode("utf-8"))
        return a[number].decode("utf-8")
    except Exception as e:
        return ""





proxies = {
  "http": "http://119.101.115.209:9999",
  "https": "https://1.192.244.90:9999",
}

#Get网页，返回内容
def get_html( url_path, payload = '', cookies = '',proxies = ''):
    print("[ GET Url ] : " + url_path)
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
        print('wite 3s...')
        time.sleep(3)
        get_html(url_path)
    except ConnectionError:
        print('Connection error')
        print('wite 3s...')
        time.sleep(3)
        '''
        print('Connection error')
        proxies_ip = {
          "http": get_proxy1()
        } 

        get_html(url_path,proxies = proxies_ip)
        '''
        get_html(url_path)
    except RequestException:
        print('RequestException')



#testurl1 = "https://c0.3.cn/stock?skuId=47974996367&area=22_1930_50947_33197&cat=1315,132,1348"


#datas1 = get_html(testurl1)



#获取info
def get_info(url):
    datainfo = get_html(url)
    html = str(datainfo)
    datas = etree.HTML(html)
    #//*[@id="J_StrPrice"]/em[2]
    #//*[@id="J_StrPrice"]
    info = datas.xpath('//*[@id="J_StrPrice"]/em/text()')
    print(info)
    return info


#获取 评论
def get_pinglun(url):
    datainfo = get_html(url)
    html = str(datainfo)
    datas = etree.HTML(html)
    #//*[@id="J_StrPrice"]/em[2]
    #//*[@id="J_StrPrice"]
    #//*[@id="J_TabBar"]/li[2]/a/em
    info = datas.xpath('//*[@id="J_TabBar"]/li[2]/a/em/text()')
    print(info)
    return info


def get_op(html):
    reg = r"\"p\":\"(.*?)\""
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data


#print(get_op(datas1))


#get_info(testurl1)

#get_pinglun(testurl1)
#<strong id="J_StrPrice"><em class="tb-rmb">&yen;</em><em class="tb-rmb-num">99.00</em></strong>
#https://item.taobao.com/item.htm?id=592571256824&ali_refid=a3_430676_1006:1214190088:N:3MsWPbg8R9Gb3Ko%2Bxbllbg%3D%3D:2bc0f672e65d822d5b10b9fe333fced0&ali_trackid=1_2bc0f672e65d822d5b10b9fe333fced0


#获取淘宝数据
#SELECT pachong_data_id,cod_link from tb_tm_pachong_data_1 WHERE pingtai = '淘宝' LIMIT 50;
def get_jd_links():
    man_db = mandb.DB()
    sql ="SELECT pachong_data_id,cod_link from jd_pachong_data_1 where substring(collection_time, 7, 1) != '8' LIMIT 100000;"
    print(sql)
    return_datas = man_db.execute_seles(sql)
    return return_datas
    


#更新淘宝数据
def updata_sql(ids,cod_price_1,collection_time):
    man_db = mandb.DB()
    sql = "UPDATE jd_pachong_data_1 set cod_price_1 = '"+cod_price_1+"',collection_time = '"+collection_time+"' where pachong_data_id = "+ids+" ;"
    man_db.execute(sql)
    print(" [ *** 更新商品信息 *** ] ")




#print(get_jd_links())



for tbdata in get_jd_links():
    ids = tbdata[0]
    print(ids)
    links = tbdata[1]
    print(links)
    jdids = links.split("/")[-1]
    jdids = jdids.split(".")[0]
    print(jdids)
    jg_url = "http://p.3.cn/prices/mgets?skuIds=J_"+jdids+"&type=1"
    print(jg_url)
    jsondatas = get_html(jg_url)
    print(jsondatas)
    print(get_op(jsondatas))
    cod_price_1 = get_op(jsondatas)
    collection_time = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
    updata_sql(str(ids),str(cod_price_1[0]),collection_time)



'''
for tbdata in get_jd_links():
    try:
        ids = tbdata[0]
        print(ids)
        links = tbdata[1]
        print(links)
        jdids = links.split("/")[-1]
        jdids = jdids.split(".")[0]
        print(jdids)
        datasjson = get_html("https://c0.3.cn/stock?skuId="+str(jdids)+"&area=22_1930_50947_33197&cat=1315,132,1348")
        cod_price_1 = get_op(datasjson)
        print(cod_price_1)

        if cod_price_1 != []:
            print(cod_price_1[0])
            collection_time = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            updata_sql(str(ids),str(cod_price_1[0]),collection_time)
        print("\n")
    except Exception as e:
        print("---")
    

'''
