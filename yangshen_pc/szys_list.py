#图片下载
import urllib
import requests
import time,re,os,sys,random
import datetime
import urllib.request
import urllib.error

from urllib.request import urlopen

import mandb

import csv

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



#插入数据
@ManDB
def add_sql(man_db,szys_id, title, imgpath, fenlei, ysdate, pl_count, ck_count, datatype):
    sql ="INSERT INTO szys_list ( szys_id, title, imgpath, fenlei, ysdate, pl_count, ck_count, datatype) \
    VALUES ( '"+szys_id+"', '"+title+"', '"+imgpath+"', '"+fenlei+"', '"+ysdate+"', "+str(pl_count)+", "+str(ck_count)+", '"+datatype+"');"

    #print(sql)

    a = man_db.execute1(sql)
    print(" [ *** 添加新数据 *** ] ")








def get_rsc(pgnumber):
	while True:
		try:
			man_db = mandb.DB()
			sql = "\
			select sydata_id,title,fenlei from sydata_dzys where fenlei = '人群' LIMIT "+str(pgnumber*100)+",100;\
			"
			return_datas = man_db.execute_seles1(sql)
			if return_datas != False:
				return return_datas
		except Exception as e:
			print("link Error")
		
		



def get_rsc1(pgnumber):
    try:
        man_db = mandb.DB()
        sql = "\
        select sydata_id,title,fenlei from sydata_dzys where fenlei = '人群' LIMIT "+str(pgnumber*100)+",100;\
        "
        return_datas = man_db.execute_seles1(sql)
        return return_datas
    except Exception as e:
        return ""
    




def get_allcount():
	while True:
	    man_db = mandb.DB()
	    sql = "\
	        select count(sydata_id) from sydata_dzys where fenlei = '人群' ;\
	    "
	    return_datas = man_db.execute_seles1(sql)
	    if return_datas != False:
	    	return return_datas[0][0]



#天天养生数据获取    一天20个
def get_ttys_data(pgnumber):
	while True:
		try:
			man_db = mandb.DB()
			sql = "\
				select tt.sydata_id, tt.fenlei, GROUP_CONCAT(ti.imgpath SEPARATOR '|') as link, tt.title \
				from sydata_ttys tt INNER JOIN sydata_ttys_imgs ti ON tt.sydata_id=substring(ti.sydata_id,5) \
				where tt.fenlei = '养生食谱' \
				GROUP BY tt.sydata_id \
				LIMIT "+str(int(pgnumber)*20)+",20;"
			return_datas = man_db.execute_seles1(sql)
			if return_datas != False:
				return return_datas
		except Exception as e:
			print("link Error")
			get_ttys_data(pgnumber)



#天天养生数据获取    一天20个
def get_ttys_data1(pgnumber):
	print(pgnumber)
	print(type(pgnumber))
	pgnumber = pgnumber*20
	man_db = mandb.DB()
	sql = "\
		select tt.sydata_id, tt.fenlei, GROUP_CONCAT(ti.imgpath SEPARATOR '|') as link, tt.title \
		from sydata_ttys tt INNER JOIN sydata_ttys_imgs ti ON tt.sydata_id=substring(ti.sydata_id,5) \
		where tt.fenlei = '营养科普' \
		GROUP BY tt.sydata_id LIMIT "+str(pgnumber)+",20; "
	return_datas = man_db.execute_seles1(sql)
	if return_datas != False:
		return return_datas


#天天养生总条数
def get_allcount_ttys():
	while True:
	    man_db = mandb.DB()
	    sql = "\
	        select count(sydata_id) from sydata_ttys where fenlei = '养生食谱' ;\
	    "
	    return_datas = man_db.execute_seles1(sql)
	    if return_datas != False:
	    	return return_datas[0][0]



niannum =  int((get_allcount_ttys()/20)+1)
print(niannum)


'''

'''



import time
import datetime
import random

#天数递增
def time_increase(begin_time,days):
	ts = time.strptime(str(begin_time),"%Y-%m-%d")
	ts = time.mktime(ts)
	dateArray = datetime.datetime.utcfromtimestamp(ts)
	date_increase = (dateArray+datetime.timedelta(days=days)).strftime("%Y-%m-%d")
	print("日期：{}".format(date_increase))
	return  date_increase




csv_data_file = "F:/szyslist-ttys-2.csv"


n=1
while n<=niannum:
	datas = time_increase('2018-10-14',n)
	datalist = get_ttys_data(n-1)
	if datalist!="":
		for datainfo in datalist:
			print(datainfo)
			ids = "tt_"+str(datainfo[0])
			print(ids)
			title = datainfo[1]
			print(title)
			if datainfo[3] == "":
				imgpath = "0"
			else:
				imgpath = datainfo[3]
			print(imgpath)
			fenlei = datainfo[2]
			pl = 0
			ck = random.randint(1, 1000)
			datatype = "tt"

			#插入数据
			#add_sql(ids,title,imgpath,fenlei,datas,pl,ck,datatype)

			input_datas = [ids,title,imgpath,fenlei,str(datas),pl,ck,datatype]

			with open(csv_data_file, 'a', newline='', encoding='utf-8') as f:
				csv_write = csv.writer(f,dialect='excel')
				csv_write.writerow(input_datas)

			print("\n")
			
		n+=1
		time.sleep(2)
	else:
		print("db timeout")





