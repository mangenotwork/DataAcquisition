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
    data = re.findall(reger, str(html))
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


import mandb

'''
                    #类型： DB交互
                    #执行查询  查询结果
'''
def ManDB(func=None, param=None):
    def deco(func):
        def wrapper(*args,**kwargs):
            man_db = mandb.DB()
            return func(man_db,*args,**kwargs)          
        wrapper.__name__ = func.__name__
        return wrapper
    return deco if not func else deco(func)


#判断数据是否存在
@ManDB
def judge_sql(man_db,names):
    print(names)
    sql ="SELECT count(cod_name)\
                from tb_tm_pachong_data_1 \
                where cod_name = '"+names+"' ;\
    "
    print(sql)
    return_datas = man_db.execute_seles(sql)
    if return_datas[0][0] == 0:
        print(" { 新数据 } ")
        return True
    else:
        print(" { 更新数据 } ")
        return False



#添加商品
@ManDB
def add_sql(man_db,cod_fenlei,cod_name,cod_link,pingtai,cod_resource_id,title_img_link,cod_price_1,cod_price_2,cod_sales,cod_shop_name,cod_shop_location,collection_time):
    sql ="INSERT INTO tb_tm_pachong_data_1 ( cod_fenlei, cod_name, cod_link, pingtai, cod_resource_id, title_img_link, cod_price_1, cod_price_2, \
    cod_sales, cod_shop_name, cod_shop_location, collection_time) \
    VALUES ( '"+cod_fenlei+"', '"+cod_name+"','"+cod_link+"','"+pingtai+"', '"+cod_resource_id+"','"+title_img_link+"','"+cod_price_1+"', '"+cod_price_2+"',\
    '"+cod_sales+"','"+cod_shop_name+"', '"+cod_shop_location+"','"+collection_time+"');"

    #print(sql)

    man_db.execute(sql)
    print(" [ *** 添加新数据 *** ] ")


#更新商品信息
@ManDB
def updata_sql(man_db,cod_name,cod_price_1,cod_price_2,cod_sales,collection_time):
    sql = "UPDATE tb_tm_pachong_data_1 set cod_price_1 = '"+cod_price_1+"',cod_price_2 = '"+cod_price_2+"',\
    cod_sales = '"+cod_sales+"',collection_time = '"+collection_time+"' where cod_name = '"+cod_name+"' ;"
    man_db.execute(sql)
    print(" [ *** 更新商品信息 *** ] ")


#更新商品数据的方法
def get_cod_datas_updata(csv_data_file,html_info,felei_data):
    for datas in get_datass(html_info):
        try:
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

            
            #后期单独遍历
            print("商品真实地址：")
            lins_url = get_now_Location(str(links))
            print(lins_url)
            
            if "item.taobao.com" in lins_url:
                pingtai_data="淘宝"
            elif "detail.tmall.com" in lins_url:
                pingtai_data="天猫"
            else:
                pingtai_data="淘宝,天猫"


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

            input_datas = [get_key_val,cod_name1,cod_name2,links,str(cod_resource_id),title_img_link,cod_price_1,cod_price_2,cod_sales,cod_shop_name,cod_shop_location]
            
            collection_time = str(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())))

            print(" *** 更新数据 *** ")
            #如果商品不存在则添加商品
            #如果商品存在则更新商品
            if judge_sql(cod_name1) == True:
                #cod_fenlei,cod_name,cod_link,pingtai,cod_resource_id,title_img_link,cod_price_1,cod_price_2,cod_sales,cod_shop_name,cod_shop_location,collection_time
                add_sql(get_key_val,cod_name1,lins_url,pingtai_data,str(cod_resource_id),
                    title_img_link,cod_price_1,cod_price_2,cod_sales,cod_shop_name,
                    cod_shop_location,collection_time)
            else:
                #cod_name,cod_price_1,cod_price_2,cod_sales,collection_time
                updata_sql(cod_name1,cod_price_1,cod_price_2,cod_sales,collection_time)

            #time.sleep(2)

            print("\n\n")
        except:
            print("\n\n")



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
        print('D:/py_test/yibiao_Auto/report/xyzg_data/tb_test1.csv')
        input_datas = [cod_name1,cod_name2]
        with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
            csv_write = csv.writer(f,dialect='excel')
            csv_write.writerow(input_datas)
        time.sleep(2)

#get_cod_datas(csv_data_file,html_info)



'''
第一页  上
https://ai.taobao.com/search/getItem.htm?page=1&sourceId=search&key=T恤&ppage=1&pageNav=true
第一页  下
https://ai.taobao.com/search/getItem.htm?page=2&sourceId=search&key=T恤&pageNav=false&ppage=0

https://ai.taobao.com/search/getItem.htm?page=3&sourceId=search&key=T恤&ppage=2&pageNav=true
https://ai.taobao.com/search/getItem.htm?page=4&sourceId=search&key=T恤&pageNav=false&ppage=0



'''


def run_aiTaobao_updata(keyds,endpg,csv_data_file):
    pachong_key = keyds

    ppage_number = 1
    page_number = 1
    while page_number<endpg:
        
        print("爬取第 = "+str(page_number)+"页")
        if (page_number % 2) != 0:
            #print("ppage ="+str(ppage_number))
            print("https://ai.taobao.com/search/getItem.htm?page="+str(page_number)+"&sourceId=search&key="+pachong_key+"&ppage="+str(ppage_number)+"&pageNav=true")
            urls = "https://ai.taobao.com/search/getItem.htm?page="+str(page_number)+"&sourceId=search&key="+pachong_key+"&ppage="+str(ppage_number)+"&pageNav=true"
            html_info = get_html(urls)
            #get_cod_datas(csv_data_file,html_info,pachong_key)
            get_cod_datas_updata(csv_data_file,html_info,pachong_key)
            ppage_number+=1
        else:
                #print("ppage=0")
                print("https://ai.taobao.com/search/getItem.htm?page="+str(page_number)+"&sourceId=search&key="+pachong_key+"&pageNav=false&ppage=0")
                urls = "https://ai.taobao.com/search/getItem.htm?page="+str(page_number)+"&sourceId=search&key="+pachong_key+"&pageNav=false&ppage=0"

            
        page_number+=1
        urls=""
        print("\n")






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
'''
pachongkeys = "丝袜"
endpg_number = 200000
csv_data_file = 'D:/tb_test_siwa_1.csv'
run_aiTaobao(pachongkeys,endpg_number,csv_data_file)
'''

#更新
def refresh_run(list_fenlei,files_csv):
    for fenlei_data in list_fenlei:
        #只爬1000页  
        #一个月更新100页
        endpg_number = 100
        csv_data_file = files_csv
        #run_aiTaobao(fenlei_data,endpg_number,csv_data_file)
        run_aiTaobao_updata(fenlei_data,endpg_number,csv_data_file)


list_fenlei = ["T恤","长袖T恤","女装","男装","女鞋","男鞋","连衣裙","伞","旗袍","卫衣","开衫"]

all_keys = ["伴娘服", "沙滩裙", "敬酒服", "小礼服", "晚礼服",
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

#refresh_run(all_keys,csv_data_file)




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






import caifen

ppfl_keys2 = caifen.ppfldatas()





csv_data_file = 'D:/PPFL_TBTM_5_30.csv'


task_keys = []
for i in txt.split(" "):
    if i != "":
        #print(i)
        task_keys.append(i)

print(task_keys)

refresh_run(ppfl_keys2,csv_data_file)