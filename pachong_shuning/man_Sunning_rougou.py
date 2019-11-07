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


'''

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
    n=0
    while n<len(PID_test_number):
        ps[n].start()
        n+=1
 
    # 阻塞进程
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

'''


#苏宁热收   接口   

#http://th.suning.com/cpc/getSingleAppCpcHotSaleSearch?keyword=%E7%94%B5%E8%A7%86&page_index=3000&page_size=10&fromhot=&terminal=wap&source=default&utm_source=default

#http://th.suning.com/cpc/getSingleAppCpcHotSaleSearch?keyword=%E7%94%B5%E8%A7%86&page_index=0&page_size=1000



test1_unrg = "http://th.suning.com/cpc/getSingleAppCpcHotSaleSearch?keyword=电视&page_index=0&page_size=1000"
html_info_unrg = get_html(test1_unrg)
#print(html_info_unrg)

#"result":{
#"goodsList":

#实价    netPrice
def get_resultlist(html):
    reg = r"\{\"clickUrl\":.*?\}"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data

#print(get_resultlist(html_info_unrg))


#获取商品链接地址
def get_urlinfo(html):
    reg = r"\"clickUrl\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data

#获取商品名称
def get_title(html):
    reg = r"\"title\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data

#获取商品价格  goodsPriceTxt
def get_goodsPriceTxt(html):
    reg = r"\"goodsPriceTxt\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data


#获取商品图片 adSrc
def get_adSrc(html):
    reg = r"\"adSrc\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data



def get_sopurl_id(html):
    reg = r"id=\"chead_indexUrl\" href=\"(.*?)\" title"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data


#总评论数  totalCount
#获取商品图片 adSrc
def get_totalCount(html):
    reg = r"\"totalCount\":(.*?),"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data


'''
top_url = get_urlinfo(html_info_unrg)[0]
top_url = top_url.replace("\\","")
print(top_url)
print("**********************************\n\n\n")
'''


def sn_rougou_run(keys,html_info_unrg,csv_data_file):
    for listdata in get_resultlist(html_info_unrg):
        print(listdata)
        
        #print(get_urlinfo(listdata)[0])
        urls = get_urlinfo(listdata)[0]
        
        print("--***  商品url  ***--")
        urls = urls.replace("\\","")
        #print(urls.split(":")[0])
        if urls.split(":")[0] == "http" or urls.split(":")[0] == "https":
            sp_link = urls
        else:
            sp_link = "http:"+urls
        print(sp_link)
        urls_data = sp_link

        #商品名称
        print("--***  商品名称  ***--")
        #print(get_title(listdata))
        if get_title(listdata) !=[]:
            name = get_title(listdata)[0]
        else:
            name = "isNull"
        print(name)

        print(get_goodsPriceTxt(listdata))
        images = get_adSrc(listdata)
        if images != []:
            images = images[0]
            images = images.replace("\\","")
        else:
            images = "isNull"

        
        print(urls.split("/"))
        html_infosadasd = get_html(sp_link)
        print(get_sopurl_id(html_infosadasd))
        if get_sopurl_id(html_infosadasd) != []:
            aaainfoaa = get_sopurl_id(html_infosadasd)[0]
            print(aaainfoaa)
            sp_id1=aaainfoaa.split("/")[-2]
        else:
            sp_id1 = "0"

        id1=urls.split("/")[-2]
        print("id1 = "+id1)
        id2=urls.split("/")[-1]
        id2=id2.split(".")[0]
        print("id1 = "+id1)
        print("id2 = "+id2)
        if len(id2) != 11:
            id2 = "00"+id2
        url_shop = "https://shop.suning.com/jsonp/"+sp_id1+"/shopinfo/shopinfo.html"
        url_price = "http://pas.suning.com/nspcsale_1_0000000"+id2+"_0000000"+id2+"_"+id1+"_230_028_0280101_361003_1000268_9265_12132_Z001___R9001185_0.2_1___0001527D4__.html"
        print(url_shop)
        print(url_price)

        print("--***  商品销量/评价  ***--")
        asdsa = "http://review.suning.com/ajax/cluster_review_satisfy/cluster-0-0000000"+id2+"-"+id1+"-----satisfy.htm"
        htmlasdsa = get_html(asdsa)
        print(get_totalCount(htmlasdsa))

        if get_totalCount(htmlasdsa) != []:

            pingjia = get_totalCount(htmlasdsa)[0]
        else:
            pingjia = "isNull"

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


        print(images)
        print("\n\n\n")
        image = images

        # 商品名称，商品链接，实际价格，活动价格，图片，评价，店家名称，店家电话，店家主页，店家服务评分，店家物流评分，店家商品评分，店家位置
        input_datas = [keys,name,urls_data,net_price,promotion_price,image,pingjia,shop_name,phone_num,shop_domain,astar_data,dstar_data,star_data,company_address]
        #print('D:/py_test/yibiao_Auto/report/xyzg_data/tb_test1.csv')

        #input_datas = [cod_name1,cod_name2]
        with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
            csv_write = csv.writer(f,dialect='excel')
            csv_write.writerow(input_datas)


def run(keys,csv_data_file):
    a=False
    number = 0
    olad_url = ""
    while a == False:
        test1_unrg = "http://th.suning.com/cpc/getSingleAppCpcHotSaleSearch?keyword="+keys+"&page_index="+str(number)+"&page_size=1000"
        print("--------- **  "+ test1_unrg +"  ** ----------")
        html_info_unrg = get_html(test1_unrg)
        if get_urlinfo(html_info_unrg) != []:

            top_url = get_urlinfo(html_info_unrg)[0]
            top_url = top_url.replace("\\","")
            print(top_url)
        else:
            top_url = olad_url
        print("**********************************\n\n\n")
        if olad_url == top_url:
            a= True

        sn_rougou_run(keys,html_info_unrg,csv_data_file)

        number+=1
        olad_url = top_url
        top_url = ""
        


#sn_rougou_run("电视",html_info_unrg,csv_data_file)






def go_run(fl_list,csv_data_file):
    for fl in fl_list:
        run(fl,csv_data_file)
        print(fl)

fllist_1 = ["T恤","长袖T恤","卫衣","开衫","女装","男装","袜子","短袜","丝袜","婚纱","伴娘服","下装","裤子","裙子","连衣裙","旗袍","蛋糕群"]
fllist_2 = ["运动鞋","篮球鞋","板鞋","皮鞋","高跟鞋","网球鞋","帆布鞋","凉鞋","拖鞋","手机","iphone","华为","小米","oppo","vivo"]
fllist_3 = ["魅族","一加","荣耀","联想","充电宝","电视","冰箱","冰柜","风扇","油烟机","按摩椅","皮带","手套","手表","粉底","口红"]
fllist_4 = ["唇彩","香水","洗面奶","护肤霜","乳液","发蜡","剃须刀","电脑","照相机","投影仪","打印机","猪肉脯","内裤","女士内裤",
        "男士内裤","睡衣","情趣内衣"]


csv_data_file = 'D:/SN_datas_RG_1.csv'


go_run(fllist_1,csv_data_file)

#秒杀并发测试程序

'''
#Get网页，返回内容
def post_html( url_path, datas='', payload = '', cookies = '',proxies = ''):
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




def get_md5(html):
    reg = r"\"md5\":\"(.*?)\","
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data

userphone = {"userPhone":"18412341221"}

sp_list = []
sp="184143"
nnn=0
while nnn<1000:
    if len(str(nnn))<=5:
        spnum=sp+"0"*(5-len(str(nnn)))+str(nnn)
        #print(spnum)
        sp_list.append(spnum)
    nnn+=1

#print(sp_list)



def run(sp_list):
    userphone_data = {"userPhone":sp_list}
    print(userphone_data)
    a = get_html( "http://192.168.2.109:8080/seckill/1003/exposer", payload = '', cookies = userphone_data,proxies = '')
    md5num = get_md5(a)[0]
    p = post_html("http://192.168.2.109:8080/seckill/1003/"+md5num+"/execution", datas='', payload = '', cookies = userphone_data,proxies = '')
    print(p)



#run(sp_list)



import threading



lock=threading.Lock()

for k in sp_list:

    new_thread = threading.Thread(target=run,args=(k,))
    new_thread.start()
'''