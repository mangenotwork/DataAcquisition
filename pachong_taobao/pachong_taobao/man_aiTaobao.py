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


test_url = 'http://docs.python-requests.org/zh_CN/latest/user/quickstart.html'
ip_test_url = 'https://www.xicidaili.com/nn/'
#html_data = get_html(ip_test_url,'content')
#print html_data.encode("GBK",'ignore')

#print get_html(ip_test_url,proxies)
#get_html(ip_test_url,proxies)



#使用re模块集成的过滤类
class Filter_RE:
	pass



#使用Xpath的过滤类
class Filter_Xpath:
	pass

'''
html_info = get_html("https://ai.taobao.com/")


f = open('C:/Users/Administrator/Desktop/tao.html', 'w', encoding='utf-8')
f.write(html_info)
f.close()
'''

test1 = "https://ai.taobao.com/search/index.htm?source_id=search&key=丝袜"
html_info = get_html(test1)
#print(html_info)
'''
print(html_info)
f = open('C:/Users/Administrator/Desktop/tao1.html', 'w', encoding='utf-8')
f.write(html_info)
f.close()

'''

def gethref(html):
    reg = r"<\s*script[^>]*>[^<]*<\s*/\s*script\s*>"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data


def gethref1(html):
    reg = r"\"p4ptop\":.*?</script>"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data


#print(gethref(html_info))

#new_html_1 = str(gethref(html_info))

#print(gethref1(new_html_1))

#new_html_2 = str(gethref1(new_html_1))

#获取头
#"title":
def get_title(html):
    reg = r"\"title\":.*?,"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#print(get_title(new_html_2))


def get_description(html):
    reg = r"\"description\":.*?,"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data




#print(get_link(new_html_2))



def fenduan(html):
    
    return html.split("},")
'''
for datas in fenduan(new_html_2):
    #print(datas)
    
    print(get_title(datas))
    print(get_description(datas))
    #hrs = get_link(datas)
    #print(hrs)

    links = hrs.replace("&amp;", "&")
    print(links)
    lins_url = get_now_Location(str(links))
    print(lins_url)
'''

'''
for links in get_link(new_html_2):
    #print(links.replace("&amp;", "&"))
    hrs = links.replace("&amp;", "&")
    #print(hrs)
    #print(get_now_Location(str(hrs)))
    lins_url = get_now_Location(str(hrs))
    print(lins_url)
'''


'''
f = open('C:/Users/Administrator/Desktop/tao2.txt', 'w', encoding='utf-8')
f.write(str(gethref1(new_html_1)))
f.close()
'''



'''
接口一    


'''





#接口 2  https://ai.taobao.com/search/getItem.htm?page=3&sourceId=search&key=T恤

#print(get_html("https://ai.taobao.com/search/getItem.htm?page=3&sourceId=search&key=T恤"))


'''
2  https://ai.taobao.com/search/getItem.htm?_tb_token_=eb78eefee007e&__ajax__=1&pid=mm_10011550_0_0&unid=&clk1=&page=4&pageSize=60&pvid=200_11.15.192.192_17308_1557243744053&squareFlag=&sourceId=search&ppathName=&supportCod=&city=&ppath=&dc12=&pageNav=false&itemAssurance=&fcatName=&price=&cat=&from=&tmall=&key=%E4%B8%9D%E8%A2%9C&fcat=&ppage=0&debug=false&sort=&exchange7=&custAssurance=&postFree=&npx=50&location=&personalizeSwitch=
4  https://ai.taobao.com/search/getItem.htm?_tb_token_=eb78eefee007e&__ajax__=1&pid=mm_10011550_0_0&unid=&clk1=&page=2&pageSize=60&pvid=200_11.15.192.192_17308_1557243744053&squareFlag=&sourceId=search&ppathName=&supportCod=&city=&ppath=&dc12=&pageNav=false&itemAssurance=&fcatName=&price=&cat=&from=&tmall=&key=%E4%B8%9D%E8%A2%9C&fcat=&ppage=0&debug=false&sort=&exchange7=&custAssurance=&postFree=&npx=50&location=&personalizeSwitch=
3  https://ai.taobao.com/search/getItem.htm?_tb_token_=eb78eefee007e&__ajax__=1&pid=mm_10011550_0_0&unid=&clk1=&page=3&pageSize=60&pvid=200_11.15.192.192_17308_1557243744053&squareFlag=&sourceId=search&ppathName=&supportCod=&city=&ppath=&dc12=&pageNav=false&itemAssurance=&fcatName=&price=&cat=&from=&tmall=&key=%E4%B8%9D%E8%A2%9C&fcat=&debug=false&sort=&exchange7=&custAssurance=&postFree=&npx=50&location=&personalizeSwitch=
5  https://ai.taobao.com/search/getItem.htm?_tb_token_=eb78eefee007e&__ajax__=1&pid=mm_10011550_0_0&unid=&clk1=&page=5&pageSize=60&pvid=200_11.15.192.192_17308_1557243744053&ppage=3&squareFlag=&sourceId=search&ppathName=&supportCod=&city=&ppath=&dc12=&pageNav=true&itemAssurance=&fcatName=&price=&cat=&from=&tmall=&key=%E4%B8%9D%E8%A2%9C&fcat=&debug=false&sort=&exchange7=&custAssurance=&postFree=&npx=50&location=&personalizeSwitch=



第一页  上
https://ai.taobao.com/search/getItem.htm?page=1&sourceId=search&key=T恤&ppage=1&pageNav=true
第一页  下
https://ai.taobao.com/search/getItem.htm?page=2&sourceId=search&key=T恤&pageNav=false&ppage=0

https://ai.taobao.com/search/getItem.htm?page=3&sourceId=search&key=T恤&ppage=2&pageNav=true
https://ai.taobao.com/search/getItem.htm?page=4&sourceId=search&key=T恤&pageNav=false&ppage=0


page/2  请求页数
ppage=页数 单页上  代表当前页

https://ai.taobao.com/search/getItem.htm?page=3&sourceId=search&key=t%E6%81%A4&ppage=2&pageNav=true


一直当页数遍历到失败结束
'''


def get_datass(html):
    reg = r"\{\"isTmall\":.*?\}"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data



#html_info = get_html("https://ai.taobao.com/search/getItem.htm?page=1&sourceId=search&key=T恤&ppage=1&pageNav=true")
#print(html_info)


#print(get_datass(html_info))
#print(len(get_datass(html_info)))


'''

"1",
"resourceId":"589088583790",
"eurl":"https://click.simba.taobao.com/cc_im?p=T%D0%F4&amp;s=1251409319&amp;k=577&amp;e=uFQjHeFygYrsIRu05QwD5WA8BKgfF6R33AkSlHXuE8HPsfPRE4Xr8YDaCvXFu7M7kcrDiZj%2B6rE7HL88DRWkiODjOHp5a1pYbaP0Ylrbvum0p2vpAxzMPt%2F5TjLanIedJ0hvzNKh%2BUONRO9HPP2BnJR%2FM%2BqAKbRR9NJIh06vt4VPbXBsPoiUs4f3OWijuvB47NQI0sWjnAua0bXGT6CSui3NgVREApmFWXY4S9kenbxYSPEm8TCam0ZkiSnN5JRKRl6y%2FCnSvif43%2FozJu%2B%2F%2Bfhq%2B65wxoA32tov6qcQ98J%2BpGswa5Wj1w9yH4J%2BNRc4yUESE%2FnjUjAdQ05eewnmIbE1mMEYJ%2FsMSRueFw6auuZHHBPHnQAE%2FTBIVXHjXsWqqhbMq9lESKg9PiqqRxKwua8Uk1eIi6Xoru8uRdQz9pTMdTHugo0%2B%2BpIQIb0DLguOzMCUXUXFH5XK2hpgQ%2F9OfhrIToGG6gVzqZdDiWglfnynaSi6zQr8nRUwiqwOPRhbIpwrFXfaLre1IRblwJZM0VoDvDbbpvMIdprcIx6w3gJ17uAsXGkasmA8BKgfF6R3",
"salePrice":"85.00",
"has_1212coupon":"0",
"sell":"11",
"redKey":"T恤",
"auctionTag":"385,587,907,1163,1478,1483,2049,2059,2123,3851,3974,4166,4491,4550,4555,5895,6603,8007,8326,8583,11083,11266,11339,11531,15563,17739,17803,18379,18763,25282,28353,28802,53121,60418,62082,65281,67521,70465,91841,101761,101762,103489,103681,107202,107842,112386,112961,115329,119937,120962,122113,249858,249986,281602,299394,364482,100022207,100022300",
"showRedbag":0,
"tbGoodSLink":"https://img.alicdn.com/imgextra/i4/118310905/O1CN01Ub1Eoy1IYWxtIlfiS_!!0-saturn_solar.jpg_sum.jpg",
"title":"t短袖体恤 男装服上衣潮牌打底衫 潮流 韩版",
"redPacket":"0",
"wangWangId":"正天羊旗舰店",
"goodsPrice":"29900",
"p4pIndex":59,
"tagType":"",
"hideSales":false,
"location":"浙江 嘉兴",
"iSMALL":"1",
"tmall":"1",
"hiddenWangwang":true



"0",
"resourceId":"592489839433",
"eurl":"https://click.simba.taobao.com/cc_im?p=T%D0%F4&amp;s=1251409319&amp;k=557&amp;e=gwvdlLyflUPsIRu05QwD5WA8BKgfF6R33AkSlHXuE8HPsfPRE4Xr8YDaCvXFu7M7kcrDiZj%2B6rHR8khNXbD1yMecnFdpjCi7baP0Ylrbvum0p2vpAxzMPt%2F5TjLanIedJ0hvzNKh%2BUONRO9HPP2BnJR%2FM%2BqAKbRR9NJIh06vt4VPbXBsPoiUs4f3OWijuvB47NQI0sWjnAua0bXGT6CSui3NgVREApmFWXY4S9kenbxYSPEm8TCam0ZkiSnN5JRKRl6y%2FCnSvif43%2FozJu%2B%2F%2Bfhq%2B65wxoA32tov6qcQ98KjEronft3JBSdR5xDzK9vABf0y78edGcoWdsLDVR62WJZI4t6BT%2FAEjdzqF36JU6lMQgw914l7QSmc%2BdD30fyTLezHtgPH8mPjTPCLv6yu4FMSImYXJq2Gof9dBEFyuN7sIeeb3kIAntDulmFlYoNzgzyVCbK6FfV0gpUTYKq%2FARZ2wsNVHrZY8nFi%2BdK0Tj2p3kYqJM5qYju6ON3oirdU6so7XbtUWS86fdgVlg4PIXExboqt8t%2BfUovp9tGu5HY%3D",
"salePrice":"37.48",
"has_1212coupon":"0",
"sell":"45",
"redKey":"T恤",
"auctionTag":"385,587,907,1163,1483,2059,3851,3915,4491,4550,4555,6603,11083,11339,11531,15563,16395,17739,17803,21442,25282,50370,52290,61890,67521,104514,120962,143746,346562",
"showRedbag":0,
"tbGoodSLink":"https://img.alicdn.com/imgextra/i2/112704202/O1CN01Yl4G491guYnEYmWXd_!!0-saturn_solar.jpg_sum.jpg",
"title":"鹿苝 cec短袖T恤女夏2019新款韩版",
"redPacket":"0",
"wangWangId":"201314子轩629",
"goodsPrice":"4500",
"p4pIndex":60,
"tagType":"",
"hideSales":false,
"location":"广东 广州",
"iSMALL":"0",
"tmall":"0",
"hiddenWangwang":true


"0",
"resourceId":"566329684579",
"eurl":"https://click.simba.taobao.com/cc_im?p=T%D0%F4&amp;s=1251409319&amp;k=557&amp;e=fvRknmy5cersIRu05QwD5WA8BKgfF6R33AkSlHXuE8HPsfPRE4Xr8YDaCvXFu7M7kcrDiZj%2B6rHXV8cGErpvi1OVGspC4xdfbaP0Ylrbvum0p2vpAxzMPt%2F5TjLanIedJ0hvzNKh%2BUONRO9HPP2BnJR%2FM%2BqAKbRR9NJIh06vt4VPbXBsPoiUs4f3OWijuvB47NQI0sWjnAua0bXGT6CSui3NgVREApmFWXY4S9kenbxYSPEm8TCam0ZkiSnN5JRKRl6y%2FCnSvif43%2FozJu%2B%2F%2Bfhq%2B65wxoA32tov6qcQ98KjEronft3JBbPsfMKxJt3c1OOJnv4EVjwoip7q7wWHrpLYUtPoKR3%2BssNgVFU0DN6u0wBXhu8eYbW8ZYNdrnPi%2BJ7lVKFkBwhJh8ldRjixrVMSImYXJq2Gof9dBEFyuN7sIeeb3kIAntDulmFlYoNzgzyVCbK6FfV0gpUTYKq%2FASiKnurvBYeusTW8kFdF%2FTup3kYqJM5qYscu3MRAK78kniN44PIriw7iWJbz2I2%2BTeHHGpsRdiMCN3bwP%2B%2F%2FHtA%3D",
"salePrice":"159.60",
"has_1212coupon":"0",
"sell":"4",
"redKey":"T恤",
"auctionTag":"587,907,1163,1483,2059,2123,3851,4491,4550,4555,5190,6603,11083,11339,11531,15563,17739,17803,18379,18763,25282,27137,32385,36610,50370,52290,61890,67521,88706,100609,120962","showRedbag":0,"tbGoodSLink":"https://img.alicdn.com/imgextra/i4/49260026/O1CN01awmV101C3wo1GGHKy_!!0-saturn_solar.jpg_sum.jpg",
"title":"cnc男装美杜莎镶钻男短袖T恤2019丝",
"redPacket":"0",
"wangWangId":"tb447772",
"goodsPrice":"16800",
"p4pIndex":52,
"tagType":"",
"hideSales":false,
"location":"广东 东莞",
"iSMALL":"0",
"tmall":"0",
"hiddenWangwang":true



"0",
"resourceId":"590036493155",
"eurl":"https://click.simba.taobao.com/cc_im?p=T%D0%F4&amp;s=1251409319&amp;k=557&amp;e=VVm4H3d81oDsIRu05QwD5WA8BKgfF6R33AkSlHXuE8HPsfPRE4Xr8YDaCvXFu7M7ZFgaaVDR7Yef5rJaOMMGRWjLnM0I%2FOLSbaP0Ylrbvum0p2vpAxzMPt%2F5TjLanIedJ0hvzNKh%2BUONRO9HPP2BnJR%2FM%2BqAKbRR9NJIh06vt4VPbXBsPoiUs4f3OWijuvB47NQI0sWjnAua0bXGT6CSui3NgVREApmFWXY4S9kenbxYSPEm8TCam0ZkiSnN5JRKRl6y%2FCnSvif43%2FozJu%2B%2F%2Bfhq%2B65wxoA32tov6qcQ98KjEronft3JBbPsfMKxJt3c1OOJnv4EVjwUYFe5DLQ2kAWgRMY%2FZWbkG6gyGNZYC73WY5U8QGeih%2Fi4xSNatuS5s%2F1m7SLtJpUVgqBjb%2FgtHVMSImYXJq2Gof9dBEFyuN7sIeeb3kIAntDulmFlYoNzgzyVCbK6FfV0gpUTYKq%2FARRgV7kMtDaQPB1MynMsAyKp3kYqJM5qYn8wa%2FGlXZ0TBZn1YOSZrz5n2V%2BDybzJjeHHGpsRdiMCN3bwP%2B%2F%2FHtA%3D",
"salePrice":"",
"has_1212coupon":"0",
"sell":"0",
"redKey":"T恤",
"auctionTag":"",
"showRedbag":0,
"tbGoodSLink":"https://img.alicdn.com/imgextra/i1/55140999/O1CN01RCuWD81JFaC0gg7bJ_!!0-saturn_solar.jpg_sum.jpg",
"title":"夏季短袖T恤清爽吸汗透气百搭简单2019",
"redPacket":"0",
"wangWangId":"吴建华_19901113",
"goodsPrice":"9900",
"p4pIndex":53,
"tagType":"",
"hideSales":false,
"location":"中国",
"iSMALL":"0",
"tmall":"0",
"hiddenWangwang":true




'''



#获取数据
#0. 请求商品类型 类型key
#1. 资源ID \"resourceId\":\"(.*?)\",
#2. 商品链接  get_link()
#3. 图片链接 \"tbGoodSLink\":\"(.*?)\",
#4. 商品名称 get_title()   get_description()
#5. 旺旺ID  \"wangWangId\":\"(.*?)\",
#6. 商家地址 \"location\":\"(.*?)\", 
#7. 商品价格  \"salePrice\":\"(.*?)\",   
#8. 销量   \"sell\":\"(.*?)\", 
#9. 价格单位分 要除以100   \"goodsPrice\":\"(.*?)\",   


def get_redKey(html):
    reg = r"\"redKey\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data


def get_link(html):
    reg = r"\"eurl\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#获取头
#"title":
def get_title(html):
    reg = r"\"title\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#print(get_title(new_html_2))

def get_description(html):
    reg = r"\"description\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

# 资源id
def get_resourceid(html):
    reg = r"\"resourceId\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#商品图片链接
def get_tbGoodSLink(html):
    reg = r"\"tbGoodSLink\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#旺旺ID 店家名称
def get_wangWangId(html):
    reg = r"\"wangWangId\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#商家地址
def get_location(html):
    reg = r"\"location\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#商品价格
def get_salePrice(html):
    reg = r"\"salePrice\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#销量
def get_sell(html):
    reg = r"\"sell\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#商品定价
def get_goodsPrice(html):
    reg = r"\"goodsPrice\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#csv_data_file = 'D:/py_test/yibiao_Auto/report/xyzg_data/tb_test_changsoutxue_1.csv'

#csv_data_file = 'D:/tb_test_nvzhuang_1.csv'

def get_cod_datas(csv_data_file,html_info,felei_data):
    for datas in get_datass(html_info):
        print("爬取数据： ")
        print(datas)
        print("请求商品类型："+str(felei_data))
        #get_key_val = get_redKey(datas)
        get_key_val = felei_data

        print("商品名称:")
        #print(get_title(datas))
        #print(get_description(datas))
        title_val_1 = get_title(datas)
        title_val_2 = get_description(datas)
        if title_val_1 != []:
            cod_name1 = title_val_1[0]
        else:
            cod_name1 = "isNull"
        if title_val_2 != []:
            cod_name2 = title_val_2[0]
        else:
            cod_name2 = "isNull"
        print(cod_name1)
        print(cod_name2)

        print("商品链接：")
        hrs = get_link(datas)
        if hrs !=0:
            hers = hrs[0]
            #print(hrs[0])
            links = hers.replace("&amp;", "&")
            print(links)
        else:
            links = "isNull"

        '''
        #后期单独遍历
        print("商品真实地址：")
        lins_url = get_now_Location(str(links))
        print(lins_url)
        '''
        print("商品ID : ")
        #print(get_resourceid(datas))
        resource_id = get_resourceid(datas)
        if resource_id !=[]:
            cod_resource_id = resource_id[0]
        else:
            cod_resource_id = "isNull"
        print(cod_resource_id)


        print("商品图片链接")
        #print(get_tbGoodSLink(datas))
        tb_goodslink = get_tbGoodSLink(datas)
        if tb_goodslink != []:
            title_img_link = tb_goodslink[0]
        else:
            title_img_link = "isNull"
        print(title_img_link)


        print("商品价格 -1")
        #print(get_salePrice(datas))
        salePrice_val = get_salePrice(datas)
        if salePrice_val !=[]:
            cod_price_1 = salePrice_val[0]
        else:
            cod_price_1 = "isNull"
        print(cod_price_1)

        print("商品价格 -2")
        #print(get_goodsPrice(datas))
        goodsPrice_val = get_goodsPrice(datas)
        if goodsPrice_val != []:
            cod_price_2 = goodsPrice_val[0]
        else:
            cod_price_2 = "isNull"
        print(cod_price_2)


        print("销量")
        #print(get_sell(datas))
        sell_val = get_sell(datas)
        if sell_val != []:
            cod_sales = sell_val[0]
        else:
            cod_sales = "isNull"
        print(cod_sales)

        print("店家")
        #print(get_wangWangId(datas))
        wangWangId_val = get_wangWangId(datas)
        if wangWangId_val !=[]:
            cod_shop_name = wangWangId_val[0]
        else:
            cod_shop_name = "isNull"
        print(cod_shop_name)

        print("店家位置")
        #print(get_location(datas))
        location_val = get_location(datas)
        if location_val != []:
            cod_shop_location = location_val[0]
        else:
            cod_shop_location = "isNull"
        print(cod_shop_location)

        print("\n\n")

        input_datas = [get_key_val,cod_name1,cod_name2,links,str(cod_resource_id),title_img_link,cod_price_1,cod_price_2,cod_sales,cod_shop_name,cod_shop_location]
        #print('D:/py_test/yibiao_Auto/report/xyzg_data/tb_test1.csv')

        #input_datas = [cod_name1,cod_name2]
        with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
            csv_write = csv.writer(f,dialect='excel')
            csv_write.writerow(input_datas)

#get_cod_datas(csv_data_file,html_info)



'''
第一页  上
https://ai.taobao.com/search/getItem.htm?page=1&sourceId=search&key=T恤&ppage=1&pageNav=true
第一页  下
https://ai.taobao.com/search/getItem.htm?page=2&sourceId=search&key=T恤&pageNav=false&ppage=0

https://ai.taobao.com/search/getItem.htm?page=3&sourceId=search&key=T恤&ppage=2&pageNav=true
https://ai.taobao.com/search/getItem.htm?page=4&sourceId=search&key=T恤&pageNav=false&ppage=0



'''



def run_aiTaobao(keyds,endpg,csv_data_file):
    pachong_key = keyds

    ppage_number = 1
    page_number = 1
    while page_number<endpg:
        try:
        
            print("爬取第 = "+str(page_number)+"页")
            if (page_number % 2) != 0:
                #print("ppage ="+str(ppage_number))
                print("https://ai.taobao.com/search/getItem.htm?page="+str(page_number)+"&sourceId=search&key="+pachong_key+"&ppage="+str(ppage_number)+"&pageNav=true")
                urls = "https://ai.taobao.com/search/getItem.htm?page="+str(page_number)+"&sourceId=search&key="+pachong_key+"&ppage="+str(ppage_number)+"&pageNav=true"
                html_info = get_html(urls)
                get_cod_datas(csv_data_file,html_info,pachong_key)
                ppage_number+=1

            else:
                #print("ppage=0")
                print("https://ai.taobao.com/search/getItem.htm?page="+str(page_number)+"&sourceId=search&key="+pachong_key+"&pageNav=false&ppage=0")
                urls = "https://ai.taobao.com/search/getItem.htm?page="+str(page_number)+"&sourceId=search&key="+pachong_key+"&pageNav=false&ppage=0"
                
            
            
            page_number+=1
            urls=""
            print("\n")

        except Exception as e:
            print(e)
        continue



#运行
pachongkeys = "香水"
endpg_number = 200000
csv_data_file = 'D:/tb_test_xiangshui_1.csv'
run_aiTaobao(pachongkeys,endpg_number,csv_data_file)



#html_info = get_html("https://ai.taobao.com/search/getItem.htm?page=4&sourceId=search&key=T恤&pageNav=false&ppage=0")
#print(html_info)


def get_all_data_list(html):
    reg = r"\"auction\":\[.*?\]"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#print(get_all_data_list(html_info))

def get_data_list(html):
    reg = r"\{\"clickUrl\":.*?\}"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#print(get_data_list(html_info))


'''

{"clickUrl":"//uland.taobao.com/coupon/edetail?e=Mz3P4H1q%2BNUGQASttHIRqbyUOnJaEJVU8BHCQAtv8Aim%2FPqYSC%2BIlnWjM9cUG9NbUgxrwGIU5VSCZGEHIhcpum7LvaUfVaFWDfqEFBOhTcyPNEqnS4RSdJkIFKnAXZ%2FAnGGPvkJt4vg%3D&amp;engpvid=100_11.139.248.86_120885_6061557286186278354",
"picWidth":500,
"description":"短袖&lt;span class=H&gt;t恤&lt;/span&gt;女夏装新款2019宽松大码字母印花韩版百搭学生上衣体桖潮",
"tkRate":550,
"enginePvid":"100_11.139.248.86_120885_6061557286186278354",
"nick":"baolidie宝丽蝶女装旗舰店",
"picUrl":"//gaitaobao4.alicdn.com/tfscom/i4/2938765121/O1CN01M1Oj2p1nhSlGHt1Nt_!!0-item_pic.jpg",
"couponAmount":"1000",
"sellerId":2938765121,
"freeShipping":true,
"price":139.00,
"tagType":"","
hideSales":false,
"inCampaign":0,
"originalPicUrl":"//gaitaobao4.alicdn.com/tfscom/i4/2938765121/O1CN01M1Oj2p1nhSlGHt1Nt_!!0-item_pic.jpg",
"originalPicWidth":0,
"picHeight":500,
"saleCount":314,
"auctionTag":"587,907,1163,1478,1483,2049,2059,3851,3915,3974,4166,4491,4550,4555,6603,11083,11339,11531,15563,16395,17739,17803,28353,28802,54913,60418,62082,67521,72386,73089,84801,84865,101761,101762,103489,103681,103937,107842,119937,122049,281666,288962,368770,371010,371074",
"showRedbag":1,
"itemLocation":"广东 广州",
"origPicUrl":"//gaitaobao4.alicdn.com/tfscom/i4/2938765121/O1CN01M1Oj2p1nhSlGHt1Nt_!!0-item_pic.jpg",
"itemId":586079264202,"originalPicHeight":0,
"redPacket":"0",
"commentNickName":"",
"picClickUrl":"//uland.taobao.com/coupon/edetail?e=Mz3P4H1q%2BNUGQASttHIRqbyUOnJaEJVU8BHCQAtv8Aim%2FPqYSC%2BIlnWjM9cUG9NbUgxrwGIU5VSCZGEHIhcpum7LvaUfVaFWDfqEFBOhTcyPNEqnS4RSdJkIFKnAXZ%2FAnGGPvkJt4vg%3D&amp;engpvid=100_11.139.248.86_120885_6061557286186278354",
"biz30Day":314,
"comment":"",
"userType":1,
"category":50000671,
"realPrice":39.00,
"sclickUrl":"//uland.taobao.com/coupon/edetail?e=Mz3P4H1q%2BNUGQASttHIRqbyUOnJaEJVU8BHCQAtv8Aim%2FPqYSC%2BIlnWjM9cUG9NbUgxrwGIU5VSCZGEHIhcpum7LvaUfVaFWDfqEFBOhTcyPNEqnS4RSdJkIFKnAXZ%2FAnGGPvkJt4vg%3D&amp;engpvid=100_11.139.248.86_120885_6061557286186278354"
},


'''

def get_link_2(html):
    reg = r"\"clickUrl\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

'''
for getdata in get_data_list(html_info):
    print(getdata)
    print("\n")
    print("请求商品类型：")
    get_key_val = "T恤"
    print("商品名称:")
    #print(get_title(datas))
    #print(get_description(datas))
    title_val_1 = get_title(getdata)
    title_val_2 = get_description(getdata)
    if title_val_1 != []:
        cod_name1 = title_val_1[0]
    else:
        cod_name1 = "isNull"
    if title_val_2 != []:
        cod_name2 = title_val_2[0]
    else:
        cod_name2 = "isNull"
    print(cod_name1)
    print(cod_name2)

    print("商品链接：")
    hrs = get_link_2(getdata)
    if hrs !=0:
        hers = hrs[0]
        #print(hrs[0])
        links = hers.replace("&amp;", "&")
        print(links)
    else:
        links = "isNull"


    print("\n\n")
'''