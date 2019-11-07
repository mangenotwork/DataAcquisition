# -*- coding:utf8 -*-
#encoding = utf-8


import pymysql
import time

def db_test():
	return "db init funtion"

DB_name = "syjy"
user_name = "root"
password = 'liman19950620'

Host_2 = "132.232.191.141"
DB_port = 3309
DB_name_2 = 'mange_db1'

password2 = 'lm123456'


#是否要在 HTML 显示页上显示信息，
#True 要显示 （不能用于生产环境，非 json）， 
#False 不在html上返回 只返回数据信息（返回json用）
#HTML_DEBUG = True
HTML_DEBUG = False

# call funtion
def db_debug_call_funtion(func):
    def wrapper(*args, **kwargs):
        print("[Debug] Call funtion < "+func.__name__+" > .")
        return func(*args, **kwargs)
    return wrapper



class DB():
	@db_debug_call_funtion
	def __init__(self, db_host=Host_2, db_port=DB_port, db_name=DB_name_2, user_acc=user_name, user_psd=password2):
		#打印创建对象的时间,目的是后面性能判断
		print("[CREATE Obj Time] :"+str(time.time()))
		self.con = pymysql.connect(host=db_host,port=int(db_port),user=user_acc,passwd=user_psd,db=db_name)
		self.cursor = self.con.cursor()
		
	@db_debug_call_funtion
	def __del__(self):
		#当对象被销毁时 断开数据连接
		self.cursor.close()
		self.con.close()
		#当对象被销毁时，打印被销毁的时间，目的是后面性能判断
		print("[Del Obj Time] :"+str(time.time()))

	def test(self):
		print("Man DB Test.")

	@db_debug_call_funtion
	def db_connect(self):
		pymysql.connect(host="132.232.191.141",port=3309,user=user_name,passwd=password,db=DB_name)
		return "connect succeed."



	'''
			# execute_sql()
			# 执行sql
	'''	
	@db_debug_call_funtion
	def execute_sql(self,sql):
		try:
			self.cursor.execute(sql)
			self.con.commit()
			
			rest_data = self.cursor.fetchall()
			if(HTML_DEBUG):
				return "<h1>"+rest_data+"</h1><br>"
			else:
				return rest_data
		except Exception as e:
			self.con.rollback()
			if(HTML_DEBUG):
				error_sql = "<h1>[SQL Error] "+str(sql)+"</h1><br>"

				error=error_sql + str(e)
				print(error)
				return error
			else:
				return e

	@db_debug_call_funtion
	def db_init_table(self,sql):
		print("db_init_table()")
		try:
			print("start db_init_table()")
			self.cursor.execute(sql)
			self.con.commit()
			if(HTML_DEBUG):
				return "<h1>CREATE user_table ok!</h1><br>"
			else:
				return "CREATE user_table ok!"
		except Exception as e:
			if(HTML_DEBUG):
				error_info = "<h1>[DB Error] CREATE user_table fail</h1><br>"
				error=error_info + str(e)
				return error
			else:
				return e


	'''
			# execute_sql()
			# 执行sql
	'''	
	@db_debug_call_funtion
	def execute(self,sql):
		self.con.ping(reconnect=True)
		self.cursor.execute(sql)
		self.con.commit()

	@db_debug_call_funtion
	def execute_seles(self,sql):
		self.con.ping(reconnect=True)
		self.cursor.execute(sql)
		self.con.commit()	
		rest_data = self.cursor.fetchall()
		
		
		return rest_data
	
	@db_debug_call_funtion
	def execute1(self,sql):
		try:
			self.con.ping(reconnect=True)
			self.cursor.execute(sql)
			self.con.commit()
		except Exception as e:
			return False
		

	@db_debug_call_funtion
	def execute_seles1(self,sql):
		try:
			self.con.ping(reconnect=True)
			self.cursor.execute(sql)
			self.con.commit()	
			rest_data = self.cursor.fetchall()
			return rest_data
		except Exception as e:
			return False
		