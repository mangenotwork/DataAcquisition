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
import redis
import urllib

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
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Connection': 'keep-alive',
    'Accept-Encoding': 'gzip, deflate',

}


def get_proxy():
        r = redis.StrictRedis(host='192.168.1.79',port='6379',db=1)
        ipnumber = r.zcard('proxy:ips')
        if ipnumber <= 1:
            number = 0
        else:
            number = random.randint(0, ipnumber-1)
        a = r.zrange('proxy:ips',0,-1,desc=True)
        print(a)
        print(a[number].decode("utf-8"))
        return a[number].decode("utf-8")



ip = get_proxy()
print(ip)
proxies = {"http":ip}


#Get网页，返回内容
def get_html( url_path, proxies = proxies, payload = '', cookies = ''):
    try:
        
        s = requests.Session()
        r = s.get(
                url_path,#路径
                headers=HEADER,#请求头
                params=payload,#传参 @payload 字典或者json
                cookies=cookies,#cookies
                verify=False,#SSL验证 @verify False忽略;True开启
                proxies=proxies,#代理
                timeout=20)#@timeout 超时单位 秒
        r.raise_for_status()
        #防止中文乱码
        r.encoding = 'gb2312'
        return r.text
    except ReadTimeout:
        print('Timeout')
        time.sleep(5)
        return get_html(url_path, {"http":get_proxy()})
    except ConnectionError:
        print('Connection error')
        time.sleep(5)
        return get_html(url_path, {"http":get_proxy()})
    except RequestException:
        print('RequestException')
        time.sleep(5)
        return get_html(url_path, {"http":get_proxy()})



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




#testurl1 = "http://college.gaokao.com/schlist/"
#datas1 = get_html(testurl1)

#print(datas1)



def get_dl_data(html):
    reg = r"<dl.+?</dl>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

def filter_href(html):
    html = str(html)
    reg = r"(?<=href=\").+?(?=\")|(?<=href=\').+?(?=\')"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data


def get_college_names(html):
    #/html/body/div[5]/div[4]/h2
    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@class="bg_sez"]/h2/text()')
    #print(info)
    #t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
    
    return info[0]

#获取大学信息 div 
def get_college_info_div(html):
    try:
        html = str(html)
        all_list_datas = []
        datas = etree.HTML(html)
        info = datas.xpath('/html/body//div[@class="college_msg bk"]')
        print(info)
        t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
        
        return t.decode("utf-8")
    except Exception as e:
        return ""


#生成学校ID 
def set_college_id(src):
    src+=str(time.time())
    m2 = hashlib.md5()   
    m2.update(src.encode('utf-8'))   
    useruuid = m2.hexdigest()
    return useruuid

#获取大学图标链接
def filter_src(html):
    reg = r"(?<=src=\").+?(?=\")|(?<=src=\').+?(?=\')"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    if data!=[]:
        return data[0]
    else:
        return 0

#获取ul
def get_ul_data(html):
    reg = r"<ul.+?</ul>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

#获取li
def get_li_data(html):
    reg = r"<li.+?</li>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

#获取 span
def get_span_data(html):
    reg = r"<span.+?>(.+?)</span>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data


#gxlvshu   高校隶属于 清洗
def gxlvy_qinxi(html):
    reg = r"高校隶属于：(.+?)</li>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    if data == []:
        return ""
    else:
        return data[0]


#gxszd  高校所在地  清洗
def gxszd_qinxi(html):
    reg = r"高校所在地：(.+?)</li>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    if data == []:
        return ""
    else:
        return data[0]

#院士清洗
def gx_ys_qinxi(html):
    reg = r"院士：(.+?) "
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    if data == []:
        return ""
    else:
        return data[0]

#博士点清洗
def gx_bs_qinxi(html):
    reg = r"博士点：(.+?) "
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    if data == []:
        return ""
    else:
        return data[0]


#硕士点清洗
def gx_ss_qinxi(html):
    reg = r"硕士点：(.+?)</"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    if data == []:
        return ""
    else:
        return data[0]


#通讯地址
def txdz(html):
    reg = r"通讯地址：(.+?)<br"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    if data == []:
        return ""
    else:
        return data[0]


#联系电话
def lxdh(html):
    reg = r"联系电话：(.+?)<br"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    if data == []:
        return ""
    else:
        return data[0]


#电子邮箱
def dzyx(html):
    reg = r"电子邮箱：(.+?)<br"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    if data == []:
        return ""
    else:
        return data[0]

#学校网址
def xxwz(html):
    reg = r"学校网址：(.+?)</p>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    if data == []:
        return ""
    else:
        return data[0]



#下载图标
def downld_img(url,inputid):
    '''
    dex = url.split(".")[-1]
    Path_img = "F:/ttys/"+inputid+"."+dex
    dbimg = "/ttys/"+inputid+"."+dex
    urllib.request.urlretrieve(url,Path_img)
    add_sql(ysid,dbimg)
    print("download succees ====> "+Path_img)
    '''
    try:
        #dex = url.split(".")[-1]
        Path_img = "F:/college_img/"+inputid+"_img.png"
        #dbimg = "/ttys/"+inputid+"."+dex
        urllib.request.urlretrieve(url,Path_img)
        #add_sql(ysid,dbimg)
        print("download succees ====> "+Path_img)
        return inputid+"_img.png"
    except Exception as e:
        print(e)
        return ""


'''
#大学  1 到 2667   http://college.gaokao.com/school/3/
testurl2 = "http://college.gaokao.com/school/1/"
datas2 = get_html(testurl2)


#print(datas2)
#大学学校名称
college_names = get_college_names(datas2).strip()
print(college_names)
college_ids = set_college_id(testurl2)
print(college_ids)
#大学学校信息
college_info_div = get_college_info_div(datas2)
print(college_info_div)
#大学图标链接
collegeimgs = filter_src(college_info_div)
print(collegeimgs)
if collegeimgs != False:
    college_img_name = downld_img(collegeimgs,college_names)
else:
    college_img_name = ""


ulinfos = get_ul_data(college_info_div)


uls1 = ulinfos[0]
uls2 = ulinfos[1]
print(uls1)
print(uls2)



lidatas = get_li_data(uls1)
print(lidatas)
#高校类型
gxtype = lidatas[0]
#高校隶属
gxlvshu = lidatas[1]
#高校所在地
gxchengshi = lidatas[2]
#高校院士，博士，硕士
gx_y_b_s = lidatas[3]


print("【高校名称】 : "+college_names)
print("【高校图标】 : "+college_img_name)
college_type_val = "|".join(get_span_data(gxtype))
print("【高校类型】 : "+college_type_val)
college_lsy_val = gxlvy_qinxi(gxlvshu)
print("【高校隶属于】 : "+college_lsy_val)
college_szd_val = gxszd_qinxi(gxchengshi)
print("【高校所在地】 : "+college_szd_val)
college_ys_number = gx_ys_qinxi(gx_y_b_s)
print("【院士】 : "+college_ys_number)
college_bs_number = gx_bs_qinxi(gx_y_b_s)
print("【博士点】 : "+college_bs_number)
college_ss_number = gx_ss_qinxi(gx_y_b_s)
print("【硕士点】 : "+college_ss_number)
college_txdz_val = txdz(uls2)
print("【通讯地址】 : "+college_txdz_val)
college_lxdh_val = lxdh(uls2)
print("【联系电话】 : "+college_lxdh_val)
college_dzyx_val = dzyx(uls2)
print("【电子邮箱】 : "+college_dzyx_val)
college_xxwz_val = xxwz(uls2)
print("【学校网址】 : "+college_xxwz_val)

'''



#院校简介  http://college.gaokao.com/school/tinfo/1/intro/
#yuanxiao_jianjie_urls = "http://college.gaokao.com/school/tinfo/1/intro/"
#yuanxiao_jianjie_datas = get_html(yuanxiao_jianjie_urls)

#院校简介 html 获取
def yuanxiao_jianjie_qinxi(html):
    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@class="jj"]')
    print(info)
    t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
    
    return t.decode("utf-8")

#获取简介内容
def yuanxiao_jianjie_getdatas(html):
    reg = r"<p>&#13;(.+?)</p>&#13;"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    if data == []:
        return ""
    else:
        return data[0]
#简介内容最终清洗
def yuanxiao_jianjie_endqinxi(html):
    qinxitxt = ['\n','\t','\u3000','&#13;']
    for qxtxt in qinxitxt:
        html = html.replace(qxtxt,"")
    return html

'''
yuanxiao_jianjie_val = yuanxiao_jianjie_qinxi(yuanxiao_jianjie_datas)
#print("【院校简介】 : "+yuanxiao_jianjie_val)

yuanxiao_jianjie_val2 = yuanxiao_jianjie_getdatas(yuanxiao_jianjie_val)
#print(yuanxiao_jianjie_val2)
print()
yuanxiao_jianjie_val3 = yuanxiao_jianjie_endqinxi(yuanxiao_jianjie_val2)
print("【院校简介】 : "+yuanxiao_jianjie_val3)
'''



# 师资力量      http://college.gaokao.com/school/tinfo/1/shizi/
#yuanxiao_sizililang_urls = "http://college.gaokao.com/school/tinfo/1/shizi/"
#yuanxiao_sizililang_datas = get_html(yuanxiao_sizililang_urls)
'''
yuanxiao_sizililang_val = yuanxiao_jianjie_qinxi(yuanxiao_sizililang_datas)
print("【师资力量】 : "+yuanxiao_sizililang_val)
'''




# 院系设置     http://college.gaokao.com/school/tinfo/1/yuanxi/
#yuanxiao_yuanxisz_urls = "http://college.gaokao.com/school/tinfo/1/yuanxi/"
#yuanxiao_yuanxisz_datas = get_html(yuanxiao_yuanxisz_urls)
'''
yuanxiao_yuanxisz_val = yuanxiao_jianjie_qinxi(yuanxiao_yuanxisz_datas)
print("【院系设置】 : "+yuanxiao_yuanxisz_val)
'''





# 专业设置     http://college.gaokao.com/school/tinfo/1/schspe/
#yuanxiao_zhuanye_urls = "http://college.gaokao.com/school/tinfo/1/schspe/"
#yuanxiao_zhuanye_datas = get_html(yuanxiao_zhuanye_urls)


#专业设置 html 清洗
def yuanxiao_zhuanye_qinxi(html):
    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@class="plan_con"]')
    print(info)
    t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
    
    return t.decode("utf-8")
'''
yuanxiao_zhuanye_val = yuanxiao_zhuanye_qinxi(yuanxiao_zhuanye_datas)
print("【专业设置】 : "+yuanxiao_zhuanye_val)
'''



#联系方式    http://college.gaokao.com/school/tinfo/1/lianxi/ 
#yuanxiao_lianxifs_urls = "http://college.gaokao.com/school/tinfo/1/lianxi/"
#yuanxiao_lianxifs_datas = get_html(yuanxiao_lianxifs_urls)
'''
yuanxiao_lianxifs_val = yuanxiao_jianjie_qinxi(yuanxiao_lianxifs_datas)
print("【联系方式】 : "+yuanxiao_lianxifs_val)

yuanxiao_lianxifs_val2 = yuanxiao_jianjie_getdatas(yuanxiao_lianxifs_val)
print(yuanxiao_lianxifs_val2)
'''

#录取分数  http://college.gaokao.com/school/tinfo/1/result/1/1/
#yuanxiao_luqu_urls = "http://college.gaokao.com/school/tinfo/1/result/1/1/"
#   【单独开爬虫】
#http://college.gaokao.com/school/tinfo/<学校>/result/<城市>/<分科>/
'''
北京=1  天津=2  辽宁=3  吉林=4  黑龙江=5  上海=6  江苏=7  浙江=8  安徽=9  福建=10  山东=11  湖北=12  湖南=13  
广东=14  重庆=15  四川=16  陕西=17  甘肃=18  河北=19  山西=20  内蒙古=21  河南=22  海南=23  广西=24  贵州=25
云南=26  西藏=27  青海=28  宁夏=29  新疆=30  江西=31  香港=33  澳门=38  台湾=39


理科=1  文科=2  综合=3  其他=4  艺术理=8  艺术文=9  综合改革=10
'''








def run1(urls_number):
    #学院主页地址
    testurl2 = "http://college.gaokao.com/school/"+str(urls_number)+"/"
    datas2 = get_html(testurl2)
    #print(datas2)

    #院校简介
    yuanxiao_jianjie_urls = "http://college.gaokao.com/school/tinfo/"+str(urls_number)+"/intro/"
    yuanxiao_jianjie_datas = get_html(yuanxiao_jianjie_urls)

    #师资力量
    yuanxiao_sizililang_urls = "http://college.gaokao.com/school/tinfo/"+str(urls_number)+"/shizi/"
    yuanxiao_sizililang_datas = get_html(yuanxiao_sizililang_urls)

    #院系设置
    yuanxiao_yuanxisz_urls = "http://college.gaokao.com/school/tinfo/"+str(urls_number)+"/yuanxi/"
    yuanxiao_yuanxisz_datas = get_html(yuanxiao_yuanxisz_urls)

    #专业设置
    yuanxiao_zhuanye_urls = "http://college.gaokao.com/school/tinfo/"+str(urls_number)+"/schspe/"
    yuanxiao_zhuanye_datas = get_html(yuanxiao_zhuanye_urls)

    #联系方式
    yuanxiao_lianxifs_urls = "http://college.gaokao.com/school/tinfo/"+str(urls_number)+"/lianxi/"
    yuanxiao_lianxifs_datas = get_html(yuanxiao_lianxifs_urls)

    #录取分数
    yuanxiao_luqu_urls = "http://college.gaokao.com/school/tinfo/"+str(urls_number)+"/result/1/1/"

    #print(datas2)
    #大学学校名称
    college_names = get_college_names(datas2).strip()
    print(college_names)
    college_ids = set_college_id(testurl2)
    #print(college_ids)
    #大学学校信息
    college_info_div = get_college_info_div(datas2)
    print(college_info_div)
    #大学图标链接
    collegeimgs = filter_src(college_info_div)
    #print(collegeimgs)
    if collegeimgs != False :
        college_img_name = downld_img(collegeimgs,college_names)
    else:
        college_img_name = "isnull"
    ulinfos = get_ul_data(college_info_div)
    if ulinfos !=[]:
        uls1 = ulinfos[0]
        uls2 = ulinfos[1]
    else:
        uls1 = ""
        uls2 = ""
    #print(uls1)
    #print(uls2)
    lidatas = get_li_data(uls1)
    #print(lidatas)
    #高校类型
    if lidatas!=[]:
        gxtype = lidatas[0]
        #高校隶属
        gxlvshu = lidatas[1]
        #高校所在地
        gxchengshi = lidatas[2]
        #高校院士，博士，硕士
        gx_y_b_s = lidatas[3]
    else:
        gxtype = ""
        #高校隶属
        gxlvshu = ""
        #高校所在地
        gxchengshi = ""
        #高校院士，博士，硕士
        gx_y_b_s = ""
    #print("【高校名称】 : "+college_names)
    #print("【高校图标】 : "+college_img_name)
    college_type_val = "|".join(get_span_data(gxtype))
    #print("【高校类型】 : "+college_type_val)
    college_lsy_val = gxlvy_qinxi(gxlvshu)
    #print("【高校隶属于】 : "+college_lsy_val)
    college_szd_val = gxszd_qinxi(gxchengshi)
    #print("【高校所在地】 : "+college_szd_val)
    college_ys_number = gx_ys_qinxi(gx_y_b_s)
    #print("【院士】 : "+college_ys_number)
    college_bs_number = gx_bs_qinxi(gx_y_b_s)
    #print("【博士点】 : "+college_bs_number)
    college_ss_number = gx_ss_qinxi(gx_y_b_s)
    #print("【硕士点】 : "+college_ss_number)
    college_txdz_val = txdz(uls2)
    #print("【通讯地址】 : "+college_txdz_val)
    college_lxdh_val = lxdh(uls2)
    #print("【联系电话】 : "+college_lxdh_val)
    college_dzyx_val = dzyx(uls2)
    #print("【电子邮箱】 : "+college_dzyx_val)
    college_xxwz_val = xxwz(uls2)
    #print("【学校网址】 : "+college_xxwz_val)

    yuanxiao_jianjie_val = yuanxiao_jianjie_qinxi(yuanxiao_jianjie_datas)
    #print("【院校简介】 : "+yuanxiao_jianjie_val)

    yuanxiao_jianjie_val2 = yuanxiao_jianjie_getdatas(yuanxiao_jianjie_val)
    #print(yuanxiao_jianjie_val2)
    #print()
    yuanxiao_jianjie_val3 = yuanxiao_jianjie_endqinxi(yuanxiao_jianjie_val2)
    #print("【院校简介】 : "+yuanxiao_jianjie_val3)

    yuanxiao_sizililang_val = yuanxiao_jianjie_qinxi(yuanxiao_sizililang_datas)
    #print("【师资力量】 : "+yuanxiao_sizililang_val)

    yuanxiao_yuanxisz_val = yuanxiao_jianjie_qinxi(yuanxiao_yuanxisz_datas)
    #print("【院系设置】 : "+yuanxiao_yuanxisz_val)

    yuanxiao_zhuanye_val = yuanxiao_zhuanye_qinxi(yuanxiao_zhuanye_datas)
    #print("【专业设置】 : "+yuanxiao_zhuanye_val)

    yuanxiao_lianxifs_val = yuanxiao_jianjie_qinxi(yuanxiao_lianxifs_datas)
    print("【联系方式】 : "+yuanxiao_lianxifs_val)

    yuanxiao_lianxifs_val2 = yuanxiao_jianjie_getdatas(yuanxiao_lianxifs_val)
    print(yuanxiao_lianxifs_val2)



    #保存数据 1    学校信息表   高校名称,高校ID,高校图标,高校类型,高校隶属于,高校所在地,院士,博士点,硕士点,通讯地址,联系电话,电子邮箱,学校网址
    #                          院校简介,联系方式,源数据地址
    print("【高校名称】 : "+college_names)
    print("【高校ID】 : "+college_ids)
    print("【高校图标】 : "+str(college_img_name))
    print("【高校类型】 : "+college_type_val)
    print("【高校隶属于】 : "+college_lsy_val)
    print("【高校所在地】 : "+college_szd_val)
    print("【院士】 : "+college_ys_number)
    print("【博士点】 : "+college_bs_number)
    print("【硕士点】 : "+college_ss_number)
    print("【通讯地址】 : "+college_txdz_val)
    print("【联系电话】 : "+college_lxdh_val)
    print("【电子邮箱】 : "+college_dzyx_val)
    print("【学校网址】 : "+college_xxwz_val)
    print("【院校简介】 : "+yuanxiao_jianjie_val3)
    print("【联系方式】 : "+yuanxiao_lianxifs_val2)
    print("【源数据地址】 : "+testurl2)

    #写入数据到csv
    addlist_1 = [college_names, college_ids, college_img_name, college_type_val, college_lsy_val, college_szd_val, college_ys_number, college_bs_number,
                college_ss_number, college_txdz_val, college_lxdh_val, college_dzyx_val, college_xxwz_val, yuanxiao_jianjie_val3, yuanxiao_lianxifs_val2,
                testurl2]
    print(addlist_1)
    with open("D:/xuexuao_info_5.csv", 'a', newline='', encoding='utf-8') as f:
        print(" ===>   add ok !!!")
        csv_write = csv.writer(f,dialect='excel')
        csv_write.writerow(addlist_1)
    print("__________________________________\n")


    #保存数据 2 表2   学校院系设置爬虫数据表       高校名称,高校ID,院系设置,院系设置-源数据地址,师资力量,师资力量-源数据地址,专业设置,专业设置-源数据地址
    #                                           录取分数-源数据地址
    print("【高校名称】 : "+college_names)
    print("【高校ID】 : "+college_ids)
    print("【院系设置】 : "+yuanxiao_yuanxisz_val)
    print("【院系设置-源数据地址】 : "+yuanxiao_yuanxisz_urls)
    print("【师资力量】 : "+yuanxiao_sizililang_val)
    print("【师资力量-源数据地址】 : "+yuanxiao_sizililang_urls)
    print("【专业设置】 : "+yuanxiao_zhuanye_val)
    print("【专业设置-源数据地址】 : "+yuanxiao_zhuanye_urls)
    print("【录取分数-源数据地址】 : "+yuanxiao_luqu_urls)
    addlist_2 = [college_names, college_ids, yuanxiao_yuanxisz_val, yuanxiao_yuanxisz_urls, yuanxiao_sizililang_val, yuanxiao_sizililang_urls,
                yuanxiao_zhuanye_val, yuanxiao_zhuanye_urls, yuanxiao_luqu_urls]
    print(addlist_2)
    with open("D:/xuexuao_pachong_5.csv", 'a', newline='', encoding='utf-8') as f:
        print(" ===>   add ok !!!")
        csv_write = csv.writer(f,dialect='excel')
        csv_write.writerow(addlist_2)
    print("__________________________________\n")





n=1
while n<=2667:
    #709 没有学校  是个 404地址
    if n in [709,747,1823,2402,2403,2404,2405,2406,2407]:
        n+=1
        continue
    print("____________________***** "+str(n)+" *****____________________________")
    run1(n)
    time.sleep(1)
    n+=1


#bug   154    693(手动添加)   
