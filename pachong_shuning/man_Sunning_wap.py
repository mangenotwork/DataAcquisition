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




test1 = "https://search.suning.com/emall/searchV1Product.do?keyword=衣服&pg=01&cp=01&adNumber=5&n=1"
html_info = get_html(test1)
#print(html_info)
'''
////*[@id="0070209396-10499060737"]

'''

def get_li(html):
    reg = r"<li.*?<\/li>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data

def get_name(html):
    
    reg = r"<img alt=\"(.*?)\""
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data

def get_urls(html):
    reg = r"href=\"(.*?)\""
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data

def get_image(html):
    reg = r"src=\"(.*?)\""
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data

def get_a(html):
    reg = r"<a.*?>(.*?)<\/a>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data

def get_pingjia(html):
    reg = r"<i>(.*?)<\/i>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data





#"companyName":"   公司名称
def get_shopName(html):
    reg = r"\"shopName\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data


#店家电话
def get_phoneNUM(html):
    reg = r"\"telPhone\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data



#店家首页
def get_shopDomain(html):
    reg = r"\"shopDomain\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data



#服务评分  Astar
def get_Astar(html):
    reg = r"\"Astar\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data



#物流评分  Dstar
def get_Dstar(html):
    reg = r"\"Dstar\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data



#商品评分  star
def get_star(html):
    reg = r"\"star\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data



#店家位置  companyAddress
def get_companyAddress(html):
    reg = r"\"companyAddress\":\"(.*?)\""
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data



#促销价   promotionPrice
def get_promotionPrice(html):
    reg = r"\"promotionPrice\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data



#实价    netPrice
def get_netPrice(html):
    reg = r"\"netPrice\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data





#print(get_li(html_info))
def get_datas(keys,html_info,csv_data_file):
    for li in get_li(html_info):
        #print(li)
        

        print("--***  商品名称  ***--")
        name = get_name(li)[0]
        print(name)

        print("--***  商品url  ***--")
        urls_data = get_urls(li)[0]
        print(urls_data)
        print(urls_data.split("/"))
        id1=urls_data.split("/")[-2]
        id2=urls_data.split("/")[-1]
        id2=id2.split(".")[0]
        print("id1 = "+id1)
        print("id2 = "+id2)
        if len(id2) != 11:
            id2 = "00"+id2
        url_shop = "https://shop.suning.com/jsonp/"+id1[2:]+"/shopinfo/shopinfo.html"
        url_price = "http://pas.suning.com/nspcsale_1_0000000"+id2+"_0000000"+id2+"_"+id1+"_230_028_0280101_361003_1000268_9265_12132_Z001___R9001185_0.2_1___0001527D4__.html"
        print(url_shop)
        print(url_price)
        shop_data = get_html(url_shop)
        price_data = get_html(url_price)
        print("--***  店家名称  ***--")
        shop_name = get_shopName(shop_data)
        if shop_name != []:
            shop_name = shop_name[0]
        else:
            shop_name = "isNull"
        print(shop_name)

        print("--***  店家电话  ***--")
        phone_num = get_phoneNUM(shop_data)
        if phone_num != []:
            phone_num = phone_num[0]
        else:
            phone_num = "isNull"
        print(phone_num)
        #print(get_phoneNUM(shop_data))

        print("--***  店家主页  ***--")
        #print(get_shopDomain(shop_data))
        shop_domain = get_shopDomain(shop_data)
        if shop_domain != []:
            shop_domain = shop_domain[0]
        else:
            shop_domain = "isNull"
        print(shop_domain)

        print("--***  店家评分  ***--")
        #print(get_Astar(shop_data))#服务评分
        #print(get_Dstar(shop_data))#物流评分
        #print(get_star(shop_data))#商品评分
        astar_data = get_Astar(shop_data)
        dstar_data = get_Dstar(shop_data)
        star_data = get_star(shop_data)

        if astar_data != []:
            astar_data = astar_data[0]
        else:
            astar_data = "isNull"
        print(astar_data)

        if dstar_data != []:
            dstar_data = dstar_data[0]
        else:
            dstar_data = "isNull"
        print(dstar_data)


        if star_data != []:
            star_data = star_data[0]
        else:
            star_data = "isNull"
        print(star_data)


        print("--***  店家位置  ***--")
        #print(get_companyAddress(shop_data))
        company_address = get_companyAddress(shop_data)
        if company_address != []:
            company_address = company_address[0]
        else:
            company_address = "isNull"
        print(company_address)

        #print(url_price)
        print("--***  商品实际价格  ***--")
        #print(get_netPrice(price_data)[0])
        net_price = get_netPrice(price_data)
        if net_price != []:
            net_price = net_price[0]
        else:
            net_price = "isNull"
        print(net_price)

        print("--***  商品活动价格  ***--")
        #print(get_promotionPrice(price_data)[0])
        promotion_price = get_promotionPrice(price_data)
        if promotion_price != []:
            promotion_price = promotion_price[0]
        else:
            promotion_price = "isNull"
        print(promotion_price)

        print("--***  商品首张图片  ***--")
        #print(get_image(li)[0])
        image = get_image(li)
        if image != []:
            image = image[0]
        else:
            image = "isNull"
        print(image)
        

        print("--***  商品评价  ***--")
        #print(get_pingjia(li)[-4])
        pingjia = get_pingjia(li)
        if pingjia != []:
            pingjia = pingjia[0]
        else:
            pingjia = "isNull"
        print(pingjia)

        print("\n\n")
        # 商品名称，商品链接，实际价格，活动价格，图片，评价，店家名称，店家电话，店家主页，店家服务评分，店家物流评分，店家商品评分，店家位置
        input_datas = [keys,name,urls_data,net_price,promotion_price,image,pingjia,shop_name,phone_num,shop_domain,astar_data,dstar_data,star_data,company_address]
        #print('D:/py_test/yibiao_Auto/report/xyzg_data/tb_test1.csv')

        #input_datas = [cod_name1,cod_name2]
        with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
            csv_write = csv.writer(f,dialect='excel')
            csv_write.writerow(input_datas)


#get_datas(html_info)
csv_data_file = 'D:/SN_datas_yifu_3.csv'
keys="衣服"



def run(keys,csv_data_file):
    n=0
    while n<51:
        if n<10:
            cp_n = "0"+str(n)
            
        else:
            cp_n = str(n)

        print(cp_n)
        test1 = "https://search.suning.com/emall/searchV1Product.do?keyword="+keys+"&pg=01&cp="+cp_n+"&adNumber=5&n=1"
        print(test1)
        html_info = get_html(test1)
        get_datas(keys,html_info,csv_data_file)
        n+=1


#run(keys,csv_data_file)




def main():
    print("主进程执行中>>> pid={0}".format(os.getpid()))
    #logger.info("主进程执行中>>> pid={0}".format(os.getpid()))
    PID_test_number = [["T恤","D:/SN_datas_Txie_1.csv"],
                        ["长袖T恤","D:/SN_datas_CXTxie_1.csv"],
                        ["卫衣","D:/SN_datas_weiyi_1.csv"],
                        ["开衫","D:/SN_datas_kaisan_1.csv"],
                        ["女装","D:/SN_datas_nvzhuang_1.csv"],
                        ["男装","D:/SN_datas_nanzhuang_1.csv"]
                        ]
                    

    ps=[]
    # 创建子进程实例
    for i in PID_test_number:
        p=Process(target=run,name="run"+str(i),args=(i[0],i[1],))
        ps.append(p)
 
    # 开启进程
    '''
    for i in PID_test_number:
        ps[i].start()
    '''
    n=0
    while n<len(PID_test_number):
        ps[n].start()
        n+=1
 
    # 阻塞进程
    '''
    for i in PID_test_number:
        ps[i].join()
    '''
    j=0
    while j<len(PID_test_number):
        ps[j].join()
        j+=1


    print("主进程终止")
    #logger.info("[End] ** 主进程终止 **")
 
if __name__ == '__main__':
    main()
    #a=0
    #case_init(["man_test_001","man_test_002"],a)