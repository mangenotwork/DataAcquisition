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


import urllib
import requests
import time,re,os,sys,random
import datetime
import urllib.request
import urllib.error

from urllib.request import urlopen


from PIL import Image, ImageDraw, ImageFont
import random


import redis



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



def get_proxy1():
    try:
        r = redis.StrictRedis(host='192.168.1.79',port='6379',db=1)
        ipnumber = r.zcard('proxy:ips')
        if ipnumber <= 1:
            number = 0
        else:
            number = random.randint(0, ipnumber-1)
        a = r.zrange('proxy:ips',0,-1,desc=True)
        #print(a)
        #print(a[number].decode("utf-8"))
        return a[number].decode("utf-8")
    except Exception as e:
        return ""


#print(get_proxy1())


#Get网页，返回内容
def get_html( url_path, payload = '', cookies = ''):
    try:
        ip = get_proxy1()
        print(ip)
        proxies = {"http":ip}
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



#Get网页，返回内容
def get_html1( url_path, payload = '', cookies = '',proxies=""):
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





#test_url = "https://xin.baidu.com/s?q=华西&t=0"


#print(get_html(test_url))

#data1 = get_html(test_url)


def get_list(html):
    datas = etree.HTML(html)
    info = datas.xpath('/html/body//div[@class="zx-list-item"]')
    print(info)
    if info == []:
        return False
    else:
        t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)
        return t.decode("utf-8")




#print(get_list(data1))

#cimgdata = get_list(data1)

def filter_td(html):
    html = str(html)
    reg = r"url\((.+?)\)"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data


def gettitle(html):
    html = str(html)
    reg = r"<a.+?title=\"(.+?)\">"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, html)
    return data




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
        Path_img = "F:/baiduimg/"+inputid+".jpg"
        #dbimg = "/ttys/"+inputid+"."+dex
        urllib.request.urlretrieve(url,Path_img)
        #add_sql(ysid,dbimg)
        print("download succees ====> "+Path_img)
        return Path_img
    except Exception as e:
        print(e)
        return False






#image = Image.new(mode='RGBA', size=(50, 50),)


def c_imgs(txtdata,names):
    coler = ["#e8ab6f","#8A2BE2","#A52A2A","#66CC33","#FF3333","#4169E1","#8b4513"]
    image = Image.new("RGB",(100,100),random.choice(coler))
    draw_table = ImageDraw.Draw(im=image)

    if len(txtdata) == 1:
        draw_table.text(xy=(15, 15), text=txtdata, fill='#fff', font=ImageFont.truetype('C:\\Windows\\Fonts\\simhei.ttf', 70))
    elif len(txtdata) == 2:
        #draw_table.text(xy=(10, 10), text=u' '+txtdata[0]+'\n '+txtdata[1]+'', fill='#fff', font=ImageFont.truetype('C:\\Windows\\Fonts\\simhei.ttf', 40))
        draw_table.text(xy=(10, 30), text=u''+txtdata+'', fill='#fff', font=ImageFont.truetype('C:\\Windows\\Fonts\\simhei.ttf', 40))
    elif len(txtdata) == 3:
        draw_table.text(xy=(10, 10), text=u' '+txtdata[0]+'\n'+txtdata[1:3]+'', fill='#fff', font=ImageFont.truetype('C:\\Windows\\Fonts\\simhei.ttf', 40))
    elif len(txtdata) == 4:
        draw_table.text(xy=(10, 10), text=u''+txtdata[0:2]+'\n'+txtdata[2:4]+'', fill='#fff', font=ImageFont.truetype('C:\\Windows\\Fonts\\simhei.ttf', 40))
    #draw_table.text(xy=(10, 10), text=u'漫鸽\n漫鸽', fill='#fff', font=ImageFont.truetype('C:\\Windows\\Fonts\\simhei.ttf', 40))

    #draw_table.text(xy=(10, 10), text=u' 鸽\n漫鸽', fill='#fff', font=ImageFont.truetype('C:\\Windows\\Fonts\\simhei.ttf', 40))

    #draw_table.text(xy=(10, 10), text=u' 鸽\n 鸽', fill='#fff', font=ImageFont.truetype('C:\\Windows\\Fonts\\simhei.ttf', 40))

    

    #image.show()  # 直接显示图片
    imglopath = 'F:/baiduimg/'+names+'.png'
    image.save(imglopath, 'PNG')  # 保存在当前路径下，格式为PNG
    image.close()
    return imglopath
    


#c_imgs("我日","nihao2")






'''
geturls = filter_td(cimgdata)
print(geturls)
if geturls!=[]:
    print(geturls[0])
    downld_img(geturls[0],"aaaaaa")
else:
    print("not img")
    #print(gettitle(cimgdata))
    titledata = gettitle(cimgdata)
    if titledata !=[]:
        print(titledata[0])
        c_imgs(titledata[0],"aaacc")
    else:
        print("not found!")
'''



# -*- coding: utf-8 -*-
import oss2



def svimg(svimgs):
    svimgs_name = svimgs.split("/")[-1]
    print(svimgs_name)
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth('LTAIcXIGZIwvejz8', 'P6LUyMcw5v9I2FzpLeIGtBkV2n8n2E')
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, 'http://oss-cn-shenzhen.aliyuncs.com', 'yibiao')

    # <yourLocalFile>由本地文件路径加文件名包括后缀组成，例如/users/local/myfile.txt
    # 公司商标
    bucket.put_object_from_file('company_img/'+svimgs_name, svimgs)

    print("https://yibiao.oss-cn-shenzhen.aliyuncs.com/company_img/"+svimgs_name)
    return "https://yibiao.oss-cn-shenzhen.aliyuncs.com/company_img/"+svimgs_name


def svimg_shareholder(svimgs):
    svimgs_name = svimgs.split("/")[-1]
    print(svimgs_name)
    # 阿里云主账号AccessKey拥有所有API的访问权限，风险很高。强烈建议您创建并使用RAM账号进行API访问或日常运维，请登录 https://ram.console.aliyun.com 创建RAM账号。
    auth = oss2.Auth('LTAIcXIGZIwvejz8', 'P6LUyMcw5v9I2FzpLeIGtBkV2n8n2E')
    # Endpoint以杭州为例，其它Region请按实际情况填写。
    bucket = oss2.Bucket(auth, 'http://oss-cn-shenzhen.aliyuncs.com', 'yibiao')
    # 项目负责人图标
    # shareholder_img
    bucket.put_object_from_file('shareholder_img/'+svimgs_name, svimgs)
    print("https://yibiao.oss-cn-shenzhen.aliyuncs.com/shareholder_img/"+svimgs_name)
    return "https://yibiao.oss-cn-shenzhen.aliyuncs.com/shareholder_img/"+svimgs_name


import mysql_do as mandb


'''
#获取业绩通公司名称

import mysql_do as mandb

c_datas = mandb.get_companydata()
print(c_datas)

for ccc in c_datas:
    id_val = ccc["id"].strip()
    company_val = ccc["company"].strip()
    print(id_val+"  ===> "+company_val)
    #url = "https://xin.baidu.com/s?q="+company_val+"&t=0&fl=1&castk=LTE%3D"
    url = "https://xin.baidu.com/s?q="+company_val+"&t=0"
    getdata = get_html1(url)

    #print(getdata)
    #time.sleep(5)

    
    cimgdata = get_list(getdata)

    if cimgdata == False:
        print("nonono")
        dbtourl = "0"
        

    geturls = filter_td(cimgdata)
    print(geturls)
    if geturls!=[]:
        print(geturls[0])
        svok = downld_img(geturls[0],id_val+"_imges")
        if svok != False:
            dbtourl = svimg(svok)
    else:
        print("not img")
        #print(gettitle(cimgdata))
        titledata = gettitle(cimgdata)
        if titledata !=[]:
            print(titledata[0])
            imglopaths = c_imgs(titledata[0],id_val+"_imges")
            dbtourl = svimg(imglopaths)
        else:
            print("not found!")

    #将图片保存的路径存入数据库
    print("DB --> "+dbtourl)
    mandb.set_imgdata(dbtourl,id_val)

    #time.sleep(3)
'''



def runings(htmls,id_val):
    cimgdata = get_list(htmls)

    if cimgdata == False:
        print("nonono")
        dbtourl = "0"
        

    geturls = filter_td(cimgdata)
    print(geturls)
    if geturls!=[]:
        print(geturls[0])
        svok = downld_img(geturls[0],id_val+"_imges")
        if svok != False:
            dbtourl = svimg(svok)
    else:
        print("not img")
        #print(gettitle(cimgdata))
        titledata = gettitle(cimgdata)
        if titledata !=[]:
            print(titledata[0])
            imglopaths = c_imgs(titledata[0],id_val+"_imges")
            dbtourl = svimg(imglopaths)
        else:
            print("not found!")

    #将图片保存的路径存入数据库
    print("DB --> "+dbtourl)
    mandb.set_imgdata(dbtourl,id_val)





from selenium import webdriver  
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common import exceptions
from selenium.webdriver import ActionChains
import os
import time

#chromedriver.exe  地址
chromedriver_EXE_path = "D:/py_test/yibiao_Auto/Static_tool/chromedriver.exe"


#代理IP
'''
 {ip: '103.38.40.162', port: '13128', username: '262872626', 'pwd': '123456'},
    {ip: '103.38.40.226', port: '13128', username: '262872626', 'pwd': '123456'},
    {ip: '123.183.217.26', port: '13128', username: '262872626', 'pwd': '123456'},
    {ip: '123.183.217.77', port: '13128', username: '262872626', 'pwd': '123456'},
    {ip: '103.23.8.132', port: '13128', username: '262872626', 'pwd': '123456'},
    {ip: '103.23.8.221', port: '13128', username: '262872626', 'pwd': '123456'},
    {ip: '103.23.8.226', port: '13128', username: '262872626', 'pwd': '123456'},
    {ip: '58.220.21.32', port: '13128', username: '262872626', 'pwd': '123456'},
    {ip: '58.220.21.36', port: '13128', username: '262872626', 'pwd': '123456'},
    {ip: '58.220.21.76', port: '13128', username: '262872626', 'pwd': '123456'},





// {ip: '1.82.230.118', port: '888', username: 'cj75k', pwd: 'cj75k'},
  // {ip: '222.73.48.174', port: '888', username: 'cj75k', pwd: 'cj75k'},
  // {ip: '39.106.150.97', port: '888', username: 'cj75k', pwd: 'cj75k'},
  // {ip: '112.29.170.76', port: '888', username: 'cj75k', pwd: 'cj75k'},
  // {ip: '103.21.142.201', port: '888', username: 'cj75k', pwd: 'cj75k'},
  // {ip: '103.21.142.173', port: '888', username: 'cj75k', pwd: 'cj75k'},
  // {ip: '103.21.142.181', port: '888', username: 'cj75k', pwd: 'cj75k'},
  // {ip: '120.210.206.180', port: '888', username: 'cj75k', pwd: 'cj75k'},
  // {ip: '210.16.180.254', port: '888', username: 'cj75k', pwd: 'cj75k'},
  // {ip: '123.249.34.10', port: '888', username: 'cj75k', pwd: 'cj75k'},
  // {ip: '218.92.143.27', port: '18027', username: 'pc326', pwd: '111'},
  // {ip: '218.92.143.32', port: '18032', username: 'pc326', pwd: '111'},





  // {ip: '58.220.21.162', port: '16162', username: 'pc326', pwd: '111'},
    // {ip: '58.220.21.177', port: '16177', username: 'pc326', pwd: '111'},
    // {ip: '180.97.187.202', port: '26202', username: 'pc326', pwd: '111'},
    // {ip: '180.97.187.207', port: '26207', username: 'pc326', pwd: '111'},
    // {ip: '103.23.8.132', port: '18132', username: 'pc326', pwd: '111'},
    // {ip: '103.23.8.221', port: '18221', username: 'pc326', pwd: '111'},
    // {ip: '220.167.106.177', port: '18177', username: 'pc326', pwd: '111'},
    // {ip: '220.167.106.207', port: '18207', username: 'pc326', pwd: '111'},

'''




chromeOptions = webdriver.ChromeOptions()
#1
#chromeOptions.add_argument("--proxy-server=http://103.38.40.162:13128")

#2
#chromeOptions.add_argument("--proxy-server=http://103.38.40.226:13128")

#3
#chromeOptions.add_argument("--proxy-server=http://123.183.217.26:13128")

#4
#chromeOptions.add_argument("--proxy-server=http://123.183.217.77:13128")

#5
#chromeOptions.add_argument("--proxy-server=http://103.23.8.132:13128")

#6
#chromeOptions.add_argument("--proxy-server=http://103.23.8.221:13128")

#7
#chromeOptions.add_argument("--proxy-server=http://103.23.8.226:13128")

#8
#chromeOptions.add_argument("--proxy-server=http://58.220.21.32:13128")

#9
#chromeOptions.add_argument("--proxy-server=http://58.220.21.36:13128")

#10
#chromeOptions.add_argument("--proxy-server=http://58.220.21.76:13128")


'''
os.environ["webdriver.chrome.driver"] = chromedriver_EXE_path
browser = webdriver.Chrome(chromedriver_EXE_path,chrome_options = chromeOptions)
browser.get("https://xin.baidu.com/s?q=&t=0&fl=1&castk=LTE%3D")
time.sleep(1)
browser.maximize_window()
a = input("input:")
'''




def getdatas(namesss,id_val):

    input_query_3 = "/html/body/div[2]/div/div[2]/div[3]/div/div/div/input"

    browser.find_element_by_xpath(input_query_3).clear()
    #输入公司名称
    
    browser.find_element_by_xpath(input_query_3).send_keys(namesss)
    time.sleep(0.5)

    click_query_3 = '/html/body/div[2]/div/div[2]/div[3]/div/div/input'
    browser.find_element_by_xpath(click_query_3).click()
    #print(browser.page_source)
    getdata = browser.page_source
    runings(getdata,id_val)
    #time.sleep(1)


'''

c_datas = mandb.get_companydata()
print(c_datas)


for ccc in c_datas:
    try:
        id_val = ccc["id"].strip()
        company_val = ccc["company"].strip()
        print(id_val+"  ===> "+company_val)
        getdatas(company_val,id_val)
    except Exception as e:
        pinglvurl = browser.current_url
        print(pinglvurl)
        if pinglvurl == "https://xin.baidu.com/fs/forbidden":
            browser.back()
            time.sleep(3)
            #刷新
            browser.refresh()
        elif "xin.baidu.com/fs/check" in pinglvurl:
            print("请输入验证码")
            a = input("input:")
            #自动识别
            #browser.back()
            #time.sleep(3)
            #browser.back()
            #time.sleep(3)
            #browser.refresh()
        else:    
            print("aaa")
            #刷新
            browser.refresh()
'''



'''


for ccc in c_datas:
        id_val = ccc["id"].strip()
        company_val = ccc["company"].strip()
        print(id_val+"  ===> "+company_val)
        getdatas(company_val,id_val)
'''

import mysql_do as mandb



'''
cd = mandb.get_cd()
#print(cd)
cdlist = []

for aaacd in cd:
    print(aaacd["City_CN"])
    cdlist.append(aaacd["City_CN"])


cdlist = cdlist+ ["(",")","'","公司","有限","有限公司","集团","经理部",'临邑', '临邑县','县'
               '丹东市', '丹东','县','市','州','省']
'''


def fencidata(names):
    for aa in cdlist:
        if aa in names:
            names = names.replace(aa,"")

    testurl = "http://118.25.137.1:8888/manfenci?appid=1&appkey=1&string="+names+"&type=search"

    #print(get_html1(testurl))
    aaa = get_html1(testurl)
    print(type(aaa))
    ccc = json.loads(aaa)
    print(ccc["returndata"])
    print(type(ccc["returndata"]))

    bbb = ccc["returndata"]

    if len(bbb) >2:

        if len(bbb[0]) < 3:
            if len(bbb[1]) < 2:
                datas = bbb[1]+bbb[2]
                datas = datas[0:4]
                print(datas)
            else:
                datas = bbb[0]+bbb[1]
                datas = datas[0:4]
                print(datas)
        else:
            print(bbb[0])
            datas = bbb[0]
    else:
        datas = bbb[0]
        print(datas)

        
    return datas



'''
c_datas = mandb.get_companydata()
print(c_datas)
for ccc in c_datas:
    
    id_val = ccc["id"].strip()
    company_val = ccc["company"].strip()
    print("\n **** "+company_val)
    try:
        titledata = fencidata(company_val)
        imglopaths = c_imgs(titledata,id_val+"_imges")
        dbtourl = svimg(imglopaths)
        #将图片保存的路径存入数据库
        print("DB --> "+dbtourl)
        mandb.set_imgdata(dbtourl,id_val)
    except Exception as e:
        print("DB --> "+"0")
        mandb.set_imgdata("0",id_val)
'''






def fx_chuli(txt):
    #名字提取   副姓
    fuxing = ["谷梁", "拓跋", "夹谷", "轩辕", "令狐", "段干", "百里", "呼延", "东郭", "南门", "羊舌", "微生", "公户", "公玉", "公仪", "梁丘", "公仲", "公上", 
          "公门", "公山", "公坚", "左丘", "公伯", "西门", "公祖", "第五", "公乘", "贯丘", "公皙", "南荣", "东里", "东宫", "仲长", "子书", "子桑", "即墨", 
          "达奚", "褚师", "吴铭", "欧阳", "太史", "端木", "上官", "司马", "东方", "独孤", "南宫", "万俟", "闻人", "夏侯", "诸葛", "尉迟", "公羊", "赫连",
          "澹台", "皇甫", "宗政", "濮阳", "公冶", "太叔", "申屠", "公孙", "慕容", "仲孙", "钟离", "长孙", "宇文", "司徒", "鲜于", "司空", "闾丘", "子车", 
          "亓官", "司寇", "巫马", "公西", "颛孙", "壤驷", "公良", "漆雕", "乐正"]
    for cc in fuxing:
        if cc in txt:
            return cc
    else:
        return txt[0]

'''
for aacc in mandb.get_username():
    id_val = str(aacc["id"]).strip()
    company_val = aacc["shareholder"].strip()
    print(id_val)
    print(company_val)
    
    titledata = fx_chuli(company_val)
    print(titledata)

    imglopaths = c_imgs(titledata,id_val+"_imges")
    dbtourl = svimg_shareholder(imglopaths)
    #将图片保存的路径存入数据库
    print("DB --> "+dbtourl)
    #存入表
    mandb.set_username(id_val,dbtourl)
'''


#修改提取公司简称错误的修改图标
c_names = mandb.get_companynames("重庆第六建设有限责任公司")[0]
print(c_names)

id_val = c_names["id"]
company_val = c_names["company"].strip()
print(id_val)
print(company_val)

titledata = "重庆六建"
print(titledata)

imglopaths = c_imgs(titledata,id_val+"_imges")
dbtourl = svimg(imglopaths)
#将图片保存的路径存入数据库
print("DB --> "+dbtourl)
#存入表
#mandb.set_username_test(id_val,dbtourl,company_val)
mandb.set_imgdata(dbtourl,id_val)
