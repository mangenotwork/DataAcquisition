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
def get_html( url_path, proxies = '', payload = '', cookies = ''):
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
        return get_html(url_path, proxies = {"http":get_proxy()})
    except ConnectionError:
        print('Connection error')
        return get_html(url_path, proxies = {"http":get_proxy()})
    except RequestException:
        print('RequestException')
        return get_html(url_path, proxies = {"http":get_proxy()})


'''
def get_html( url_path, proxie = '', payload = '', cookies = ''):
    try:
        
        s = requests.Session()
        r = s.get(
                url_path,#路径
                headers=HEADER,#请求头
                params=payload,#传参 @payload 字典或者json
                cookies=cookies,#cookies
                verify=False,#SSL验证 @verify False忽略;True开启
                proxies=proxie,#代理
                timeout=20)#@timeout 超时单位 秒
        r.raise_for_status()
        #防止中文乱码
        r.encoding = 'gb2312'
        return r.text
    except ReadTimeout:
        print('Timeout')
        return get_html(url_path)
    except ConnectionError:
        print('Connection error')
        return get_html(url_path)
    except RequestException:
        print('RequestException')
        return get_html(url_path)
'''

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





#数据库
import pymysql
import time



class DB_funtion():
	def __init__(self,host_IP,port,db_name,user_name,passwd,charset = 'utf8'):
		self.host = host_IP
		self.port = port
		self.db = db_name
		self.user = user_name
		self.passwd = passwd
		self.charset = charset
		self.conn = pymysql.Connect(host=self.host, port=self.port, db=self.db, user=self.user, passwd=self.passwd, charset=self.charset, cursorclass=pymysql.cursors.DictCursor)
		#self.conn.autocommit(True)
		self.cursor = self.conn.cursor()

	#查询
	def execute_sql(self,sql_cmd):
		self.cursor.execute(sql_cmd)
		data = self.cursor.fetchall()
		#
		return data

	def exect(self,sql_cmd):
		self.cursor.execute(sql_cmd)
		self.conn.commit()

	def __del__(self):
		#print("断开数据库连接")
		self.cursor.close()
		self.conn.close()



def get_dx_info():
	db_test1 = DB_funtion('118.25.137.1',3306,'manmc','root','liman19950620')
	get_user_id_sql = "select college_names,college_ids,luqu_url from daxue_info_pachong where temp_1 = 0;"
	user_id = db_test1.execute_sql(get_user_id_sql)
	#print(user_id)
	return user_id

def set_run(ids):
	db_test1 = DB_funtion('118.25.137.1',3306,'manmc','root','liman19950620')
	get_user_id_sql = "update daxue_info_pachong set temp_1 = 1 where college_ids='"+ids+"';"
	db_test1.exect(get_user_id_sql)


diqu_list = {"北京":1, "天津":2, "辽宁":3, "吉林":4, "黑龙江":5, "上海":6, "江苏":7, "浙江":8, "安徽":9, "福建":10, "山东":11,  
"湖北":12, "湖南":13, "广东":14, "重庆":15, "四川":16, "陕西":17, "甘肃":18, "河北":19, "山西":20, "内蒙古":21, "河南":22, "海南":23,  
"广西":24, "贵州":25, "云南":26, "西藏":27,  "青海":28,  "宁夏":29,  "新疆":30,  "江西":31,  "香港":33,  "澳门":38,  "台湾":39}


kemu_list = {"理科":1,  "文科":2,  "综合":3,  "其他":4,  "艺术理":8,  "艺术文":9,  "综合改革":10}


'''
#通过遍历的方式爬取数据
for diqu in diqu_list:
	diqu_key = diqu
	diqu_val = diqu_list[diqu]
	for kemu in kemu_list:
		kemu_key = kemu
		kemu_val = kemu_list[kemu]
		print(diqu_key,kemu_key)
		urls = "http://college.gaokao.com/school/tinfo/2/result/"+str(diqu_val)+"/"+str(kemu_val)+"/"
		print(urls)
'''	


#学校ID    学校   地区  科目  源地址  年份  最低  最高  平均  录取人数   录取批次  

#1. 在大学爬虫表取学校id与学校录取分数链接地址
#2. 通过遍历的方式爬取数据
#	
#http://college.gaokao.com/school/tinfo/<学校>/result/<城市>/<分科>/
'''
北京=1  天津=2  辽宁=3  吉林=4  黑龙江=5  上海=6  江苏=7  浙江=8  安徽=9  福建=10  山东=11  湖北=12  湖南=13  
广东=14  重庆=15  四川=16  陕西=17  甘肃=18  河北=19  山西=20  内蒙古=21  河南=22  海南=23  广西=24  贵州=25
云南=26  西藏=27  青海=28  宁夏=29  新疆=30  江西=31  香港=33  澳门=38  台湾=39

理科=1  文科=2  综合=3  其他=4  艺术理=8  艺术文=9  综合改革=10
'''
#	
#http://college.gaokao.com/school/tinfo/2/result/1/1/





def get_ul_html(html):
    html = str(html)
    all_list_datas = []
    datas = etree.HTML(html)
    info = datas.xpath('*//div[@id="pointbyarea"]/table')
    print(info)
    if info!=[]:
        t = etree.tostring(info[0], encoding="utf-8", pretty_print=True)  
        return t.decode("utf-8")
    else:
        return False


def get_tr(html):
    reg = r"<tr.+?>(.+?)</tr>"
    reger = re.compile(reg, re.S)
    data = re.findall(reger, str(html))
    return data

def get_td(html):
    reg = r"(<td.+?>|<td>)(.+?)</td>"
    reger = re.compile(reg)
    data = re.findall(reger, str(html))
    return data


def get_a(html):
    reg = r"<a.+?>(.+?)</a>"
    reger = re.compile(reg)
    data = re.findall(reger, str(html))
    return data


'''
testurl1 = "http://college.gaokao.com/school/tinfo/2/result/1/1/"
datas1 = get_html(testurl1)

#print(datas1)


ul_html = get_ul_html(datas1)

print(ul_html)

trlist = get_tr(ul_html)

for trhtml in trlist:
	if "td" in trhtml:
		print(trhtml,"\n")
		tdlist = get_td(trhtml)
		print(tdlist)
		nianfen = tdlist[0][1]
		zuidi = tdlist[1][1]
		zugao = tdlist[2][1]
		pingjun = get_a(tdlist[3][1])[0]
		lqrenshu = tdlist[4][1]
		lqpici = tdlist[5][1]

		print(" 年份  :",nianfen)
		print(" 最低  :",zuidi)
		print(" 最高  :",zugao)
		print(" 平均  :",pingjun)
		print(" 录取人数  :",lqrenshu)
		print(" 录取批次  :",lqpici)
'''

def runs(url,college_names,college_ids,diqu_key,kemu_key):
	datas1 = get_html(url)
	#print(datas1)
	ul_html = get_ul_html(datas1)
	if ul_html == False:
		return 0
	#print(ul_html)
	trlist = get_tr(ul_html)
	for trhtml in trlist:
		if "td" in trhtml:
			#print(trhtml,"\n")
			tdlist = get_td(trhtml)
			#print(tdlist)
			nianfen = tdlist[0][1]

			zuidi = tdlist[1][1]
			if "-" in zuidi:
				zuidi = ""

			zugao = tdlist[2][1]
			if "-" in zugao:
				zugao = ""

			pingjun = get_a(tdlist[3][1])[0]
			if "-" in pingjun:
				pingjun = ""

			lqrenshu = tdlist[4][1]
			if "-" in lqrenshu:
				lqrenshu = ""
			try:
				lqpici = tdlist[5][1]
			except:
				lqpici = ""
			
			#学校ID    学校   地区  科目  源地址  年份  最低  最高  平均  录取人数   录取批次  
			print(" 学校ID  :",college_ids)
			print(" 学校  :",college_names)
			print(" 地区  :",diqu_key)
			print(" 科目  :",kemu_key)
			print(" 年份  :",nianfen)
			print(" 最低  :",zuidi)
			print(" 最高  :",zugao)
			print(" 平均  :",pingjun)
			print(" 录取人数  :",lqrenshu)
			print(" 录取批次  :",lqpici)
			print(" 源地址  :",url)
			#写入数据到csv
			addlist = [college_ids, college_names, diqu_key, kemu_key, nianfen, zuidi, zugao, pingjun, lqrenshu, lqpici, url]
			print(addlist)
			with open("D:/xuexuao_luquxian_9.csv", 'a', newline='', encoding='utf-8') as f:
				print(" ===>   add ok !!!")
				csv_write = csv.writer(f,dialect='excel')
				csv_write.writerow(addlist)
			print("__________________________________\n")
	set_run(college_ids)




#在大学爬虫表取学校id与学校录取分数链接地址
#print(get_dx_info())
college_list = get_dx_info()

for college in college_list:
	college_names = college["college_names"]
	print(college_names)
	college_ids = college["college_ids"]
	print(college_ids)
	luquurl = college["luqu_url"]
	lqurls = "/".join(luquurl.split("/")[:-3])
	print(lqurls)
	
	#通过遍历的方式爬取数据
	for diqu in diqu_list:
		diqu_key = diqu
		diqu_val = diqu_list[diqu]
		for kemu in kemu_list:
			kemu_key = kemu
			kemu_val = kemu_list[kemu]
			print(diqu_key,kemu_key)
			urls = lqurls+"/"+str(diqu_val)+"/"+str(kemu_val)+"/"
			print(urls)
			runs(urls,college_names,college_ids,diqu_key,kemu_key)



	


