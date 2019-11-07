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




#https://data.p4psearch.1688.com/data/ajax/get_premium_offer_list.json?beginpage=1&asyncreq=1&keywords=%E6%89%8B%E6%9C%BA&sortType=&descendOrder=&province=&city=&priceStart=&priceEnd=&dis=&pageid=28891ebeHwr8ir&p4pid=1560824155735015189348&callback=jsonp_1560824153707_79257&_=1560824153707
#https://data.p4psearch.1688.com/data/ajax/get_premium_offer_list.json?beginpage=1&asyncreq=2&keywords=%E6%89%8B%E6%9C%BA&sortType=&descendOrder=&province=&city=&priceStart=&priceEnd=&dis=&pageid=28891ebeHwr8ir&p4pid=1560824155735015189348&callback=jsonp_1560824153734_66728&_=1560824153734


#https://data.p4psearch.1688.com/data/ajax/get_premium_offer_list.json?beginpage=50&asyncreq=1&keywords=%E6%89%8B%E6%9C%BA&sortType=&descendOrder=&province=&city=&priceStart=&priceEnd=&dis=&pageid=28891ebeHwr8ir&p4pid=1560824155735015189348&callback=jsonp_1560824395679_83517&_=1560824395679


#一页  6个    asyncreq   ： 1~6

#50页     beginpage  ： 1~50






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


#test_url = 'https://data.p4psearch.1688.com/data/ajax/get_premium_offer_list.json?beginpage=1&asyncreq=1&keywords=手机'
#ip_test_url = 'https://www.xicidaili.com/nn/'
#html_data = get_html(test_url)
#print html_data.encode("GBK",'ignore')
#print(html_data)






#print(type(html_data))
#print("\n\n\n\n")


def get_offerResult(html):
    reg = r"\"offerResult\":.*?]"
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

def get_tp(html):
    html = str(html)
    html = html.split("TP")
    return html


#"title":
def get_title(html):
    reg = r"\"title\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

def get_olany_name(html):
    html = str(html)
    dr = re.compile(r'<[^>]+>',re.S)
    dd = dr.sub('',html)
    #print(dd)
    return dd


# eurl
def get_eurl(html):
    reg = r"\"eurl\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data


# imgUrl
def get_imgUrl(html):
    reg = r"\"imgUrl\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#价格  strPriceMoney
def get_strPriceMoney(html):
    reg = r"\"strPriceMoney\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

#bizTypeName   经营类型
def get_bizTypeName(html):
    reg = r"\"bizTypeName\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

# name 
def get_name(html):
    reg = r"\"name\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data

# city
def get_city(html):
    reg = r"\"city\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data


#province
def get_province(html):
    reg = r"\"province\":\"(.*?)\","
    reger = re.compile(reg)
    data = re.findall(reger, html)
    return data


#print(get_tp(html_data))
def run(html_data,kyes,csv_data_file):
	for data1 in get_tp(html_data):
		
		#print(data1)
		if "title" in data1 and "eurl" in data1 and get_title(data1) != []:
			#print(data1)
			#print(get_title(data1))
			'''
			title_val1 = get_title(data1)[0]
			title_val = get_olany_name(title_val1)
			print(" [ Title ] = "+title_val)

			eurl = get_eurl(data1)[0]
			print(" [ eurl ] = "+eurl)

			imgUrl = get_imgUrl(data1)[0]
			print(" [ imgUrl ] = "+imgUrl)

			strPriceMoney = get_strPriceMoney(data1)[0]
			print(" [ strPriceMoney ] = "+strPriceMoney)

			bizTypeName = get_bizTypeName(data1)[0]
			print(" [ bizTypeName ] = "+bizTypeName)

			name = get_name(data1)[1]
			print(" [ 公司名 ] = "+name)

			city = get_city(data1)[0]
			print(" [ city ] = "+city)

			province = get_province(data1)[0]
			print(" [ province ] = "+province)

			print(" [ key ] = "+kyes)

			input_datas = ['1688',kyes,title_val,eurl,imgUrl,strPriceMoney,bizTypeName,name,province,
							city]
			with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
				csv_write = csv.writer(f,dialect='excel')
				csv_write.writerow(input_datas)
			'''
	
			try:
				title_val1 = get_title(data1)[0]
				title_val = get_olany_name(title_val1)
				print(" [ Title ] = "+title_val)

				eurl = get_eurl(data1)[0]
				print(" [ eurl ] = "+eurl)

				imgUrl = get_imgUrl(data1)[0]
				print(" [ imgUrl ] = "+imgUrl)

				strPriceMoney = get_strPriceMoney(data1)[0]
				print(" [ strPriceMoney ] = "+strPriceMoney)

				bizTypeName = get_bizTypeName(data1)[0]
				print(" [ bizTypeName ] = "+bizTypeName)

				name = get_name(data1)[1]
				print(" [ 公司名 ] = "+name)

				city = get_city(data1)[0]
				print(" [ city ] = "+city)

				province = get_province(data1)[0]
				print(" [ province ] = "+province)

				print(" [ key ] = "+kyes)

				input_datas = ['1688',kyes,title_val,eurl,imgUrl,strPriceMoney,bizTypeName,name,province,
								city]
				with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
					csv_write = csv.writer(f,dialect='excel')
					csv_write.writerow(input_datas)
			except:
				print("网络环境异常")
		print("\n\n")


#run(html_data)

'''
https://data.p4psearch.1688.com/data/ajax/get_premium_offer_list.json?beginpage=1&asyncreq=1&keywords=手机&pageid=28891ebeHwr8ir&p4pid=1560824155735015189348

'''




def gorun(keys,csv_data_file):
	pgn=0
	while pgn < 51:
		nnn = 1

		while nnn < 7:
			url = 'https://data.p4psearch.1688.com/data/ajax/get_premium_offer_list.json?beginpage='+str(pgn)+'&asyncreq='+str(nnn)+'&keywords='+keys
			print(url)
			html_data = get_html(url)
			run(html_data,keys,csv_data_file)

			nnn += 1


		pgn += 1





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



txt = """
遮阳网 篷布 防虫网  农业工具 镰刀 锹 高压水枪 锨 镐 耙子 锄头 叉  饲料 猪饲料 羊饲料 牛饲料 预混料 饲料原料 全价料 饲料添加剂 浓缩料  畜牧养殖 加工设备 养殖器械 渔业用具 养殖服务 配种服务 养鸡设备 挤奶机 母猪产床  兽药 化学药 中兽药 抗生素 驱虫 消毒剂 疫苗 阿莫西林 氟苯尼考
"""


task_keys = []
for i in txt.split(" "):
    if i != "":
        #print(i)
        task_keys.append(i)

#print(task_keys)

alllist = set(all_keys+task_keys)
#print(alllist)

csv_data_file = 'D:/1688_01.csv'
#gorun("手机",csv_data_file)

for listdata in task_keys:
	print(listdata)
	gorun(listdata,csv_data_file)