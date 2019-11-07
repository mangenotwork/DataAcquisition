#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'man' 

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

#db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
test_sql = "select user_id,query_count,count_date,query_type from yb_biz_user_query_count;"

'''
yb_biz_user_query_count_data = db_test1.select_data(test_sql)

for user_q_c in yb_biz_user_query_count_data:
	print(user_q_c)
'''
#关联查询   yb_org_user






#select id,company from  yb_biz_company_info

def get_companydata():
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	#get_user_id_sql = "select id,company from  yb_biz_company_info where pic_address is Null LIMIT 391812;"
	get_user_id_sql = "select id,company from  yb_biz_company_info where pic_address = '0';"
	user_id = db_test1.execute_sql(get_user_id_sql)
	#print(user_id)
	return user_id


#查找公司名称
def get_companynames(names):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	#get_user_id_sql = "select id,company from  yb_biz_company_info where pic_address is Null LIMIT 391812;"
	get_user_id_sql = "select id,company from  yb_biz_company_info where company = '"+names+"';"
	user_id = db_test1.execute_sql(get_user_id_sql)
	#print(user_id)
	return user_id

#  pic_address
#updata yb_biz_company_info set pic_address = "aaaa" where user_id ="aaaa";


def set_imgdata(imgurl,ids):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "UPDATE yb_biz_company_info set pic_address = '"+imgurl+"' where id = '"+ids+"';"
	user_query_count_info = db_test1.exect(sql)
	#print(user_query_count_info)
	return user_query_count_info

def get_user_uuid(user_name):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	get_user_id_sql = "select id from yb_org_user where username = '"+user_name+"';"
	user_id = db_test1.execute_sql(get_user_id_sql)
	#print(user_id)
	return user_id



#获取名称   yb_com_shareholder_info
def get_username():
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	get_user_id_sql = "select id,shareholder from yb_com_shareholder_info where imgs is Null LIMIT 0,71986;"
	user_id = db_test1.execute_sql(get_user_id_sql)
	#print(user_id)
	return user_id

#更新姓名图标的url
def set_username(ids,imgurl):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "UPDATE yb_com_shareholder_info set imgs = '"+imgurl+"' where id = '"+ids+"';"
	user_query_count_info = db_test1.exect(sql)
	#print(user_id)
	return user_query_count_info


#更新姓名图标的url
def set_username_test(ids,imgurl,names):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "UPDATE yb_com_shareholder_info set imgs = '"+imgurl+"' where company = '"+names+"' ;"# and id = "+str(ids)+";"
	user_query_count_info = db_test1.exect(sql)
	#print(user_id)
	return user_query_count_info



def get_user_query_count_info(user_uuid):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "select user_id,query_count,count_date,query_type from yb_biz_user_query_count where user_id = '"+user_uuid+"';"
	user_query_count_info = db_test1.execute_sql(sql)
	print(user_query_count_info)

def empty_user_query_count(user_uuid):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "update yb_biz_user_query_count set query_count = 1,query_all_count = 1 where user_id = '"+user_uuid+"';"
	user_query_count_info = db_test1.execute_sql(sql)
	print(user_query_count_info)


def get_cd():
	db_test1 = DB_funtion('118.25.137.1',3306,'manmc','root','liman19950620')
	sql = "select City_CN from china_city_list where length(City_CN) > 6;"
	user_query_count_info = db_test1.execute_sql(sql)
	print(user_query_count_info)
	return user_query_count_info


def empty_user_query_count_number(user_name):
	'''
	try:
		user_id = get_user_uuid(user_name)
		uuid = user_id[0].get('id')
		print(uuid)
		empty_user_query_count(uuid)
	except Exception as e:
		print("[DB Error] ： empty_user_query_count_number  username: "+user_name)
		print(e)
	try:
	'''
	user_id = get_user_uuid(user_name)
	uuid = user_id[0].get('id')
	print(uuid)
	empty_user_query_count(uuid)
	

#empty_user_query_count_number("man_test_001")


#易中标人工智能查询业绩
def yb_AI_Get_project(names):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = """SELECT
	cp.project_name
FROM
	yb_biz_company_perform cp
WHERE
	cp.qy_id IN (
		SELECT DISTINCT
			ci.id
		FROM
			yb_biz_company_info ci
		INNER JOIN yb_biz_perform_classify pc ON pc.qy_id = ci.id
		WHERE
			ci.company = '%s'
	);""" % (names)
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info


#易中标人工智能 项目源地址 url 链接
def yp_AI_Get_project_url(names):
	db_test1 = DB_funtion('192.168.1.52',3306,'perform','root','root')
	sql = """select b.url
from bid_result  a
inner join bid_notice b on a.project_num = b.project_num
where  a.bid_title = '%s'
;""" % (names)
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info

#王板桥灌排渠玉河段项目中标候选人公示


#易中标获取公司名称
def get_company():
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = """SELECT
	company,legal_person,social_credit,company_type,business_address,contacts
FROM
	yb_biz_company_info
where contacts != ""

	LIMIT 100
;"""
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info


def s_company(names):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "SELECT\
			company,legal_person,social_credit,company_type,business_address,contacts \
		FROM \
			yb_biz_company_info \
		where company like '%"+names+"%' \
			LIMIT 100 \
		;"
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info

print(s_company('网络会所'))


#print(get_company())
'''
import csv

csv_data_file = "D:/test1.csv"

for info in get_company():
	print(info)
	datalist = [info["company"],info["legal_person"],info["social_credit"],info["company_type"],info["business_address"],info["contacts"]]
	with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
		csv_write = csv.writer(f,dialect='excel')
		csv_write.writerow(datalist)

'''
#http://www.sccin.com.cn/WebSiteInfo/YellowPages/EnterpriseSearch.aspx?AreaCode=0&Category=APT_008&KeyWords=
#http://www.sccin.com.cn/WebSiteInfo/YellowPages/EnterpriseSearch.aspx?AreaCode=0&Category=APT_008&KeyWords=



#易中标获取公司名称
def get_company_name(name):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = """SELECT
	company,legal_person,social_credit,company_type,business_address,contacts
FROM
	yb_biz_company_info
where company = '%s'
	LIMIT 100
;""" % (name)
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info






#易中标数据有效性验证  全国建筑市场监管
def get_company_info():
	db_test1 = DB_funtion('192.168.1.31',3306,'yibiao','ybData','3532Yibiao!')
	sql = """SELECT id,name
	FROM company_info
;"""
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info



##在测试库通过公司名称查询该公司的总资质数量
#SELECT count(*) FROM yb_biz_company_aptitude cp INNER JOIN yb_biz_company_info ci ON ci.id = cp .qy_id WHERE ci.company = '中交第四公路工程局有限公司'
def get_zz_allnum(company_name):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "SELECT count(*) FROM yb_biz_company_aptitude cp INNER JOIN yb_biz_company_info ci ON ci.id = cp .qy_id WHERE ci.company = '"+company_name+"';"
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info


##在测试库通过公司名称查询该公司的总资质数量
#SELECT count(*) FROM yb_biz_company_aptitude cp INNER JOIN yb_biz_company_info ci ON ci.id = cp .qy_id WHERE ci.company = '中交第四公路工程局有限公司'
def get_zz_allnum1(company_name):
	try:
		db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
		sql = "SELECT count(*) FROM yb_biz_company_aptitude cp INNER JOIN yb_biz_company_info ci ON ci.id = cp .qy_id WHERE ci.company = '"+company_name+"';"
		user_query_count_info = db_test1.execute_sql(sql)
		#print(user_query_count_info)
		return user_query_count_info
	except Exception as e:
		print("wite 3s...")
		time.sleep(3)
		return get_zz_allnum1(company_name)
	





# 在测试库通过公司名称查询该公司的人员资质信息  （资质名称：资质人数）
# SELECT ap.zgmc,COUNT(ap.zgmc) FROM yb_biz_person_aptitude ap INNER JOIN yb_biz_company_info ci ON ap.qy_id = ci.id WHERE ci.company = '中国华西企业有限公司' GROUP BY ap.zgmc
def get_ryzz_allnum(company_name):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "SELECT ap.zgmc,COUNT(ap.zgmc) FROM yb_biz_person_aptitude ap INNER JOIN \
	yb_biz_company_info ci ON ap.qy_id = ci.id WHERE ci.company = '"+company_name+"' GROUP BY ap.zgmc"
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info



# 在测试库通过公司名称查询该公司的人员资质信息  所有人员资质信息
#SELECT COUNT(ap.zgmc) FROM yb_biz_person_aptitude ap INNER JOIN yb_biz_company_info ci ON ap.qy_id = ci.id WHERE ci.company = '中国华西企业有限公司'
def get_ryzz_all(company_name):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "SELECT COUNT(ap.zgmc) FROM yb_biz_person_aptitude ap INNER JOIN \
	yb_biz_company_info ci ON ap.qy_id = ci.id WHERE ci.company = '"+company_name+"';"
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info


# 在测试库通过公司名称查询该公司的人员资质信息  所有人员资质信息
#SELECT COUNT(ap.zgmc) FROM yb_biz_person_aptitude ap INNER JOIN yb_biz_company_info ci ON ap.qy_id = ci.id WHERE ci.company = '中国华西企业有限公司'
def get_ryzz_all1(company_name):
	try:
		db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
		sql = "SELECT COUNT(ap.zgmc) FROM yb_biz_person_aptitude ap INNER JOIN \
		yb_biz_company_info ci ON ap.qy_id = ci.id WHERE ci.company = '"+company_name+"';"
		user_query_count_info = db_test1.execute_sql(sql)
		#print(user_query_count_info)
		return user_query_count_info
	except Exception as e:
		print("wite 3s...")
		time.sleep(3)
		return get_ryzz_all1(company_name)
	





# 在测试库查看该公司的总业绩数
#select count(*) from yb_biz_company_perform where company = '四川大路路桥工程有限公司'
def get_yj_all(company_name):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "select count(*) from yb_biz_company_perform where company = '"+company_name+"';"
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info


# 在测试库查看该公司的总业绩数
#select count(*) from yb_biz_company_perform where company = '四川大路路桥工程有限公司'
def get_yj_all1(company_name):
	try:
		db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
		sql = "select count(*) from yb_biz_company_perform where company = '"+company_name+"';"
		user_query_count_info = db_test1.execute_sql(sql)
		#print(user_query_count_info)
		return user_query_count_info
	except Exception as e:
		print("wite 3s...")
		time.sleep(3)
		return get_yj_all1(company_name)
	




# 在测试库通过公司名称查该公司的所有业绩总数
# select count(*) from yb_biz_company_perform where company = '四川大路路桥工程有限公司'






# 在测试库检查业绩的金额项目负责人为空的数据
'''
select b.bid_time,a.url,a.data_source,b.project_name,a.html_text
from yb_biz_company_perform_html a
inner join yb_biz_company_perform b on a.perform_id = b.id
where b.data_source  in ('全国公共资源交易平台(四川省)','四川省政府政务服务和公共资源交易服务中心','重庆市公共资源交易平台','四川建设网')
and
( ifNull(b.project_manager,'') = ''  or ifNull(b.bid_amount,'') = '' )
LIMIT 10;
'''
def get_null_yeji():
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "select b.bid_time,a.url,a.data_source,b.project_name,a.html_text \
			from yb_biz_company_perform_html a \
			inner join yb_biz_company_perform b on a.perform_id = b.id \
			where b.data_source  in ('全国公共资源交易平台(四川省)','四川省政府政务服务和公共资源交易服务中心','重庆市公共资源交易平台') \
			and \
			( ifNull(b.project_manager,'') = ''  or ifNull(b.bid_amount,'') = '' ) LIMIT 53038;"
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info


#查看QA库 的全国建筑市场监管公共服务平台 企业资质总数
def get_QAtest_qgjzsc_zz():
	db_test1 = DB_funtion('127.0.0.1',3306,'yb_test','root','123')
	sql = "select name,zz_number \
			from qgjzsc_zz \
			where zz_number != 'null' \
			and test is NULL \
			;"
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info


# 添加 的全国建筑市场监管公共服务平台 企业资质总数 对比测试 结果到 QA库
def add_QAtest_qgjzsc_zz(name,yb_33_zz_number, test_r):
	db_test1 = DB_funtion('127.0.0.1',3306,'yb_test','root','123')
	sql = "UPDATE qgjzsc_zz set yb_33_number = "+str(yb_33_zz_number)+",test='"+test_r+"' where name = '"+name+"' ;"
	user_query_count_info = db_test1.exect(sql)
	#print(user_query_count_info)
	return user_query_count_info


# 添加 的全国建筑市场监管公共服务平台 企业资质总数 对比测试 结果到 QA库
def add_QAtest_qgjzsc_zz1(name,yb_33_zz_number, test_r):
	try:
		db_test1 = DB_funtion('127.0.0.1',3306,'yb_test','root','123')
		sql = "UPDATE qgjzsc_zz set yb_33_number = "+str(yb_33_zz_number)+",test='"+test_r+"' where name = '"+name+"' ;"
		user_query_count_info = db_test1.exect(sql)
	except Exception as e:
		print("wite 3s...")
		time.sleep(3)

		return add_QAtest_qgjzsc_zz1(name,yb_33_zz_number, test_r)
	


#查看QA库 的全国建筑市场监管公共服务平台 企业业绩总数
def get_QAtest_qgjzsc_yj():
	db_test1 = DB_funtion('127.0.0.1',3306,'yb_test','root','123')
	sql = "select name,yj_allnumber \
			from qgjzsc_yj \
			where yj_allnumber != '' \
			and test is NULL \
			;"
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info



# 添加 的全国建筑市场监管公共服务平台 企业业绩总数 对比测试 结果到 QA库
def add_QAtest_qgjzsc_yj(name,yb_33_zz_number, test_r):
	try:
		db_test1 = DB_funtion('127.0.0.1',3306,'yb_test','root','123')
		sql = "UPDATE qgjzsc_yj set yb_33_number = "+str(yb_33_zz_number)+",test='"+test_r+"' where name = '"+name+"' ;"
		user_query_count_info = db_test1.exect(sql)
	except Exception as e:
		print("wite 3s...")
		time.sleep(3)

		return add_QAtest_qgjzsc_zz1(name,yb_33_zz_number, test_r)
	


#查看QA库 的全国建筑市场监管公共服务平台 企业人员总数
def get_QAtest_qgjzsc_ryzz():
	db_test1 = DB_funtion('127.0.0.1',3306,'yb_test','root','123')
	sql = "select name,ryzz_info \
			from qgjzsc_ryzz \
			where ryzz_info != 'null' \
			and test is NULL \
			;"
	user_query_count_info = db_test1.execute_sql(sql)
	#print(user_query_count_info)
	return user_query_count_info



# 添加 的全国建筑市场监管公共服务平台 企业业绩总数 对比测试 结果到 QA库
def add_QAtest_qgjzsc_ryzz(name,ryzz_allnumber, yb_33_info, yb_33_zz_number, test_r):
	try:
		db_test1 = DB_funtion('127.0.0.1',3306,'yb_test','root','123')
		sql = "UPDATE qgjzsc_ryzz set ryzz_allnumber = "+ str(ryzz_allnumber) +",  yb_33_info = '"+ str(yb_33_info) +"', yb_33_number = "+str(yb_33_zz_number)+",test='"+test_r+"' where name = '"+name+"' ;"
		user_query_count_info = db_test1.exect(sql)
	except Exception as e:
		print("wite 3s...")
		time.sleep(3)

		return add_QAtest_qgjzsc_zz1(name,ryzz_allnumber, yb_33_info, yb_33_zz_number, test_r)





# **************  人工智能准确性测试  *********************
def fenlei_gourp():
	db_test1 = DB_funtion('127.0.0.1',3306,'yb_test','root','123')
	sql = "SELECT GROUP_CONCAT(fl) as allfl from aitest1 GROUP BY fl;"
	return db_test1.execute_sql(sql)


def fenlei_info():
	db_test1 = DB_funtion('127.0.0.1',3306,'yb_test','root','123')
	sql = "SELECT * from ai_33;"
	return db_test1.execute_sql(sql)



def get_gjc(fldata):
	db_test1 = DB_funtion('127.0.0.1',3306,'yb_test','root','123')
	sql = "SELECT gjc from c2 where cid = "+fldata+";"
	return db_test1.execute_sql(sql)


def fenlei_vaule(fldata):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "SELECT * from dict_perform_classify \
		where class1='"+fldata+"' \
		or class2='"+fldata+"' \
		or class3='"+fldata+"' \
		or class4='"+fldata+"' \
		or class5='"+fldata+"' "
	return db_test1.execute_sql(sql)


#获取中标公示
def get_zbgs(pid):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "SELECT construction_method from yb_biz_perform_classify where  perform_id = '"+pid+"';"
	return db_test1.execute_sql(sql)


#获取该分类编号的项目
def get_all_poj(flval):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "SELECT perform_id from yb_biz_perform_classify \
	where value="+flval+" and data_source in ('全国公共资源交易平台(四川省)','四川建设网','四川省政府政务服务和公共资源交易服务中心') ;"
	return db_test1.execute_sql(sql)

#获取该项目编号的公示信息
def get_gs_info(pojid):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "select b.title,b.company,a.data_source,b.content,a.value from yb_biz_perform_classify a inner join yb_biz_bid_result  b \
	on a.qy_id= b.qy_id where a.perform_id = '"+pojid+"' ;"
	return db_test1.execute_sql(sql)

#判断项目是否通过人工智能分类
def ai_yesno(pojid):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "SELECT count(*) from yb_biz_perform_classify p \
	join dict_perform_classify c \
	on p.value= c.value \
	where data_source in ('全国公共资源交易平台(四川省)','四川建设网','四川省政府政务服务和公共资源交易服务中心')\
	and perform_id = '"+pojid+"';"
	if db_test1.execute_sql(sql)[0]['count(*)'] > 0:
		return True
	else:
		return False

def get33_fenlei(flval):
	db_test1 = DB_funtion('192.168.1.33',3306,'yibiao','ybData','3532Yibiao!')
	sql = "select * from dict_perform_classify where value='"+flval+"'"
	return db_test1.execute_sql(sql)


#return pymysql.Connect(host='192.168.1.31',port=3306,db=db_name,user='ybData',passwd='3532Yibiao!',charset='utf8',cursorclass = pymysql.cursors.DictCursor)

def test_debug_1():
    db_test1 = DB_funtion('192.168.1.31',3306,'yibiao','ybData','3532Yibiao!')
    sql = '''
            select 
                ifNull(a.name,'') person_name,
                ifNull(c.name,'') as company_name,
                b.certificates
            from company_person_info a
            inner join company_info c on a.company_id = c.id
            inner join person_info b on a.id = b.id
            where b.certificates  <> ''
            and  c.name like '四川大路路桥%' and a.name ='罗章春'   
        '''
    return db_test1.execute_sql(sql)    




#aa = test_debug_1()
#print(aa)



def get_original_to_repeat_list():
        db_test1 = DB_funtion('192.168.1.31',3306,'yibiao','ybData','3532Yibiao!')
        results = db_test1.execute_sql('''
            select 
                ifNull(a.name,'') person_name,
                ifNull(c.name,'') as company_name,
                b.certificates
            from company_person_info a
            inner join company_info c on a.company_id = c.id
            inner join person_info b on a.id = b.id
            where b.certificates  <> ''
            and  c.name like '四川大路路桥%' and a.name ='罗章春'   
        ''')
        #results = cursor_31.fetchall()
        
        print("[DEBUG] 获取记录数：",len(results))
        
        for row in results:

            #1先获取人员id
            company_name = wash_fun.wash_company_name(row['company_name'])
            person_name = wash_fun.wash_person_name(row['person_name'])
            key_str = company_name + '^' + person_name

            if company_name == '':
                continue
            
            if person_name == '':
                continue
            
            if key_str not in self.person_id_mapping and "" in [company_name,person_name]:
                print("有证书无法匹配人员：", key_str, "原字符串\n:", row)
                continue
            person_id = key_str
            print("[company_name] == " +company_name)
            print("[person_name] == " +person_name)
            print("[key_str] == " +key_str)
            print("[person_id] == " +person_id)
            '''
            #开始处理证书信息
            certificates = row['certificates']
            #开始处理证书
            certificates = certificates.replace(' ','')
            print("###################################################")
            print(certificates)
            for one_cert_str in certificates.split("#;#"):
                #开始处理每一个证书相关信息
                print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
                print(one_cert_str)

                apt_num  = ''
                expiry_date = ''
                profession =''
                seal_num = ''
                apt_type = ''

                #检查每一个字段
                for one_field in one_cert_str.split("#*#"):
                    if "#:#" not in one_field:
                        continue
                    key = one_field.split("#:#")[0]
                    value = one_field.split("#:#")[1]
                    #print(key,':',value) 
                    if key == '注册单位':
                        apt_company_name = value
                    if key == '注册类别':
                        apt_type = value
                    if key == '证书编号':
                        apt_num = value
                    if key == '执业印章号':
                        seal_num = value
                    if key == '注册专业':
                        profession = value
                    if key == '有效期':
                        expiry_date = value
                    if not key in ['注册单位','注册类别','证书编号','执业印章号','注册类别','注册专业','有效期']:
                        print(key,':',value)


                # 处理有效期
                expiry_end = expiry_date.replace('年', '-')
                expiry_end = expiry_end.replace('月', '-')
                expiry_end = expiry_end.replace('日', '')


                #处理等级,级别在字符串之前
                level_name = '不分等级'
                if '建造师' in apt_type or '建筑师' in apt_type or '结构工程师' in apt_type:
                    for sub in ['二级临时','一级临时','二级','一级']:
                        if apt_type.startswith(sub):
                            apt_type = apt_type.replace(sub,'')
                            level_name = sub
                            break

                if level_name not in self.level_alias_mapping:
                    print("发现无效等级：",level_name,"/",one_cert_str)
                    continue
                level_id = self.level_alias_mapping[level_name]


                #处理证书类别字典
                alias = apt_type+"^"+profession
                if alias not in self.first_mapping:
                    # 收集非规范证书
                    self.un_match.add((apt_type, profession,''))
                    continue
                cert_dict_id = self.first_mapping[alias]

                #添加进集合
                self.repeat_obj_list.append(PersonCert({
                    'cert_dict_id':cert_dict_id,
                    'person_id':person_id,
                    'level_id':level_id,
                    'cert_num':apt_num,
                    'registered_num':seal_num,
                    'expiry_end':expiry_end
                }))
            '''


#get_original_to_repeat_list()