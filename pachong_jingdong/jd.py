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







'''

商品店家名称  

https://chat1.jd.com/api/checkChat?pidList=100000177760,100003433872,7437710,8735304,100004404934,7437786,100002962227,7652013,100003434260,100000650837,100002677997,100002071812,100000773889,100002544828,5089253,100003332220,8264403,100005150846,7081550,100004680720,7299782,100004363706,100002539302,3133827,5089275,100002493099,5089267,100002535419,100003936976,100000349372&callback=jQuery9150660&_=1557405390674


接口
https://search-x.jd.com/Search?callback=jQuery7275379&area=2&enc=utf-8&keyword=手机&adType=7&page=2&ad_ids=291%3A33&xtest=new_search&_=1557405390962


轮询page

https://search-x.jd.com/Search?enc=utf-8&keyword=手机&page=9&ad_ids=291%3A33


https://search.jd.com/s_new.php?keyword=%E6%89%8B%E6%9C%BA&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=%E6%89%8B%E6%9C%BA&cid2=653&cid3=655&page=2&s=27
'''

#只有  0~10
test1 = "https://search-x.jd.com/Search?area=22&enc=utf-8&keyword=冰箱&page=9&ad_ids=291%3A33"
test2 = "https://search-x.jd.com/Search?area=22&enc=utf-8&keyword=冰箱&page=11&ad_ids=292%3A5"
html_info = get_html(test1)
#print(html_info)


def get_totalCount(html):
    #reg = r"\{\"sku_cid3\":.*?\{\"sku_cid3"
    reg = r"\{\"sku_cid3\":.*?\}"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data



def get_data_list(html):
    if html != None:
        print(type(html))
        #print(html)
        datalist = html.split("},{")
        print(len(datalist))
        #return datalist[1:]
    else:
        datalist = ""
    return datalist

#get_data_list(html_info)

#https://item.jd.com/8795212.html
#//img14.360buyimg.com/n2/jfs/t1/32651/27/2682/58088/5c6cf032E5895fd48/9778e1a7cbac6213.jpg
#http://img14.360buyimg.com/n2/jfs/t1/31047/34/11836/68381/5cb68aadEe1ad4458/66c058fd2c7b35fc.jpg
#
#jfs/t1/40273/18/4749/40954/5ccaa281E56622fe6/dd0821c44597776c.jpg


# 商品名称，商品链接，实际价格，活动价格，图片，评价数，店家名称，店家主页，用户评价分，物流履约，售后服务，京东商城网店经营者评分信息查看地址，京东商城网店经营者资质信息查看地址



#图 ：  image_url
def get_image_url(html):
    reg = r"\"image_url\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data

#链接 ： link_url
def get_link_url(html):
    reg = r"\"link_url\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data
#店家名称 : shop_name
def get_shop_name(html):
    reg = r"\"shop_name\":\"(.*?)\"\}"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data
#价格 ： pc_price
def get_pc_price(html):
    reg = r"\"pc_price\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data
#特价  : sku_price
def get_sku_price(html):
    reg = r"\"sku_price\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data
#评价 : comment_num
def get_comment_num(html):
    reg = r"\"comment_num\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data
#商品名称 ：  ad_title
def get_ad_title(html):
    reg = r"\"ad_title\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data
#店家主页  ：  shop_id    https://mall.jd.com/index-shop_id.html
def get_shop_id(html):
    reg = r"\"shop_id\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data


def get_spu_id(html):
    reg = r"\"spu_id\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data
    


'''
{"sku_cid3":"878",
#http:\/\/item.jd.com\/44561544196.html
#http://item.jd.com/43825404425.html
"link_url":"https:\/\/item.jd.com\/41911101705.html",
"monitor_url":"9b9171757fe127e7^v2.8^SWC^291^^142810257^^403799655^https:\/\/item.jd.com\/41911101705.html^e1186c63-6a83-485b-9fac-60bcf200daf9^1^0^761801^",
"color":"白色",
"promo_desc":"",
"exposal_url":"https:\/\/im-x.jd.com\/dsp\/np?log=qljOuUlXaLTlTmncXvdL01cvbKMpwGIdTGSQKKVe46ijJalPiMYYkYMTsrBtZy0mAO7mG68EoZCRtsd9xL8g-uz8K191U_INUFCRNnpvvhp0ukwSHLy55QW14h_h6c8geKg5TWiN26lHVHz6gxLTFcr6gjpfVbSy2__rv6Nym3cwxVke01iVlJI2EXYKnFDgpmT97-UThSYWprjLYjgrYEJf4DB1lqoTtlA0efxHDNv_nIwJzwWFvGT2_IXZ4wzzSjzQGEyFTLlpSfo-Hr2TuZSqBQgpxT_7wwjOpOcwd8joP5DNg_qQKO2m4hC8yfw_NyRuogqOJMruuwCwGTDWvM8ZWBKAX8R2gE1yY_-1OGNChG5sWIJ-9fiv-fM8_18C24wy7_W7JnXKBvE76oGscOozngahMONVYIVuxcpAq1oRBj6XdcMtRccz2qpk18OsZ29S6Y7HY7Z2RArVilLAp2Dslk5OFMW9_nagSKKaqE0
pDQmHuSqr4Vuxsz0PetzvXW2jHcnqYXb6HVt2uC71WyQLq6-DsvcPjTDyfEZoQLi8S8koV4xi7iWELd2xSrUe8LQ9HaC9Mb_tUWWIy1nNgDnY0FIIrgFpbaVZX6qNXreoaS734X7HcMzQn3wXWsnJ1dvEORF2wXJit3sMK4zObFbHNb9kRv_7_eKwEnij5B8OKVJKD-waVXPSFMPG2nPVPiP1vEJVrlJ0poFpCoJA47Tpc7rcCwgYQhx6irVAxGJY4Q9HQ3NRFOB3MUZ1ciQ0Dg5DPfUEVkR62Aeu9PB24KAmrg-no2-z2NgrvToyxFI&v=404&rt=3",
"icon_url":"",
"fuzzy_comment_num":"50+",
"abt":"0",
"good_rate":"86",
"ad_title":"海尔（Haier）<font class=\"skcolor_ljg\">冰箱<\/font> 多门 对开门风冷无霜528升两门双门双开门变频超薄节能家用 电<font class=\"skcolor_ljg\">冰箱<\/font> <font class=\"skcolor_ljg\">新品<\/font> 白色",
"vender_id":"761801",
"promo_title":"",
"ad_type":"3",
"ad_spread_type":"1",
"comment_num":"57",
"long_image_url":"",
"shop_link":{"good_shop":"0",
"shop_name":"海尔威斯专卖店"}


'''



#评分
#https://mall.jd.com/view/getJshopHeader.html?appId=686366

test3 = "https://mall.jd.com/view/getJshopHeader.html?appId=686366"
html_info3 = get_html(test3)
#print(html_info3)


def get_urls(html):
    reg = r"href=\\\"(.*?)\\\""
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data


def get_td(html):
    reg = r"<td>(.*?)<\/td>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data



def get_span(html):
    reg = r"<span.*?>(.*?)<\/span>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data



def get_olany_name(html):
    html = str(html)
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub('',html)
    #print(dd)
    return dd

def get_jd_data_1(keys,csv_data_file,html_info):

        
    
        #v=1
        # 商品名称，商品链接，实际价格，活动价格，图片，评价数，店家名称，店家主页，用户评价分，物流履约，售后服务，京东商城网店经营者评分信息查看地址，京东商城网店经营者资质信息查看地址
        for datas in get_data_list(html_info):
            try:
                global shop_fen_s,shop_fen_w,shop_fen_w_lve,shop_fen_f,shop_fen_f_lve,shopLevel_info,showLicence_info
                #print(v)
                print(datas)
                print("[商品名称] --> ")
                #print(get_ad_title(datas))
                cod_name = get_ad_title(datas)
                if cod_name !=[]:
                    #print(cod_name[0])
                    cod_name = get_olany_name(cod_name[0])
                else:
                    cod_name = "isNull"
                print(cod_name)
                print(type(cod_name))


                print("[商品链接] --> ")
                cod_link = get_link_url(datas)
                if cod_link != []:
                    cod_link = cod_link[0].replace("\\","")
                else:
                    cod_link = "isNull"
                print(cod_link)
                print(type(cod_link))

                print("[平台] --> ")
                pingtai = "京东商城"
                print(pingtai)

                print("[实际价格] --> ")
                cod_price_1 = get_pc_price(datas)
                if cod_price_1 != []:
                    cod_price_1 = cod_price_1[0]
                else:
                    cod_price_1 = "isNull"
                print(cod_price_1)
                print(type(cod_price_1))

                print("[活动价格] --> ")
                cod_price_2 = get_sku_price(datas)
                if cod_price_2 != []:
                    cod_price_2 = cod_price_2[0]
                else:
                    cod_price_2 = "isNull"
                print(cod_price_2)
                print(type(cod_price_2))

                print("[图片] --> ")
                title_img_link = get_image_url(datas)
                if title_img_link != []:
                    title_img_link = title_img_link[0].replace("\\","")
                    title_img_link = "http://img14.360buyimg.com/n2/"+title_img_link
                else:
                    title_img_link = "isNull"
                print(title_img_link)
                

                print("[评价数] --> ")
                cod_sales = get_comment_num(datas)
                if cod_sales != []:
                    cod_sales = cod_sales[0]
                else:
                    cod_sales = "isNull"
                print(cod_sales)

                print("[店家名称] --> ")
                cod_shop_name = get_shop_name(datas)
                if cod_shop_name != []:
                    cod_shop_name = cod_shop_name[0]
                else:
                    cod_shop_name = "isNull"
                print(cod_shop_name)
                
                print("[店家id] --> ")
                cod_shop_id = get_shop_id(datas)
                if cod_shop_id !=[]:
                    cod_shop_id = cod_shop_id[0]
                    test3 = "https://mall.jd.com/view/getJshopHeader.html?appId="+cod_shop_id
                    html_info3 = get_html(test3)
                    dd = get_td(html_info3)
                    print(dd)
                    if dd != []:
                        dd1 = get_span(dd[1])
                        print("用户评价：")
                        print(dd1)
                        if len(dd1) >= 2:
                            
                            shop_fen_s = dd1[0]
                            
                            
                            shop_fen_s_lve = dd1[1]
                            
                        else:
                            shop_fen_s = "isNull"
                            shop_fen_s_lve = "isNull"
                        '''
                        print("[用户评价 评分] --> ")
                        print(shop_fen_s)
                        print("[用户评价 等级] --> ")
                        print(shop_fen_s_lve)
                        '''

                        dd2 = get_span(dd[4])
                        print("物流履约：")
                        print(dd2)
                        if len(dd2) >= 2:
                            
                            shop_fen_w = dd2[0]
                            
                            
                            shop_fen_w_lve = dd2[1]
                            
                        else:
                            shop_fen_w = "isNull"
                            shop_fen_w_lve = "isNull"
                        '''
                        print("[物流履约 评分] --> ")
                        print(shop_fen_w)
                        print("[物流履约 等级] --> ")
                        print(shop_fen_w_lve)
                        '''

                        dd3 = get_span(dd[-2])
                        print("售后服务：")
                        print(dd3)
                        if len(dd3) >= 2:
                            
                            shop_fen_f = dd3[0]
                            
                            
                            shop_fen_f_lve = dd3[1]
                        else:
                            shop_fen_f = "isNull"
                            shop_fen_f_lve = "isNull"

                        '''
                        print("[物流履约 评分] --> ")
                        print(shop_fen_f)
                        print("[物流履约 等级] --> ")
                        print(shop_fen_f_lve)
                        '''

                        for c in set(get_urls(html_info3)):
                            #print(c)
                            if "shopLevel" in c:
                                #print("京东商城网店经营者评分信息")
                                #print(c)
                                shopLevel_info = c
                            if "showLicence" in c:
                                #print("京东商城网店经营者资质信息")
                                #print(c)
                                showLicence_info = c

                        '''
                        print("京东商城网店经营者评分信息")
                        print(shopLevel_info)
                        print("京东商城网店经营者资质信息")
                        print(showLicence_info)
                        '''
                        
                else:
                    print("店家id：null")
                    shop_fen_s = "isNull"
                    shop_fen_s_lve = "isNull"
                    shop_fen_w = "isNull"
                    shop_fen_w_lve = "isNull"
                    shop_fen_f = "isNull"
                    shop_fen_f_lve = "isNull"
                    shopLevel_info = "isNull"
                    showLicence_info = "isNull"


                '''
                print("[用户评价 评分] --> ")
                print(shop_fen_s)

                
                print("[用户评价 等级] --> ")
                print(shop_fen_s_lve)

                print("[物流履约 评分] --> ")
                print(shop_fen_w)
                print("[物流履约 等级] --> ")
                print(shop_fen_w_lve)

                print("[物流履约 评分] --> ")
                print(shop_fen_f)
                print("[物流履约 等级] --> ")
                print(shop_fen_f_lve)

                print("京东商城网店经营者评分信息")
                print(shopLevel_info)
                print("京东商城网店经营者资质信息")
                print(showLicence_info)
                '''


                print(get_shop_id(datas))

                collection_time = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

                print("\n\n\n")
                #v+=1
                #分类，商品名称，商品链接，
                input_datas = [keys,cod_name,cod_link,pingtai,cod_price_1,cod_price_2,title_img_link,cod_sales,
                                cod_shop_name,shop_fen_s,shop_fen_s_lve,shop_fen_w,shop_fen_w_lve,
                                shop_fen_f,shop_fen_f_lve,shopLevel_info,showLicence_info,collection_time]
                #print('D:/py_test/yibiao_Auto/report/xyzg_data/tb_test1.csv')

                #input_datas = [cod_name1,cod_name2]
                with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
                    csv_write = csv.writer(f,dialect='excel')
                    csv_write.writerow(input_datas)
            except:
                print("遇到了一个问题....")
            continue
'''
#print(get_urls(html_info3))

for c in set(get_urls(html_info3)):
	#print(c)
	if "shopLevel" in c:
		print("京东商城网店经营者评分信息")
		print(c)
	if "showLicence" in c:
		print("京东商城网店经营者资质信息")
		print(c)

#print(get_td(html_info3))

dd = get_td(html_info3)
dd1 = get_span(dd[1])
print("用户评价：")
print(dd1)

'''


def get_shop_info(shop_id):
    shop_info_list = []
    test3 = "https://mall.jd.com/view/getJshopHeader.html?appId="+shop_id
    html_info3 = get_html(test3)
    dd = get_td(html_info3)
    print(dd)
    if dd != []:
        dd1 = get_span(dd[1])
        print("用户评价：")
        print(dd1)
        if len(dd1) >= 2:        
            shop_fen_s = dd1[0]
            shop_fen_s_lve = dd1[1]
                            
        else:
            shop_fen_s = "isNull"
            shop_fen_s_lve = "isNull"
        
        shop_info_list.append(shop_fen_s)
        shop_info_list.append(shop_fen_s_lve)

        dd2 = get_span(dd[4])
        print("物流履约：")
        print(dd2)
        if len(dd2) >= 2:
            shop_fen_w = dd2[0]
            shop_fen_w_lve = dd2[1]  
        else:
            shop_fen_w = "isNull"
            shop_fen_w_lve = "isNull"

        shop_info_list.append(shop_fen_w)
        shop_info_list.append(shop_fen_w_lve)

        dd3 = get_span(dd[-2])
        print("售后服务：")
        print(dd3)
        if len(dd3) >= 2:
            shop_fen_f = dd3[0]
            shop_fen_f_lve = dd3[1]
        else:
            shop_fen_f = "isNull"
            shop_fen_f_lve = "isNull"

        shop_info_list.append(shop_fen_f)
        shop_info_list.append(shop_fen_f_lve)


        for c in set(get_urls(html_info3)):
            #print(c)
            if "shopLevel" in c:
                #print("京东商城网店经营者评分信息")
                #print(c)
                shopLevel_info = c
                shop_info_list.append(shopLevel_info)
            if "showLicence" in c:
                #print("京东商城网店经营者资质信息")
                #print(c)
                showLicence_info = c    
                shop_info_list.append(showLicence_info)        

    #shop_info_list = [shop_fen_s,shop_fen_w,shop_fen_w_lve,shop_fen_f,shop_fen_f_lve,shopLevel_info,showLicence_info]
    if len(shop_info_list) == 0:
        shop_info_list = ["isNull","isNull","isNull","isNull","isNull","isNull","isNull","isNull"]
    
    print(str(shop_info_list))

    return shop_info_list


def get_jd_data_2(keys,csv_data_file,html_info):
    for datas in get_data_list(html_info):
        try:
            print(datas)
            print("\n\n\n")
            
            print("[商品名称] --> ")
            cod_name = get_ad_title(datas)
            #print(cod_name[0])
            if cod_name !=[]:
                cod_name = get_olany_name(cod_name[0])
                cod_name = cod_name.replace("'","")
            else:
                cod_name = "isNull"
            print(cod_name)
            print(type(cod_name))
            print("\n")
            print("[商品链接] --> ")
            #cod_link = get_link_url(datas)
            cod_link = get_spu_id(datas)
            #print(get_link_url(datas))
            if cod_link != []:
                cod_link = "http://item.jd.com/"+str(cod_link[0])+".html"
                #cod_link = cod_link[0].replace("\\","")
            else:
                cod_link = "isNull"
            print(cod_link)
            print(type(cod_link))
            print("\n")
            #print(get_spu_id(datas))

            
            print("[平台] --> ")
            pingtai = "京东商城"
            print(pingtai)

            print("[实际价格] --> ")
            cod_price_1 = get_pc_price(datas)
            if cod_price_1 != []:
                cod_price_1 = cod_price_1[0]
            else:
                cod_price_1 = "isNull"
            print(cod_price_1)
            print(type(cod_price_1))

            print("[活动价格] --> ")
            cod_price_2 = get_sku_price(datas)
            if cod_price_2 != []:
                cod_price_2 = cod_price_2[0]
            else:
                cod_price_2 = "isNull"
            print(cod_price_2)
            print(type(cod_price_2))

            print("[图片] --> ")
            title_img_link = get_image_url(datas)
            if title_img_link != []:
                title_img_link = title_img_link[0].replace("\\","")
                title_img_link = "http://img14.360buyimg.com/n2/"+title_img_link
            else:
                title_img_link = "isNull"
            print(title_img_link)
                    

            print("[评价数] --> ")
            cod_sales = get_comment_num(datas)
            if cod_sales != []:
                cod_sales = cod_sales[0]
            else:
                cod_sales = "isNull"
            print(cod_sales)

            print("[店家名称] --> ")
            cod_shop_name = get_shop_name(datas)
            if cod_shop_name != []:
                cod_shop_name = cod_shop_name[0]
            else:
                cod_shop_name = "isNull"
            print(cod_shop_name)
                    
            print("[店家id] --> ")
            cod_shop_id = get_shop_id(datas)
            if cod_shop_id !=[]:
                cod_shop_id = cod_shop_id[0]
                shop_infodata = get_shop_info(cod_shop_id)
                
            print(get_shop_id(datas))

            collection_time = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))
            print(collection_time)
            print("\n\n\n")
            input_datas = [keys,cod_name,cod_link,pingtai,cod_price_1,cod_price_2,title_img_link,cod_sales,
                                    cod_shop_name] + shop_infodata
            input_datas.append(collection_time)
            #print('D:/py_test/yibiao_Auto/report/xyzg_data/tb_test1.csv')
            print("input Data = "+str(input_datas))
            #input_datas = [cod_name1,cod_name2]
            
            with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
                csv_write = csv.writer(f,dialect='excel')
                csv_write.writerow(input_datas)
        
            
        except:
            print("网络环境异常")
        continue

'''
dd2 = get_span(dd[4])
print("物流履约：")
print(dd2)
dd3 = get_span(dd[-2])
print("售后服务：")
print(dd3)

'''

'''
for d in get_td(html_info3):
	#print(d)
	print(get_span(d))
'''
#https://mall.jd.com/view/getJshopHeader.html?appId=677256
#京东营业执照   //mall.jd.com/showLicence-677256.html


#联系卖家   //chat.jd.com/pop/chat?shopId=677256









keys=["T恤","长袖T恤","卫衣","开衫","女装","男装","袜子","短袜","丝袜","婚纱","伴娘服","下装","裤子","裙子","连衣裙","旗袍","蛋糕群",
        "运动鞋","篮球鞋","板鞋","皮鞋","高跟鞋","网球鞋","帆布鞋","凉鞋","拖鞋","手机","iphone","华为","小米","oppo","vivo",
        "魅族","一加","荣耀","联想","充电宝","电视","冰箱","冰柜","风扇","油烟机","按摩椅","皮带","手套","手表","粉底","口红",
        "唇彩","香水","洗面奶","护肤霜","乳液","发蜡","剃须刀","电脑","照相机","投影仪","打印机","猪肉脯","内裤","女士内裤",
        "男士内裤","睡衣","情趣内衣"]

#keys=["T恤"]

all_keys = ["T恤","长袖T恤","卫衣","开衫","女装","男装","袜子","短袜","丝袜","婚纱","伴娘服","下装","裤子","裙子","连衣裙","旗袍","蛋糕群",
        "运动鞋","篮球鞋","板鞋","皮鞋","高跟鞋","网球鞋","帆布鞋","凉鞋","拖鞋","手机","iphone","华为","小米","oppo","vivo",
        "魅族","一加","荣耀","联想","充电宝","电视","冰箱","冰柜","风扇","油烟机","按摩椅","皮带","手套","手表","粉底","口红",
        "唇彩","香水","洗面奶","护肤霜","乳液","发蜡","剃须刀","电脑","照相机","投影仪","打印机","猪肉脯","内裤","女士内裤",
        "男士内裤","睡衣","情趣内衣","女人","连衣裙冬","睡衣夏","女装","女鞋","凉鞋","拖鞋","帆布鞋", "连衣裙","裙子",
        "裙子夏", "夏连衣裙", "旗袍", "背带裙", "蛋糕裙", "婚纱", "裙", "伴娘服", "沙滩裙", "敬酒服", "小礼服", "晚礼服",
        "秀禾服", "新娘礼服", "红色礼服", "真丝旗袍","上衣","大码装", "针织短袖", "胖mm装", "卫衣", "闺蜜装", "针织外套",
        "大码女装", "胖妹妹装", "大码裤", "外搭开衫", "胖mm裤子", "休闲上衣", "工装外套", "胖mm套装", "防晒开衫", "空调衫",
        "裤子", "短裤", "阔腿裤", "运动裤", "连体裤", "工装裤", "裤", "安全裤", "九分裤", "七分裤", "打底裤", "直筒裤", 
        "西装套装", "哈伦裤", "裙裤", "高腰短裤", "五分裤", "鞋子", "鞋子夏", "夏季鞋", "布鞋", "板鞋", "包头凉鞋", "半拖鞋",
        "凉拖鞋", "拖鞋夏", "平底凉鞋", "大东鞋", "一脚蹬鞋", "皮鞋", "情侣鞋", "夏季凉鞋", "人字拖鞋", "洞洞鞋",
        "内衣","睡衣春秋", "睡衣性感", "睡裙夏", "情侣睡衣", "情趣睡衣", "家居服夏", "夏季睡衣", "真丝睡衣", "短袜", "睡衣", 
        "棉绸睡衣", "隐形袜", "水手服", "袜子", "船袜", "冰丝睡衣","配饰","耳钉", "墨镜", "耳钉纯银", "潘多拉", "手链情侣", 
        "周生生", "红绳手链", "小方巾", "波点", "真丝", "防晒披肩", "方巾", "围脖", "耳骨钉", "耳钉气质", "纱巾", "男人",
        "潮男鞋", "男鞋", "汉服", "T恤", "情侣装", "牛仔裤", "男士衬衫", "工装裤男", "上衣","短袖", "男装秋冬", "t恤短袖", 
        "汉服男", "半袖男", "打底衫", "半袖", "男短袖T", "衬衣", "冰丝t恤", "班服定制", "夏季装", "潮牌t恤", "唐装男", 
        "supreme", "boy短袖", "下装","男裤", "休闲裤", "袜子男", "九分裤", "短裤男潮", "短裤潮", "运动裤", "薄款男裤", 
        "七分裤", "睡衣男", "情侣睡衣", "睡衣男夏", "袜子男潮", "哈伦裤男", "沙滩裤", "直筒裤男", "鞋子", "运动鞋", "板鞋男", 
        "豆豆鞋男", "板鞋", "休闲鞋", "人字拖男", "豆豆鞋", "情侣鞋", "沙滩鞋", "海澜之家", "情侣拖鞋", "休闲皮鞋", "潮男凉鞋", 
        "沙滩鞋男", "鞋运动鞋", "阿迪", "配饰","背带裤", "皮带", "腰带", "dw手表", "手套", "浪琴", "阿玛尼", "防晒手套", "儿童手表",
        "运动手表", "皮带男潮", "对戒", "卡地亚", "天王手表", "西铁城", "防晒袖套", "汽摩装备","平衡车", "摩托车", "头盔男",
        "代步车", "机车", "摩托", "儿童头盔", "宝马", "agv头盔", "鬼火", "宝马摩托", "机车头盔", "踏板车", "雅马哈", "杜卡迪", 
        "复古头盔", "数码", "手机", "耳机", "充电宝", "华为", "冰箱", "风扇", "风扇", "无线耳机", "大家电","电视机", "小冰箱",
        "油烟机", "抽油烟机", "海尔冰箱", "冰柜", "小米电视", "爱奇艺", "美的冰箱", "小型冰箱", "液晶电视", "容声冰箱", "美菱冰箱", 
        "小冰柜", "电冰箱", "吸油烟机", "生活家电","养生壶", "火锅", "电煮锅", "小火锅", "火锅锅", "充电风扇", "落地扇", 
        "电炒锅", "电火锅", "炖锅", "电锅", "炖盅", "电炖盅", "电炖锅", "电热锅", "宿舍风扇", "个人家电", "护膝", "艾灸", 
        "靠垫", "艾灸盒", "护腰带", "护腰", "艾灸条", "按摩枕", "制氧机", "艾柱", "艾灸仪", "氧气瓶", "呼吸机", "按摩椅垫", 
        "按摩垫", "护颈","休闲家电", "投影仪", "打印机", "耳塞", "运动耳机", "铁三角", "beats", "索尼耳机", "打印照片", "扩音器", 
        "森海塞尔", "降噪耳机", "耳麦", "游戏耳机", "电脑耳机", "投影", "3d打印机","电脑相机手机", "vivo", "oppo", "华为手机", 
        "平板电脑", "苹果手机", "ipad", "智能手表", "vivo手机", "三星", "荣耀", "平板", "诺基亚", "魅族", "小米手机", "充电器", 
        "iphone7", "数码配件", "小风扇", "漫威", "移动电源", "罗马仕", "moda", "耳机套", "小恶魔", "marvel", "苹果官网", 
        "汽车风扇", "耳机包", "耳机盒", "电宝", "小米风扇", "爱国者", "充电", "母婴", "泡泡机", "孕妇夏装", "外套", "儿童凉鞋", 
        "背带裤", "男童凉鞋", "孕妇装", "孕妇裤", "童装", "开衫", "女童裤子", "马甲", "女童外套", "男童外套", "防蚊裤", 
        "男童短裤", "宝宝裤子", "宝宝外套", "儿童裤子", "儿童外套", "宝宝衣服", "女童裤", "婴儿外套", "包屁衣", "女童上衣", 
        "童鞋", "配饰", "宝宝凉鞋", "儿童拖鞋", "童鞋", "婴儿凉鞋", "学步鞋", "婴儿鞋", "宝宝鞋", "童鞋凉鞋", "宝宝网鞋", 
        "儿童发饰", "女孩凉鞋", "绿鞋", "gap", "儿童发夹", "女宝凉鞋", "基诺浦", "益智玩具", "刀", "泡泡枪", "hottoys", "泡泡", 
        "吹泡泡", "泡泡液", "儿童汽车", "电动汽车", "炉石传说", "兵人", "奔驰", "穿越火线", "碰碰车", "兵器", "dnf", "电动童车", 
        "奶粉辅食", "饼干", "奶粉", "益生菌", "钙片", "磨牙棒", "爱他美", "飞鹤奶粉", "日本零食", "a2奶粉", "君乐宝", "婴儿奶粉", 
        "飞鹤", "一件代发", "妈咪爱", "美素佳儿", "合生元", "婴童用品", "奶瓶", "纸尿裤", "餐椅", "尿不湿", "湿巾", "拉拉裤", 
        "宝宝餐椅", "巴布豆", "湿纸巾", "贝亲奶瓶", "儿童餐椅", "婴儿湿巾", "贝亲", "花王", "尿片", "尤妮佳", "孕产必备", 
        "孕妇裙", "孕妇短裤", "孕妇", "吸乳器", "孕妇春装", "孕妇短袖", "孕妇装夏", "孕妇长裙", "孕妇长裤", "孕妇裤夏", "哺乳裙", 
        "孕妇裙夏", "孕妇半袖", "孕妇T", "孕妇衣服", "十月妈咪", "家居", "雨伞", "收纳箱", "鞋架", "鞋柜", "沙发垫", "保温杯", 
        "洗衣液", "花盆架","整理收纳", "挂钩", "收纳柜", "收纳袋", "储物柜", "整理箱", "压缩袋", "工具箱", "储物箱", "衣架挂钩", 
        "粘钩", "门后挂钩", "厨房挂钩", "周转箱", "吸盘", "真空袋", "收纳抽屉", "居家日用", "太阳伞", "遮阳伞", "喜糖盒", 
        "伞", "气球", "折叠雨伞", "同学录", "生日布置", "防晒伞", "礼品盒", "长柄雨伞", "礼品袋", "天堂伞", "晴雨伞", 
        "儿童雨伞", "明星同款","清洁洗护", "垃圾箱", "化妆镜", "蟑螂药", "老鼠药", "斑马", "小镜子", "梳妆镜", "杀虫剂", 
        "台式镜子", "灭鼠器", "老鼠夹", "粘鼠板", "蓝月亮", "蚂蚁药", "蟑螂", "蟑螂屋", "厨房餐饮", "茶壶", "饮料", "保温杯女", 
        "紫砂壶", "榨汁杯", "密封瓶", "特百惠", "塑料水杯", "玻璃罐", "泡茶壶", "迪士尼", "玻璃茶壶", "玻璃瓶", "塑料杯", 
        "膳魔师", "杯套", "家纺家饰", "凉席", "抱枕", "冰丝凉席", "装饰画", "床头靠垫", "床席1.8m", "靠枕", "壁画", "床头",
        "挂画", "竹席", "草席", "靠垫", "沙发坐垫", "沙发罩", "画", "家具建材", "花架", "多肉植物", "电脑桌", "办公桌", 
        "布艺沙发", "盆栽", "绿萝", "欧式沙发", "北欧沙发", "真皮沙发", "小桌子", "美式沙发", "鞋架多层", "床上书桌", "铁艺花架",
        "简易鞋架","美食", "酸奶", "芒果", "牛肉干", "方便面", "螺丝粉", "糖果", "小零食", "白酒", "各地特产", "猪肉铺", "牛肉", 
        "肉松", "湖南特产", "四川特产", "鱼干", "小鱼干", "肉干", "牛板筋", "鸡翅", "风干牛肉", "小鱼仔", "牛肉粒", "清真", 
        "猪手", "清真食品", "休闲零食", "酒", "棒棒糖", "糖", "喜糖", "海苔", "锅巴", "薄荷糖", "棉花糖", "五粮液", "爆米花", 
        "膨化食品", "龙角散", "茅台", "乐事薯片", "软糖", "麦芽糖", "各类坚果", "花生", "花生仁", "腰果", "板栗", "杏仁", 
        "巴旦木", "花生米", "越南腰果", "多味花生", "杏仁片", "栗子", "黑花生", "甘栗仁", "竹炭花生", "蜂蜜杏仁", "坚果杏仁", 
        "茗茶冲饮", "绿茶叶", "安慕希", "代餐", "食品", "魔芋", "黑芝麻", "白凉粉", "减肥餐", "脱脂奶粉", "代餐粉", "五谷杂粮", 
        "葛根粉", "伊利", "抹茶粉", "西湖龙井", "土豆粉", "生鲜蔬果", "肯德基", "鸡胸肉", "下饭菜", "黄桃罐头", "芒果新鲜", 
        "罐头", "榨菜", "泡菜", "咸菜", "水果罐头", "菜", "萝卜干", "黄桃", "辣白菜", "鸡", "湖北特产","粮油米面", "泡面", 
        "酸辣粉", "大米", "整箱泡面", "干脆面", "火锅底料", "米", "海底捞", "米线", "养生茶", "汤达人", "金戈", "螺狮粉", 
        "热干面", "粉丝", "干吃面", "美妆", "口红", "洗发水", "电动牙刷", "洗面奶", "香水", "沐浴乳", "剃须刀", "粉底液", 
        "基础护肤", "水乳", "化妆品", "护肤品", "精华液", "水乳套装", "洗脸仪", "护肤套装", "百雀羚", "黛珂", "冻干粉", "美容仪", 
        "洁面仪", "自然堂", "芙丽芳丝", "玻尿酸", "洁面", "精致妆容", "纹身贴", "唇釉", "粉底", "口红小样", "kiko口红", "ysl口红", 
        "kiko", "fresh", "3ce口红", "nyx", "纹身", "变色唇膏", "兰蔻口红", "dior口红", "rmk", "唇彩", "气质香氛", "男士香水", 
        "瘦腿神器", "纯露", "ck香水", "栀子花", "朵拉朵尚", "马油皂", "手工皂", "祖马龙", "玫瑰纯露", "洗脸皂", "祛疤", "coco香水", 
        "兰蔻香水", "高夫", "安娜苏", "美发护发", "卷发棒", "染发剂", "发胶", "阿道夫", "发蜡", "染发", "染发膏", "夹板", "露华浓", 
        "卷发神器", "一洗黑", "弹力", "吕洗发水", "定型喷雾", "蛋卷", "直板夹", "个人护理", "牙刷", "脱毛液", "脱毛", "欧舒丹", 
        "漂胡剂", "脱毛蜜蜡", "欧姆龙", "脱毛纸", "泡泡浴", "欧乐b", "去毛膏", "护手霜", "搓泥", "薇婷", "永久脱毛", "口腔护理",
        "男士护肤", "刮胡刀", "飞利浦", "男士面膜", "男士护肤", "飞科", "博朗", "男士美白", "超人", "剃须", "胡子刀", "男剃须刀", 
        "奔腾", "乳液面霜", "洗面奶", "护肤霜", "乳液", "箱包", "小ck", "小ck女包", "背包", "腰包", "腰包", "斜挎男包", "卡套", 
        "行李箱", "女包", "ck包", "zara", "背包", "小ck包", "链条包", "电脑包", "草编包", "透明包", "cos", "帆布袋", 
        "托特包", "ysl女包", "小方包", "夏小包", "珍珠包", "稻草人包", "男包", "男背包", "挎包", "健身包", "邮差包", "信封", 
        "男包", "镭射包", "公文包", "帆布男包", "休闲包", "男腰包", "手机腰包", "男手包", "男挎包", "ck包", "信封男包", 
        "旅行包袋", "行李袋", "密码箱", "登机箱", "旅行包", "皮箱", "行李包", "旅行袋", "小行李箱", "拉杆包", "箱包", 
        "旅游包", "行李", "手提箱", "旅行箱", "rimowa", "日默瓦", "运动包", "双肩包", "mcm", "户外用品", "小背包", "运动包", 
        "男手机包", "匡威书包", "臂包", "运动腰包", "男腰包", "小熊包", "手机腰包", "耐克书包", "mk双肩包", "跑步腰包", 
        "行李牌", "运动用品", "功能小包", "卡包", "手机包", "公交卡套", "驾驶证", "钱包", "驾照套", "卡片包", "卡夹", "驾驶证套", 
        "长款钱包", "钥匙包", "真皮钱包", "短款钱包", "锁匙包", "银行卡套", "驾照本"]



list_all_2 = ["纹身", "变色唇膏", "兰蔻口红", "dior口红", "rmk", "唇彩", "气质香氛", "男士香水", 
        "瘦腿神器", "纯露", "ck香水", "栀子花", "朵拉朵尚", "马油皂", "手工皂", "祖马龙", "玫瑰纯露", "洗脸皂", "祛疤", "coco香水", 
        "兰蔻香水", "高夫", "安娜苏", "美发护发", "卷发棒", "染发剂", "发胶", "阿道夫", "发蜡", "染发", "染发膏", "夹板", "露华浓", 
        "卷发神器", "一洗黑", "弹力", "吕洗发水", "定型喷雾", "蛋卷", "直板夹", "个人护理", "牙刷", "脱毛液", "脱毛", "欧舒丹", 
        "漂胡剂", "脱毛蜜蜡", "欧姆龙", "脱毛纸", "泡泡浴", "欧乐b", "去毛膏", "护手霜", "搓泥", "薇婷", "永久脱毛", "口腔护理",
        "男士护肤", "刮胡刀", "飞利浦", "男士面膜", "男士护肤", "飞科", "博朗", "男士美白", "超人", "剃须", "胡子刀", "男剃须刀", 
        "奔腾", "乳液面霜", "洗面奶", "护肤霜", "乳液", "箱包", "小ck", "小ck女包", "背包", "腰包", "腰包", "斜挎男包", "卡套", 
        "行李箱", "女包", "ck包", "zara", "背包", "小ck包", "链条包", "电脑包", "草编包", "透明包", "cos", "帆布袋", 
        "托特包", "ysl女包", "小方包", "夏小包", "珍珠包", "稻草人包", "男包", "男背包", "挎包", "健身包", "邮差包", "信封", 
        "男包", "镭射包", "公文包", "帆布男包", "休闲包", "男腰包", "手机腰包", "男手包", "男挎包", "ck包", "信封男包", 
        "旅行包袋", "行李袋", "密码箱", "登机箱", "旅行包", "皮箱", "行李包", "旅行袋", "小行李箱", "拉杆包", "箱包", 
        "旅游包", "行李", "手提箱", "旅行箱", "rimowa", "日默瓦", "运动包", "双肩包", "mcm", "户外用品", "小背包", "运动包", 
        "男手机包", "匡威书包", "臂包", "运动腰包", "男腰包", "小熊包", "手机腰包", "耐克书包", "mk双肩包", "跑步腰包", 
        "行李牌", "运动用品", "功能小包", "卡包", "手机包", "公交卡套", "驾驶证", "钱包", "驾照套", "卡片包", "卡夹", "驾驶证套", 
        "长款钱包", "钥匙包", "真皮钱包", "短款钱包", "锁匙包", "银行卡套", "驾照本"]


'''


连衣裙冬半身裙裙子夏长裙旗袍背带裙
上衣
防晒衣 妈妈夏装 牛仔外套 中年夏装 妈妈装 中老年装
裤子
裤连体裤工装裤阔腿裤牛仔裤背带裤
鞋子
小白鞋高跟鞋帆布鞋运动女鞋鞋子夏鞋子
内衣
睡衣夏睡衣春秋睡衣性感睡裙夏船袜蕾丝内裤
配饰
帽墨镜手链情侣女士手链手链

T恤 男士衬衫 短袖 男装 秋冬 情侣装 半袖男
下装
工装裤男男裤休闲裤袜子男短裤潮短裤男潮
鞋子
潮男鞋男鞋帆布鞋男板鞋男休闲鞋板鞋
配饰
帽子男遮阳帽渔夫帽手环棒球帽防晒帽
汽摩装备
摩托车头盔男jbl机车儿童头盔摩托
运动户外
跑步鞋皮肤衣防晒服泳装徒步


空调冰箱电视机小冰箱格力空调海尔冰箱
生活家电
电饭煲风扇充电风扇雪糕模具火锅电煮锅
个人家电
体重秤艾灸护膝按摩棒艾灸盒体脂秤
休闲家电
耳机无线耳机mp3苹果7耳塞打印机
电脑相机手机
手机手机壳华为vivo华为手机oppo
数码配件
充电宝漫威移动电源游戏手柄手柄


背带裤男童外套女 童裤子 男童 春装男童短裤 宝宝裤子
童鞋&配饰
儿童凉鞋男童凉鞋儿童拖鞋宝宝凉鞋女童装女童凉鞋
益智玩具
泡泡机乐高乐高积木抱枕毛绒玩具积木
奶粉辅食
饼干奶粉米粉婴儿奶粉飞鹤奶粉钙片
婴童用品
婴儿推车婴儿车纸尿裤奶瓶儿童推车婴儿床
孕产必备
孕妇夏装孕妇装孕妇裙连衣裙妈咪包

收纳箱晾衣架挂钩手提袋整理箱工具箱
居家日用
雨伞灭蚊器太阳伞遮阳伞喜糖盒伞
清洁洗护
垃圾箱抽纸纸巾收纳卫生纸卷纸
厨房餐饮
茶杯碗玻璃杯杯子玻璃饮料不沾锅
家纺家饰
沙发垫四件套地垫地毯无印良品装饰画
家具建材
台灯布艺沙发电脑桌车饰摆件办公桌


牛肉干猪肉铺牛肉湖南特产四川特产小鱼干
休闲零食
面包糖果啤酒小零食全麦面包棒棒糖
各类坚果
花生花生仁腰果瓜子巴西松子干果零食
茗茶冲饮
酸奶三只松鼠矿泉水花茶苏打水玫瑰花
生鲜蔬果
小龙虾牛排下饭菜黄桃罐头罐头榨菜
粮油米面
螺丝粉方便面泡面酸辣粉粽子



卸妆液水乳卸妆水芦荟胶化妆品面霜
精致妆容
眼影盒眼影盘眼影口红唇釉定妆粉
气质香氛
香水男士香水纯露ck香水祖马龙香水女士
美发护发
吹风机卷发棒护发素染发剂护发精油夹板
个人护理
电动牙刷身体乳脱毛液牙刷手霜凡士林
男士护肤
剃须刀刮胡刀飞利浦曼秀雷敦男士面膜]
'''


txt = """
双肩包 情侣包 旅行包 登山包   运动服 休闲服 春秋装 情侣装   猫眼石 水晶兔 珍珠串 首饰盒   电冰箱 洗衣机 电风扇 淋浴器 国宴酒 婚庆酒 礼品酒 高度酒   学步车 羊奶粉 孕妇装 婴儿床   布沙发 席梦思 竹凉席 餐饮具   盆栽花 水族箱 宠物犬 波斯猫
女装男装
潮流女装 羽绒服 毛呢大衣 毛衣 冬季外套 新品 裤子 连衣裙 腔调  时尚男装 秋冬新品 淘特莱斯 淘先生 拾货 秋冬外套 时尚套装 潮牌 爸爸装  性感内衣 春新品 性感诱惑 甜美清新 简约优雅 奢华高贵 运动风 塑身 基础内衣  羽绒服 轻薄款 长款 短款 毛领 加厚 被子 鹅绒 新品  秋外套 秋款 夹克 卫衣 西装 风衣 皮衣 毛呢外套 薄羽绒  文胸 无钢圈 无痕文胸 蕾丝内衣 运动文胸 聚拢文胸 大码文胸 抹胸式 隐形  呢外套 廓形 双面呢 羊绒 中长款 短款 毛领 设计师款 系带  衬衫/T恤 T恤 长袖T 打底衫 纯色 衬衫 长袖款 商务款 时尚款  家居服 睡衣套装 睡裙 睡袍浴袍 外穿家居 女士睡衣 男士睡衣 情侣睡衣 亲子睡衣  毛衣 马海毛 貂绒 羊绒 羊毛 开衫 中长款 短款 卡通  男士裤子 休闲裤 工装裤 运动裤 长裤 牛仔裤 小脚裤 哈伦裤 直筒裤  内裤 女士内裤 男士内裤 三角裤 平角裤 丁字裤 阿罗裤 星期裤 低腰  外套上衣 外套 套装 风衣 卫衣 真皮皮衣 马甲 小西装 唐装 中老年  针织毛衫 薄毛衣 针织开衫 圆领毛衣 V领毛衣 纯色毛衣 民族风 羊毛衫 羊绒衫  丝袜 船袜 男人袜 连裤袜 隐形袜 收腹裤 塑身衣 美体裤 收腹带
鞋类箱包
女鞋 帆布鞋 高帮 低帮 内增高 懒人鞋 厚底 韩版 系带 情侣款 运动风鞋 厚底 内增高 星星鞋 系带  潮流女包 上新 人气款 单肩包 斜挎包 手提包 迷你包 手拿包 小方包  帽子 棒球帽 鸭舌帽 遮阳帽 渔夫帽 草帽 平顶帽 嘻哈帽 贝雷帽 牛仔帽 爵士帽  单鞋 高跟 平底 厚底 中跟 粗跟 坡跟 浅口 尖头 圆头 运动款 头层牛皮 内增高 松糕鞋 豆豆鞋  精品男包 商务 休闲 潮范 胸包 腰包 单肩 斜跨 手提 手拿 帆布 牛皮  腰带 女士腰带 男士皮带 帆布腰带 腰封 腰链 针扣头 平滑扣 自动扣 真皮 正品  运动风鞋 厚底 内增高 星星鞋 系带 一脚蹬 魔术贴 气垫 网状  双肩包 印花 铆钉 水洗皮 卡通 原宿 糖果色 商务 运动 帆布 牛皮  围巾 女士围巾 男士围巾 披肩 丝巾 假领 小方巾 三角巾 大方巾 真丝 雪纺 棉质 亚麻 蕾丝  男鞋 青春潮流 商务皮鞋 休闲皮鞋 正装皮鞋 商务休闲 布洛克 内增高 反绒皮 真皮 潮流低帮 韩版 英伦 复古 铆钉 编织 豹纹 大头  旅行箱 拉杆箱 密码箱 学生箱 子母箱 拉杆包 万向轮 飞机轮 航空箱 铝框  手套 女士手套 男士手套 真皮手套 蕾丝手套 防晒手套 半指手套 分指手套 连指手套 短款手套 长款手套  休闲男鞋 皮鞋 低帮 反绒皮 大头鞋 豆豆鞋 帆船鞋 懒人鞋 帆布/板鞋 高帮 凉鞋/拖鞋 沙滩鞋 人字拖 皮凉鞋 洞洞鞋  热门 钱包 潮包馆 真皮包 手机包 大牌 coach MK MCM  其他配件 毛线 鞋垫 鞋带 领带 领结 袖扣 手帕 布面料 耳套 领带夹 婚纱配件 皮带扣 
母婴用品
宝宝奶粉 英国牛栏 英国爱他美 美赞臣 雅培 澳洲爱他美 可瑞康 惠氏 贝因美  婴童用品 推车 驱蚊器 婴儿床 理发器 奶瓶 餐椅 背带腰凳 安全座椅  孕产必备 内衣 内裤 喂奶枕 收腹带 妈咪包 待产包 防辐射服 储奶袋  辅食营养 米粉 肉松 磨牙棒 果泥 益生菌 清火开胃 钙铁锌 维生素  纸尿裤 花王 moony 大王 帮宝适 雀氏 好奇 妈咪宝贝 安儿乐  海外直邮 海淘奶粉 海淘辅食 海淘营养品 直邮花王 海淘洗护 海淘奶瓶 海淘餐具 海淘孕产  童装 T恤 连衣裙 泳装 套装 衬衫 防晒服 半身裙 短裤  童鞋 凉鞋 沙滩鞋 洞洞鞋 网鞋 学步鞋 拖鞋 帆布鞋 宝宝鞋  亲子鞋服 母女裙 父子装 亲子T恤 亲子衬衫 亲子套装 母女鞋 父子鞋 家庭鞋  玩具 沙滩戏水 早教启蒙 拼插益智 遥控模型 运动户外 学习爱好 卡通公仔 亲子互动  童车 电动车 自行车 学步车 手推车 三轮车 滑板车 扭扭车 儿童轮滑  早教启蒙 早教机 点读机 健身架 布书 串/绕珠 床/摇铃 爬行垫 木质拼图
护肤彩妆
美容护肤 卸妆 面膜 洁面 防晒 面霜 爽肤水 眼霜 乳液  换季保养 补水 美白 收缩毛孔 控油 祛痘 祛斑 去黑眼圈 去黑头  超值彩妆 BB霜 粉底液 唇膏 隔离 遮瑕 指甲油 粉饼 彩妆套装  香氛精油 女士香水 男士香水 中性香水 淡香水 古龙水 香精 复方精油 香体乳  美发造型 洗发水 护发素 染发 烫发 造型 假发 洗护套装 假发配件  纤体塑身 美胸 纤体 胸部护理 身体护理 塑身 脱毛 手部保养 足部护理  眼部彩妆 眼线 睫毛膏 眼影 眉笔 假睫毛 眼霜 双眼皮贴 眼部护理  男士护理 劲能醒肤 清洁面膜 男性主义 剃须膏 男士套装 男士防晒 火山岩 爽身走珠  海外直邮 抗皱 抗敏感 保湿 去眼袋 滋润 抗氧化 深层清洁  热门品牌 雅诗兰黛 兰蔻 资生堂 自然乐园 SK-II 悦诗风吟 水宝宝 契尔氏  新品推荐 芦荟胶 彩妆盘 腮红 香氛 高光棒 修容 V脸 去角质  口碑大赏 洁面 爽肤水 精华 乳液 鼻贴 马油
汇吃美食
休闲零食 牛肉干 鲜花饼 红枣 糖果 巧克力 山核桃 松子 卤味 饼干 话梅 蔓越莓 薯片  生鲜果蔬 奇异果 芒果 樱桃 橙子 秋葵 苹果 番茄 柠檬 椰子 榴莲  粮油调味 大米 橄榄油 小米 黄豆 赤豆 火腿 香肠 木耳 香菇 豆瓣酱  水产鲜肉 海参 龙虾 瑶柱 土鸡 牛排 三文鱼 咸鸭蛋 皮蛋 五花肉 北极贝  美酒佳酿 鸡尾酒 红酒 啤酒 白酒 梅酒 洋酒 清酒 滋补酒 茅台 五粮液  牛奶饮料 麦片 咖啡 牛奶 柚子茶 酸梅汤 矿泉水 酵素 藕粉 姜茶 酸奶粉  四季茗茶 铁观音 红茶 花草茶 龙井 普洱 黑茶 碧螺春 毛峰 袋泡茶 白茶  滋补养生 枸杞 人参 石斛 燕窝 雪蛤 蜂蜜 天麻 花粉 党参 红花  全球美食 芒果干 鱼子酱 咖啡 橄榄油 薯片 巧克力 咖喱 方便面 红酒 麦片
珠宝配饰
时尚饰品 项链 手链 戒指 发饰 银饰 水晶 耳饰 手镯  珠宝首饰 翡翠 彩宝 蜜蜡 裸钻 珍珠 黄金 钻石 金条  最热单品 和田玉 翡翠 水晶/佛珠 黄金 手表 眼镜  品质手表 瑞士表 机械表 时装表 儿童表 电子表 情侣表 石英表 手表配件  潮流眼镜 太阳镜 偏光镜 近视镜 司机镜 护目镜 眼镜配件 运动镜 老花镜  绅士配件 zippo 电子烟 烟斗 瑞士军刀 绝美酒具 风格男表  手链 佛珠 水晶 碧玺 925银 施华洛 翡翠 珍珠 黄金  项链吊坠 银项链 流行风格 天然水晶 锆石水晶 佛珠项链 人造水晶  手镯 925银 翡翠 和田玉 复古泰银 粉晶手镯 黄金手镯  发饰 日韩 甜美 复古/宫廷 欧美 瑞丽 波西米亚 民族风  新娘配饰 发饰 项链 套装 耳饰 韩式 头饰 三件套  DIY饰品 合金配件 银饰 水晶配珠 琉璃 珍珠母贝 有机玻璃 人造水晶
家装建材
装修设计 设计师 半包装修 全包装修 全案装修 装修监理 清包施工 局部装修 验房量房 装修空气质量检测 装修污染治理  全屋定制 整体橱柜 定制衣柜 定制吊顶 定制淋浴房 门 窗 定制柜 楼梯 榻榻米定制 地暖  灯具灯饰 吸顶灯 吊灯 吸吊两用灯 筒灯 射灯 台灯 落地灯 室外灯 壁灯 小夜灯  卫浴用品 浴室柜 普通马桶 花洒套装 一体智能马桶 智能马桶盖板 淋浴房 面盆龙头 地漏 五金挂件 浴霸  墙纸 PVC墙纸 无纺布墙纸 纯纸墙纸 墙布 沙粒墙纸 绒面墙纸 定制壁画 3D墙纸  地板 实木地板 实木复合地板 强化复合地板 竹地板 户外地板 PVC地板 防静电地板 防潮膜 踢脚线 地板龙骨  瓷砖 仿古砖 釉面砖 玻化砖 微晶石 马赛克 抛晶砖 通体砖 花片 腰线 瓷砖背景墙  电子电工 插座 开关 电线 监控器材 智能家居 防盗报警器材 消防报警设备 接线板插头 布线箱 断路器  基础建材 涂料乳胶漆 油漆 水管 板材 木方 阳光房 线条 天然大理石 人造大理石 防水涂料
家居家纺
卧室家具 实木床 布艺床 皮艺床 床垫 衣柜 斗柜 梳妆台 子母床 床头柜 儿童床  客厅家具 皮艺沙发 布艺沙发 沙发床 实木沙发 懒人沙发 电视柜 茶几 鞋柜 玄关厅 衣帽架  餐厅家具 餐桌 折叠餐桌 欧式餐桌 实木餐桌 大理石餐桌 餐椅 餐边柜 换鞋凳 角柜 屏风  书房家具 餐桌 折叠餐桌 欧式餐桌 实木餐桌 大理石餐桌 餐椅 餐边柜 换鞋凳 角柜 屏风  夏凉床品 蚊帐 三开蚊帐 凉席 凉席套件 冰丝席 藤席 牛皮席 夏凉被 空调被 天丝套件 床单 床笠  全季床品 四件套 全棉套件 被套 蚕丝被 羽绒被 枕头 乳胶枕 记忆枕 床褥 毛毯  居家布艺 定制窗帘 地毯 沙发垫 靠垫 桌布桌旗 飘窗垫 地垫 餐垫 防尘罩 椅垫 成品窗帘 沙发罩  家居摆件 摆件 花瓶 仿真花 台钟闹钟 香薰炉 储物罐 装饰碗盘 木雕 烟灰缸 纸巾盒 蜡烛烛台 仿真饰品  墙饰壁饰 现代装饰画 无框画 后现代画 油画 挂钟 照片墙 新中式 北欧家饰 美式乡村 挂钩搁板 装饰挂钩 壁饰
百货市场
居家日用 扇子 毛巾 浴巾 口罩 隔音耳塞 竹炭包 眼罩 夏季凉拖 居家鞋 夏季清凉  应季百货 湿巾 晴雨伞 驱蚊灯 驱蚊液 冰格 保鲜产品 密封罐 防潮制品 电扇/冰垫 5元小物  收纳整理 被子防尘袋 收纳盒 收纳袋 大衣/西服罩 护洗袋 收纳凳 鞋柜 置物架 桌用收纳 内衣收纳  个人清洁 洗发护发 沐浴露 漱口水 卫生巾 洗手液 牙膏 纸巾 香皂 沐浴球/浴擦/浴刷 指甲刀  清洁工具 剃须刮毛刀 沐浴球 浴室角架 浴帘杆 拖把 垃圾桶 梳子镜子 围裙 百洁布 海绵擦  厨房工具 餐具 锅具 刀具 炖锅 蒸锅 汤锅 煎锅 压力锅 炒锅 菜板砧板  盆碗碟筷 一次性餐桌用品 酒杯酒具 咖啡器具 碗盘碟 刀叉勺 餐具瓷器套装 餐桌小物 饭盒 厨房储物 一次性餐桌用品  茶具杯具 茶具 茶壶 飘逸杯 功夫茶杯 玻璃杯 杯垫 保温杯 马克杯 保温壶 情侣杯  家用杂物 晒衣篮 晾衣杆 脏衣篮 衣架 家庭清洁剂 蓝泡泡 管道疏通器 塑胶手套 医药箱 垃圾袋
汽车·用品
热门新车 汽车首页 新车先购 车海淘 二手车 爱车估价 suv 别克 大众 宝马  品质内饰 座垫 座套 脚垫 香水 旅行床 遮阳挡 挂件摆件 安全座椅 专车专用座垫 脚垫 安全座椅 香水 钥匙包 挂件 座套 后备箱垫 置物箱  汽车导航 智能车机 后视镜 安卓导航 便携GPS DVD导航 电子狗 流动测速 导航软件 记录仪 预警仪 GPS 车机 倒车雷达 智能后视镜 蓝牙 防盗器 MP3  汽车服务 4S保养 电瓶安装 配件安装 隔热膜 洗车卡 镀晶镀膜 连锁保养 上门服务  影音电子 行车记录仪 逆变器 跟踪器 充电器 充气泵 胎压监测 车载冰箱 空气净化 车衣 SUV踏板 晴雨挡 改色膜 汽车车标 车牌架  汽车配件 轮胎 雨刮器 机油滤芯 空气滤芯 空调滤芯 减震 刹车片 火花塞 轮胎 雨刮 机油 高亮大灯 挡泥板 保险杠 车顶架 轮眉  改装达人 轮毂 排气 保险杠 汽车包围 氙气灯 车顶架 脚踏板 大灯总成 尾翼 轮毂 汽车装饰灯 排气筒 尾喉 车身饰条  美容清洗 添加剂 防冻液 玻璃水 车蜡 补漆笔 洗车机 洗车水枪 车掸蜡拖 车蜡 洗车机 补漆笔 抛光机 打蜡海绵 车用水桶 擦车巾 车刷  外饰装潢 装饰条 车贴 尾喉 改色膜 防爆膜 晴雨挡 日行灯 车衣 夏季座垫 遮阳挡 防眩蓝镜 防晒手套
手机数码
手机 iPhone 小米 华为 三星 魅族 纽扣 酷派 VIVO  平板 iPad 小米 三星 10寸 台电 win8 蓝魔 华为  电脑 DIY电脑 一体机 路由器 显示器 学生 CPU 移动硬盘 无线鼠标  笔记本 苹果 联想 Thinkpad 戴尔 华硕 Acer 神州 三星  相机 单反 自拍神器 拍立得 佳能 微单 镜头 卡西欧 尼康  3C配件 充电宝 智能穿戴 蓝牙耳机 iPhone6壳 电脑包 手机贴膜 手机壳套 三脚架  数码配件 保护壳套 炫彩贴膜 移动电源 相机配件 手机零件 自拍神器 移动POS支付 电池  智能设备 儿童手表 Apple Watch 智能手表 智能手环 智能配饰 智能健康 智能排插 智能眼镜  电玩 游戏掌机 家用游戏机 游戏手柄 PS主机 XBOX 任天堂配件 PS主机配件 XBOX配件  网络设备 路由器 网关 交换机 光纤设备 网络存储设备 无线上网卡 TP-LINK 小米路由器  MP3/MP4 MP3 MP4 录音笔 索尼 飞利浦 ipod 爱国者 耳机  存储 U盘 闪存卡 记忆棒 移动硬盘 希捷 三星 Sandisk 金士顿 
家电办公
厨房电器 电磁炉 电水壶 料理机 电饭煲 榨汁机 净水器 豆浆机 烤箱  生活电器 电风扇 空调扇 挂烫机 扫地机 吸尘器 加湿器 除湿机 对讲机 空气净化  个护电器 理发器 电子称 美容仪 按摩椅 按摩披肩 血压计 足浴器 电动牙刷 剃须刀  影音电器 耳机 音响 网络机顶盒 麦克风 扩音器 HiFi套装 蓝光DVD 低音炮  办公耗材 打印机 投影仪 硒鼓墨盒 A4纸 一体机 学生文具 保险柜 电纸书 学习机  大家电 冰箱 空调 平板电视 油烟机 燃气灶 消毒柜 厨电套装 热水器 洗衣机  包装用品 包装设备 包装纸箱 塑料袋 包装胶带 铭牌 快递袋 气泡膜 真空机  文化用品 笔记本 文件袋 钢笔 胶粘用品 铅笔 计算器 白板 台历  个性定制 设计定制 企业用品定制 T恤印制 杯子定制 ppt模板 班服定制 洗照片 人偶定制  五金工具 电子电工 气动元件 水泵 阀门 电钻 焊接设备 万用表 雕刻机  商用家具 办公家具 商业设施 办公桌 陈列柜 货架 广告牌 文件柜 沙发  电子元器件 网络设备 电子元器件 路由器 交换机 光纤设备 视频会议 无线安全保密 机柜
更多服务
生活团购 餐饮美食 冰淇淋 火锅 购物卡券 体检配镜 美容美甲 保险理财 婚纱摄影 旅行团购  买房租房 住在帝都 住在魔都 住在杭州 住在南京 住在广州 住在青岛 住在宁波 住在成都  儿童培养 少儿英语 小学教育 潜能开发 家长训练 孕产育儿 少儿绘画 婴幼早教 音乐  淘宝游戏 Q币充值 点卡充值 充游戏币 游戏代练 超值账号 手游充值 电竞比赛 游戏帮派  挑个好房 潇洒一室 靠谱二室 舒适三房 大四室 私藏别墅 景观居所 轨道沿线 学区房  成人教育 实用英语 网站制作 IT技能 会计职称 一对一 办公软件 日语 编程  游戏中心 英雄联盟 剑侠情缘3 征途2 魔域 我叫MT 刀塔传奇 DOTA2 DNF 魔兽世界  吃喝玩乐 自助餐 个性写真 儿童写真 电影票团购 上门服务 周边旅游 境外旅游 基金理财  生活兴趣 魅力健身 时尚美妆 手工DIY 舞蹈 减肥瑜伽 个人形象 美剧英语 摄影 美女陪练 轻松甩肉 基金理财 淘宝美工 办公技能
生活服务
婚庆服务 婚纱摄影 婚礼策划 三亚婚拍 厦门婚拍 青岛婚拍 北京婚拍 杭州婚拍 上海婚拍 新娘跟妆 婚礼跟拍 婚礼司仪 婚车租赁  在线清洗 任意洗 洗外套 洗西装 洗鞋 洗四件套 洗烫衬衫 皮包护理 洗窗帘 洗地毯 在线洗衣 洗礼服 洗玩具  家庭保洁 开荒保洁 厨房保洁 公司保洁 家电清洗 空调清洗 洗油烟机 冰箱清洗 擦玻璃 家政服务 家庭保洁 保洁服务 钟点工 洗衣机清洗 卫生间保洁  汽车服务 上门养车 洗车 封釉镀膜 内饰清洗 空调清洗 汽车维修 充加油卡 年检代办 玻璃贴膜 汽车装饰 底盘装甲 四轮定位 汽车改装 违章代办 汽车隔音  健康服务 上门按摩 常规体检 入职体检 老人体检 四维彩超 孕前检查 体检报告 专业洗牙 烤瓷牙 胃部检测  母婴服务 月嫂 催乳师 育儿嫂 营养师 普通保姆 涉外保姆 产后陪护 临时看护 管家 烧饭阿姨  宠物服务 宠物寄养 宠物美容 宠物配种 宠物洗澡 宠物摄影 宠物托运 宠物训练 宠物医疗 水族服务 宠物绝育 宠物洗牙 宠物造型 宠物体检  家政服务 居家搬家 公司搬运 空调拆装 家电搬运 家具搬运 打孔 电路维修 甲醛测试 开锁换锁 杀虫消毒 高空清洁 除尘除螨  便民服务 跑腿服务 代缴费 叫醒服务 宝宝起名 学车报名 代邮代取 代送鲜花 同城速递 代办档案 机场停车  商务服务 专利申请 法律咨询 专业翻译 开发建站 图片处理 视频制作 名片制作 商标转让 打印 复印 商标注册 私人律师 合同文书 出国翻译  数码维修 手机维修 pad维修 修台式机 相机维修 修笔记本 修复印机 修游戏机 修导航仪 软件服务 延保服务 硬件维修 苹果维修 小米维修 三星维修 安卓刷机 数据恢复 电脑维修 ipad维修 华为维修 重装系统 家电维修 相机维修 硬盘维修 苹果换屏 换主板  招聘服务 名企招聘 高薪岗位 文案编辑 网店推广 开发技术 活动策划 美工设计 金牌客服 大促客服 网页设计 人才认证 图片设计 摄影师 店长 运营主管 客服主管 美工主管
运动户外
运动潮鞋 跑步鞋 篮球鞋 休闲鞋 足球鞋 帆布鞋 训练鞋 徒步鞋 登山鞋 限量版 板鞋 Rosherun  运动服 运动套装 运动卫衣 长裤 皮肤风衣 健身服 球服 耐克 阿迪达斯 三叶草 美津浓 彪马 狼爪  骑行装备 山地车 公路车 骑行服 头盔 装备 零件 工具 护具 折叠车 死飞 水壶架 行李架  球类运动 羽毛球拍 羽毛球服 羽毛球 网球拍 篮球 篮球服 足球 足球服 乒乓球拍 橄榄球 台球 高尔夫  户外野营 吊床 头灯 遮阳棚 望远镜 照明 野营帐篷 野外照明 烧烤炉 望远镜 潜水镜 防潮垫 皮划艇  户外穿戴 皮肤衣 防晒衣 冲锋衣 探路者 速干裤 迷彩服 战术靴 登山鞋 crocs 溯溪鞋 户外鞋  民间运动 麻将机 轮滑 麻将 象棋 雀友 飞镖 桌上足球 风筝 陀螺 空竹 沙袋 太极服  健身运动 甩脂机 轮滑装备 跑步机 舞蹈 瑜伽 哑铃 仰卧板 踏步机 划船机 卧推器 健身车 呼啦圈  瑜伽舞蹈 舞蹈 瑜伽 广场舞 舞蹈鞋 拉丁鞋 广场舞套装 肚皮舞服装 瑜伽垫 瑜伽球 瑜伽服  垂钓用品 鱼饵 套装 路亚 附件 鱼钩 钓鱼工具 船/艇 台钓竿 海钓竿 溪流竿 路亚竿 矶钓杆  运动包 单肩背包 旅行包 双肩背包 挎包 户外摄影包 头巾 运动水壶 防水包  电动车 电池 电自行车 平衡车 滑板车 头盔 摩托车 老年代步 独轮车 遮阳伞 扭扭车 折叠车
花鸟文娱
鲜花速递 仿真植物 干花 DIY花 手捧花 鲜果蓝 仿真蔬果 开业花篮 花瓶  花卉绿植 绿植同城 园艺方案 多肉植物 桌面盆栽 蔬菜种子 水培花卉 苔藓景观 空气凤梨  园艺用品 肥料 花盆花器 花卉药剂 营养土 园艺工具 洒水壶 花架 铺面石  观赏鱼 热带鱼 孔雀鱼 底栖鱼 虾螺 龙鱼 罗汉鱼 锦鲤 金鱼 水母 灯科鱼 乌龟  造景设备 水草 底砂 水草泥 沉木 仿真水草 假山 氧气泵 过滤器 水草灯 加热棒 鱼粮 水质维护 硝化细菌 除藻剂 龟粮  奇趣小宠 兔兔 仓鼠 龙猫 雪貂 粮食零食 医疗保健 笼子 鹦鹉 鸟笼 观赏鸟 蚂蚁工坊 蜘蛛 蚕  萌狗世界 大牌狗粮 宠物服饰 狗厕所 宠物窝 航空箱 海藻粉 羊奶粉 宠物笼 储粮桶 剃毛器 营养膏 上门服务  乐器音乐 吉他 钢琴 数码钢琴 古筝 电子琴 萨克斯风 古琴 二胡 小提琴 音箱  模玩手办 高达 手办 盒蛋 兵人 变形金刚 圣衣神话 钢铁侠 BJD 拼装 人偶  猫咪世界 猫砂 猫粮 猫爬架 猫窝 猫砂盆 化毛膏 猫罐头 喂食器 折耳猫 猫抓板 猫玩具 猫笼  乐器配件 拾音器 乐器培训 合成器 乐器包 MIDI键盘 乐器定制 扬琴 贝司 葫芦丝 尤克里里 调音台 监听耳机  动漫周边 动漫T恤 动漫抱枕 COS 背包 项链 颜文字 哆啦A梦 大白 手表 盗墓笔记 海贼 火影 LOL
农资采购
农药 杀菌剂 杀虫剂 除草剂 调节剂 杀螨剂 杀鼠剂 敌敌畏 草甘膦  种子种苗 园林种苗 动物种苗 蔬菜种苗 水果种苗 粮油种子 药材种苗 食用菌种 辣木籽  肥料 氮肥 磷肥 钾肥 叶面肥 新型肥料 复合肥 生物肥料 有机肥  农业机械 耕种机械 收割机械 农机配件 植保机械 拖拉机 施肥机械 粮油设备 微耕机  农膜 塑料薄膜 大棚膜 防渗膜 鱼塘专用 薄膜 遮阳网 篷布 防虫网  农业工具 镰刀 锹 高压水枪 锨 镐 耙子 锄头 叉  饲料 猪饲料 羊饲料 牛饲料 预混料 饲料原料 全价料 饲料添加剂 浓缩料  畜牧养殖 加工设备 养殖器械 渔业用具 养殖服务 配种服务 养鸡设备 挤奶机 母猪产床  兽药 化学药 中兽药 抗生素 驱虫 消毒剂 疫苗 阿莫西林 氟苯尼考
"""


task_keys = []
for i in txt.split(" "):
    if i != "":
        #print(i)
        task_keys.append(i)

#print(task_keys)




import caifen


ppfl_keys2 = caifen.ppfldatas()
print(ppfl_keys2)








def run(keys,csv_data_file):
    n=0
    while n<11:

        jdurl = "https://search-x.jd.com/Search?area=22&enc=utf-8&keyword="+keys+"&page="+str(n)+"&ad_ids=291%3A33"
        print(jdurl)
        html_info = get_html(jdurl)
        #print(html_info)
        get_jd_data_2(keys,csv_data_file,html_info)
        n+=1


csv_data_file = 'D:/PPFL_JD_5_30.csv'


for key_datas in ppfl_keys2:
    print(key_datas)
    run(key_datas,csv_data_file)


