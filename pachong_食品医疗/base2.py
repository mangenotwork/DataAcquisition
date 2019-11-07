#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'man'

'''
	@ 业绩通  selenium 的一些基本定位方法

'''

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

class YJT_test():
	def __init__(self):
		self.chromedriver = chromedriver_EXE_path
		os.environ["webdriver.chrome.driver"] = self.chromedriver
		self.browser = webdriver.Chrome(self.chromedriver)
		#self.wait = WebDriverWait(self.browser, 30)

	def open_web(self):
		self.browser = webdriver.Chrome(self.chromedriver)
		#self.wait = WebDriverWait(self.browser, 30)

	#打开网页
	def open_url(self,urls):
		self.browser.get(urls)
		time.sleep(1)
		self.browser.maximize_window()
		time.sleep(1)

	'''
		打开 并登录 业绩通
		open_yejitong(acc_user,acc_pass)
		@ acc_user  账号
		@ acc_pass  密码
	'''
	def open_yejitong(self,acc_user,acc_pass):
		yjt_33 = "http://192.168.1.33:8888/#/userlogin"
		yjt_123 = "http://192.168.2.123:8001/#/userlogin"
		yibiao_login = yjt_33
		self.browser.get(yibiao_login)
		time.sleep(1)
		self.browser.maximize_window()
		time.sleep(1)
		#账户密码输入框定位id
		input_userName_id = "userName"
		input_passWord_id = "passWord"

		#等待  账号 密码输入框加载成功
		for i in range(10):
			try:
				name_id = self.browser.find_element_by_id(input_userName_id)
				password_id = self.browser.find_element_by_id(input_passWord_id)
				if name_id.is_displayed() and password_id.is_displayed():
					break
			except:
				pass
			time.sleep(1)
		else:
			print(query_data+"Time out")
			os.exit()



		# 输入账号密码操作
		try:
			self.browser.find_element_by_id(input_userName_id).send_keys(acc_user)
			time.sleep(1)
			self.browser.find_element_by_id(input_passWord_id).send_keys(acc_pass)
			time.sleep(1)
			#browser.find_element_by_xpath("//button[@class='ant-btn ant-btn-primary ant-btn-lg']/span[text()='登 录']").click()
			time.sleep(1)
			self.browser.find_element_by_xpath("//div//button[@type='button']").click()
			print("[Info] 登录操作完成 !")
		except:
			print("[Error] userName and passWord error!")
			return False

		#进入业绩通首页 关闭广告
		time.sleep(3)
		#close___2Ie9H
		#close___2N0oj
		#close___2N0oj
		#close___2Ie9H
		try:
			self.browser.find_element_by_xpath("//div[@class='close___2Ie9H']").click()
			print("[Info] 关闭了广告 !")
			return True
		except:
			self.browser.find_element_by_xpath("//div[@class='close___2N0oj']").click()
			print("[Info] 关闭了广告 !")
			return True
		

	#
	def open_yejitong2(self,acc_user,acc_pass):
		yjt_33 = "http://192.168.1.33:8888/#/userlogin"
		yjt_123 = "http://192.168.2.123:8001/#/userlogin"
		yibiao_login = yjt_33
		self.browser.get(yibiao_login)
		time.sleep(1)
		self.browser.maximize_window()
		time.sleep(1)
		#账户密码输入框定位id
		input_userName_id = "userName"
		input_passWord_id = "passWord"

		#等待  账号 密码输入框加载成功
		for i in range(10):
			try:
				name_id = self.browser.find_element_by_id(input_userName_id)
				password_id = self.browser.find_element_by_id(input_passWord_id)
				if name_id.is_displayed() and password_id.is_displayed():
					break
			except:
				pass
			time.sleep(1)
		else:
			print(query_data+"Time out")
			os.exit()

		# 输入账号密码操作
		try:
			self.browser.find_element_by_id(input_userName_id).send_keys(acc_user)
			time.sleep(1)
			self.browser.find_element_by_id(input_passWord_id).send_keys(acc_pass)
			time.sleep(1)
			#browser.find_element_by_xpath("//button[@class='ant-btn ant-btn-primary ant-btn-lg']/span[text()='登 录']").click()
			time.sleep(1)
			self.browser.find_element_by_xpath("//div//button[@type='button']").click()
			print("[Info] 登录操作完成 !")
		except:
			print("[Error] userName and passWord error!")
			return False
		


	def open_yejitong123(self,acc_user,acc_pass):
		yjt_123 = "http://192.168.2.139:8081/#/userlogin"
		yibiao_login = yjt_123
		self.browser.get(yibiao_login)
		time.sleep(1)
		self.browser.maximize_window()
		time.sleep(1)
		#账户密码输入框定位id
		input_userName_id = "userName"
		input_passWord_id = "passWord"
		#等待  账号 密码输入框加载成功
		for i in range(10):
			try:
				name_id = self.browser.find_element_by_id(input_userName_id)
				password_id = self.browser.find_element_by_id(input_passWord_id)
				if name_id.is_displayed() and password_id.is_displayed():
					break
			except:
				pass
			time.sleep(1)
		else:
			print(query_data+"Time out")
			os.exit()
		# 输入账号密码操作
		try:
			self.browser.find_element_by_id(input_userName_id).send_keys(acc_user)
			time.sleep(1)
			self.browser.find_element_by_id(input_passWord_id).send_keys(acc_pass)
			time.sleep(1)
			#browser.find_element_by_xpath("//button[@class='ant-btn ant-btn-primary ant-btn-lg']/span[text()='登 录']").click()
			time.sleep(1)
			self.browser.find_element_by_xpath("//div//button[@type='button']").click()
			print("[Info] 登录操作完成 !")
		except:
			print("[Error] userName and passWord error!")
			return False




	
	'''
			关闭浏览器

	'''
	def close_browser(self):
		self.browser.quit()

	#点击的通用方法
	def click_public_1(self,xpathdata):
		self.browser.find_element_by_xpath(xpathdata).click()

	#输入的通用方法
	def input_public_1(self,xpathdata,inputdata):
		self.browser.find_element_by_xpath(xpathdata).send_keys(inputdata)

	#获取txt 通用方法1
	def get_txt_public_xpath(self,xpathdata):
		txt_result = self.browser.find_element_by_xpath(xpathdata).text
		#print(txt_result)
		return txt_result

	#获取txt 通用方法1
	def get_txt_public_id(self,iddata):
		txt_result = self.browser.find_element_by_id(iddata).text
		#print(txt_result)
		return txt_result

	'''
		点击打开 VIP专享查询页面
		open_vip_pg()
	'''
	def open_vip_pg(self):
		try:
			time.sleep(0.5)
			#<a href="#/vipQuery">
			self.browser.find_element_by_xpath("//a[@href='#/vipQuery']").click()
			print("[Info] 点击VIP专享 进入查询页面 !")
		except Exception as e:
			print("[Error] open_vip_pg() fail")
	


	'''
		点击打开 免费分类查询页面
		open_free_pg()
	'''
	def open_free_pg(self):
		try:
			time.sleep(0.5)
			#<a href="#/vipQuery">
			self.browser.find_element_by_xpath("//a[@href='#/ClassQuery']").click()
			print("[Info] 点击免费分类 进入查询页面 !")
		except Exception as e:
			print("[Error] open_vip_pg() fail")

	

	'''
		置顶截图功能
		screenshot_top(save_path)
		@save_path  截图存储路径
	'''
	def screenshot_top(self,save_path):
		self.browser.execute_script("""
			(function () {
			 window.scroll(0, 0);
	        })();
			""")
		time.sleep(0.5)
		self.browser.get_screenshot_as_file(save_path)

	'''
		企业要求 点击方法 
		qiyeyaoqiu(type_vlue)
		@ 1. "全部"
		@ 2. "川内和入川"
		@ 3. "川内州市"

	'''
	def qiyeyaoqiu(self,type_vlue):
		if(type_vlue == "全部"):
			#点击企业要求 【全部】
			#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/div/span/div[1]/div/div[1]/label/span[2]
			#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/div/span/div[1]/div/div[1]/label/span[2]
			#新系统
			#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[1]/div/span/div[1]/div/div[1]/label/span[2]
			try:
				self.browser.find_element_by_xpath("//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/div/span/div[1]/div/div[1]").click()
				#									          /div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/div/span/div[1]/div/div[1]/label/span[2]
			except:
				self.browser.find_element_by_xpath("//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[1]/div/span/div[1]/div/div[1]").click()
			print("[Info] 点击企业要求 全部选项 !")
		elif(type_vlue == "川内和入川"):
			#点击企业要求 【川内和入川】
			#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/div/span/div[1]/div/div[2]/label/span[2]
			try:
				self.browser.find_element_by_xpath("//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/div/span/div[1]/div/div[2]").click()	
			except:
				self.browser.find_element_by_xpath("//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[1]/div/span/div[1]/div/div[2]").click()	
			print("[Info] 点击企业要求 川内和入川选项 !")
		elif(type_vlue == "川内州市"):
			#点击企业要求 【川内州市】
			#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/div/span/div[1]/div/div[2]/label/span[2]
			try:
				self.browser.find_element_by_xpath("//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/div/span/div[1]/div/div[3]").click()	
			except:
				self.browser.find_element_by_xpath("//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[1]/div/span/div[1]/div/div[3]").click()		
			print("[Info] 点击企业要求 川内州市选项 !")



	'''
		企业筛选 第一栏选择的方法
		qiye_query_1(query_data)
		@query_data 条件内容
	'''
	def qiye_query_1(self,query_data):
		# 3. 点击企业筛选 下拉框1 
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div[3]/div
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div
		click_query_1_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div[1]"
		click_query_1_2 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div"
		click_query_1_new = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div"

		click_query_1_list = []
		click_query_1_list.append(click_query_1_1)
		click_query_1_list.append(click_query_1_2)
		click_query_1_list.append(click_query_1_new)

		for click_query_1 in click_query_1_list:
			try:
				self.browser.find_element_by_xpath(click_query_1).click()
				break;
			except:
				continue;

		time.sleep(0.5)
		#//*[@id="lx"]
		self.browser.find_element_by_xpath("//*[@id='lx']").send_keys(query_data)
		self.browser.find_element_by_xpath("//*[@id='lx']").send_keys(Keys.ENTER)
		print("[Info] 企业筛选 第一栏选择 : "+query_data)


	'''
		企业筛选 第二栏选择的方法
		qiye_query_2(query_data)
		@query_data 条件内容
	'''
	def qiye_query_2(self,query_data):
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]  新系统
		click_query_2_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div"
		click_query_2_2 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div"

		click_query_2_list = []
		click_query_2_list.append(click_query_2_1)
		click_query_2_list.append(click_query_2_2)

		for click_query_2 in click_query_2_list:
			try:
				self.browser.find_element_by_xpath(click_query_2).click()
				break;
			except:
				continue;
		
		time.sleep(0.5)
		try:
			#//*[@id="qydj"]
			self.browser.find_element_by_xpath("//*[@id='qydj']").send_keys(query_data)
			self.browser.find_element_by_xpath("//*[@id='qydj']").send_keys(Keys.ENTER)
		except:
			#//*[@id="dl"]
			self.browser.find_element_by_xpath("//*[@id='dl']").send_keys(query_data)
			self.browser.find_element_by_xpath("//*[@id='dl']").send_keys(Keys.ENTER)
		print("[Info] 企业筛选 第二栏选择 : "+query_data)
	

	'''
		企业筛选 第三栏选择的方法
		qiye_query_3(query_data)
		@query_data 条件内容
	'''
	def qiye_query_3(self,query_data):
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div//*[@id="xl"]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[4]/div/div/div/div[2]/div
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]
		#//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div   新		
		click_query_3_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div"
		click_query_3_2 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div"

		click_query_3_list = []
		click_query_3_list.append(click_query_3_1)
		click_query_3_list.append(click_query_3_2)

		for click_query_3 in click_query_3_list:
			try:
				self.browser.find_element_by_xpath(click_query_3).click()
				break;
			except:
				continue;
		
		time.sleep(0.5)
		#//*[@id="xl"]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div//*[@id="xl"]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div
		input_query_3_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div//*[@id='xl']"
		#//*[@id="qydj"]
		input_query_3_2 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div//*[@id='qydj']"
		

		input_query_3_list = []
		#input_query_3_list.append(input_query_3_1)
		input_query_3_list.append(click_query_3_2)
		for input_query_3 in input_query_3_list:
			try:
				self.browser.find_element_by_xpath(input_query_3).send_keys(query_data)
				time.sleep(1)
				self.browser.find_element_by_xpath(input_query_3).send_keys(Keys.ENTER)
				break;
			except:
				continue;

		
		print("[Info] 企业筛选 第三栏选择 : "+query_data)
	

	'''
		企业筛选 第四栏选择的方法
		qiye_query_4(query_data)
		@query_data 条件内容
	'''
	def qiye_query_4(self,query_data):
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[4]/div/div/div
		click_query_4 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[4]/div/div"
		self.browser.find_element_by_xpath(click_query_4).click()
		time.sleep(0.5)
		#//*[@id="zy"]
		self.browser.find_element_by_xpath("//*[@id='zy']").send_keys(query_data)
		self.browser.find_element_by_xpath("//*[@id='zy']").send_keys(Keys.ENTER)
		print("[Info] 企业筛选 第四栏选择 : "+query_data)


	'''
		企业筛选 第五栏选择的方法
		qiye_query_5(query_data)
		@query_data 条件内容
	'''
	def qiye_query_5(self,query_data):
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[5]/div/div/div
		qiye_query_5 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[5]/div/div"
		self.browser.find_element_by_xpath(qiye_query_5).click()
		time.sleep(0.5)
		#//*[@id="qydj"]
		self.browser.find_element_by_xpath("//*[@id='qydj']").send_keys(query_data)
		self.browser.find_element_by_xpath("//*[@id='qydj']").send_keys(Keys.ENTER)
		print("[Info] 企业筛选 第五栏选择 : "+query_data)



	'''
		企业筛选 添加查询 方法
		qiye_query_add()
		@input_number  当前添加了多少个 企业筛选 查询条件
	'''
	def qiye_query_add(self,input_number):
		time.sleep(0.5)
		#添加查询条件
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/button
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[6]/button
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/button 新
		#query_add_xp_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/button"
		#query_add_xp_2 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[6]/button"
		query_add_xp = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div["+str(input_number+1)+"]/button"
		query_add_xp_new = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div["+str(input_number+1)+"]/button"

		try:
			self.browser.find_element_by_xpath(query_add_xp).click()
		except:
			self.browser.find_element_by_xpath(query_add_xp_new).click()
		
		print("[Info]  企业筛选 点击 添加条件.")


	def qyzz_query_0606(self):
		time.sleep(1)
		query_add_xp = "//button[@data-title='企业筛选']"
		self.browser.find_element_by_xpath(query_add_xp).click()
		print("[Info]  企业筛选 点击 添加条件.")

	'''
		获取 企业筛选 添加查询 后显示的内容
		
	'''
	def get_qiye_query_data(self):

		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[3]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/ul
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/ul
		query_data_xp = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/ul"
		query_data_xp_new = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/ul"

		try:
			query_result = self.browser.find_element_by_xpath(query_data_xp).text
		except:
			query_result = self.browser.find_element_by_xpath(query_data_xp_new).text
		print("\n"+query_result+"\n")
		if(query_result == ''):
			return False
		return query_result

	'''
		删除 添加的企业筛选查询条件
	'''

	def remove_qiye_query(self):
		#//*[@id="企业筛选_1553509750768_false"]/div[2]/div
		#//*[@id="企业筛选_1553509761586_false"]/div[2]/div
		remove_query_xp = "//*[@class='close___2_1oC']"
		self.browser.find_element_by_xpath(remove_query_xp).click()
		print("[Info]  点击 删除 添加的企业筛选查询条件.")


	'''
		监听是否有查询到  设置 40s time out
	'''
	def Listening_vip_query_result(self):
		i = 1
		while i<35:
			#result___2YCFR
			#result___Z9VFb
			#searchBtns___pcgzV
			#result___2YCFR
			#result___Z9VFb
			#result___Z9VFb
			
			try:
				result_data = self.browser.find_element_by_xpath("//div[@class='result___2YCFR']/p").text
			except:
				result_data = self.browser.find_element_by_xpath("//div[@class='result___Z9VFb']/p").text


			if(result_data == "查询结果（总共 0 条）"):
				print("Not Listening query result.")
			else:
				print("Matched to query result. time:"+str(i))
				return i
				break;
			time.sleep(1)
			i+=1
			print("[Listening_vip_query_result]:"+str(i))
		return False


	'''	
		点击查询
	'''
	def vip_query_go(self):
		#点击【立即查询】
		#//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[4]/button
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[4]/button
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[4]/button
		vip_query_button_old = "//div[@class='searchBtns___pcgzV']"
		vip_query_button_new = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[4]/button"

		vip_query_button_list = []
		vip_query_button_list.append(vip_query_button_old)
		vip_query_button_list.append(vip_query_button_new)
		for vip_query_button in vip_query_button_list:
			try:
				time.sleep(0.5)
				self.browser.find_element_by_xpath(vip_query_button).click()
				break;
			except:
				continue;
		'''
		#searchBtns___pcgzV
		try:
			self.browser.find_element_by_xpath(vip_query_button_old).click()
		except:
			self.browser.find_element_by_xpath(vip_query_button_new).click()
		print("[Info]  点击 了 立即查询.")
		'''
	

	def vip_query_go2(self):
		#searchBtns___pcgzV
		#vip_query_button = "//div[@class='searchBtns___pcgzV']/button"
		vip_query_button = "//div[@class='searchBtns___2I0DI']/button"
		self.browser.find_element_by_xpath(vip_query_button).click()
		print("[Info]  点击 了 立即查询.")
		

	'''
			查询的结果条数

	'''
	def get_vip_query_result(self):
		time.sleep(0.5)
		try:
			query_result = self.browser.find_element_by_xpath("//div[@class='result___2YCFR']/p").text
		except:
			query_result = self.browser.find_element_by_xpath("//div[@class='result___Z9VFb']/p").text
		
		print(query_result)
		return query_result

	'''
		刷新页面
	'''
	def f5(self):
		self.browser.refresh() #刷新页面
		print('刷新页面')


	'''
		进入新系统

	'''
	def go_new_vip_pg(self):
		js = "window.scrollTo(0,0)"
		self.browser.execute_script(js)
		time.sleep(0.1)
		#//*[@id="root"]/div/div[1]/div[1]/a
		self.browser.find_element_by_xpath("//*[@id='root']/div/div[1]/div[1]/a").click()
		print("[Info]  进入新系统.")


	'''
			进入 12.168.1.79:8081
			http://192.168.1.79:8081
	'''
	def go_79_pg(self):
		js = 'window.open("http://192.168.1.79:8081/#/userlogin");'
		self.browser.execute_script(js)
		


	def login_79(self,acc_user,acc_pass):
		time.sleep(3)
		#账户密码输入框定位id
		input_userName_id = "userName"
		input_passWord_id = "passWord"

		#等待  账号 密码输入框加载成功
		for i in range(10):
			try:
				name_id = self.browser.find_element_by_id(input_userName_id)
				password_id = self.browser.find_element_by_id(input_passWord_id)
				if name_id.is_displayed() and password_id.is_displayed():
					break
			except:
				pass
			time.sleep(1)
		else:
			print(query_data+"Time out")
			os.exit()

		# 输入账号密码操作
		try:
			self.browser.find_element_by_id(input_userName_id).send_keys(acc_user)
			time.sleep(1)
			self.browser.find_element_by_id(input_passWord_id).send_keys(acc_pass)
			time.sleep(1)
			#browser.find_element_by_xpath("//button[@class='ant-btn ant-btn-primary ant-btn-lg']/span[text()='登 录']").click()
			time.sleep(1)
			self.browser.find_element_by_xpath("//div//button[@type='button']").click()
			print("[Info] 登录操作完成 !")
		except:
			print("[Error] userName and passWord error!")
			return False

		#进入业绩通首页 关闭广告
		time.sleep(3)
		#close___2Ie9H
		#close___2N0oj
		#close___2N0oj
		try:
			self.browser.find_element_by_xpath("//div[@class='close___2Ie9H']").click()
			print("[Info] 关闭了广告 !")
			return True
		except:
			self.browser.find_element_by_xpath("//div[@class='close___2N0oj']").click()
			print("[Info] 关闭了广告 !")
			return True


	'''
			切换窗口

	'''

	def switch_to_newvip(self):
		print(self.browser.window_handles)
		self.browser.switch_to.window(self.browser.window_handles[1])
		print(self.browser.window_handles)
		print("switch_to_newvip"+ str(self.browser.window_handles[1]))

	def switch_to_oldvip(self):
		#handles = browser.window_handles
		print(self.browser.window_handles)
		self.browser.switch_to.window(self.browser.window_handles[0])
		print("switch_to_oldvip"+ str(self.browser.window_handles[0]))

	def switch_pg(self):
		window_1 = self.browser.current_window_handle
		windows = self.browser.window_handles
		for current_window in windows:
		    if current_window != window_1:
		        self.browser.switch_to.window(current_window)

	'''
			人员筛选  第一栏
	'''
	def staff_query_1(self,query_data):
		print("[Info]  点击 人员筛选  第一栏.input data :"+ str(query_data))
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]  老
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]  新

		staff_query_1_list = []
		staff_query_1_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]"
		staff_query_1_2 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]"
		staff_query_1_list.append(staff_query_1_1)
		staff_query_1_list.append(staff_query_1_2)
		for staff_query_1_cik in staff_query_1_list:
			try:
				self.browser.find_element_by_xpath(staff_query_1_cik).click()
				break;
			except:
				continue;

		staff_query_1_input_list = []
		staff_query_1_input_1 = "//*[@id='zglx']"
		staff_query_1_input_2 = "//*[@id='zglx']"
		staff_query_1_input_list.append(staff_query_1_input_1)
		staff_query_1_input_list.append(staff_query_1_input_2)
		for staff_query_1_inp in staff_query_1_input_list:
			try:
				time.sleep(0.5)
				self.browser.find_element_by_xpath(staff_query_1_inp).send_keys(query_data)
				time.sleep(1)
				self.browser.find_element_by_xpath(staff_query_1_inp).send_keys(Keys.ENTER)
				break;
			except:
				continue;

	'''
			人员筛选  第二栏

	'''
	def staff_query_2(self,query_data):
		print("[Info]  点击 人员筛选  第二栏.input data :"+ str(query_data))
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]  老
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]  新

		staff_query_2_list = []
		staff_query_2_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]"
		staff_query_2_2 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]"
		staff_query_2_list.append(staff_query_2_1)
		staff_query_2_list.append(staff_query_2_2)
		for staff_query_2_cik in staff_query_2_list:
			try:
				self.browser.find_element_by_xpath(staff_query_2_cik).click()
				break;
			except:
				continue;

		staff_query_2_input_list = []
		#//*[@id="zgmc"]
		#//*[@id="rydj"]
		staff_query_2_input_1 = "//*[@id='zgmc']"
		staff_query_2_input_2 = "//*[@id='rydj']"
		staff_query_2_input_list.append(staff_query_2_input_1)
		staff_query_2_input_list.append(staff_query_2_input_2)
		for staff_query_2_inp in staff_query_2_input_list:
			try:
				time.sleep(0.5)
				self.browser.find_element_by_xpath(staff_query_2_inp).send_keys(query_data)
				time.sleep(1)
				self.browser.find_element_by_xpath(staff_query_2_inp).send_keys(Keys.ENTER)
				#browser.find_element_by_xpath(staff_query_2_inp).send_keys(Keys.TAB)
				#Keys.TAB
				self.browser.find_element_by_xpath("//div[@class='result___2YCFR']/p").click()
				break;
			except:
				continue;

	'''
			人员筛选  第三栏

	'''
	def staff_query_3(self,query_data):
		print("[Info]  点击 人员筛选  第三栏.input data :"+ str(query_data))
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]  老
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]  新
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div/div[1]
		staff_query_3_list = []
		staff_query_3_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div/div[1]"
		staff_query_3_2 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div/div[1]"
		staff_query_3_3 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div"
		staff_query_3_4 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div"

		staff_query_3_list.append(staff_query_3_1)
		staff_query_3_list.append(staff_query_3_2)
		staff_query_3_list.append(staff_query_3_3)
		staff_query_3_list.append(staff_query_3_4)

		for staff_query_3_cik in staff_query_3_list:
			try:
				self.browser.find_element_by_xpath(staff_query_3_cik).click()
				break;
			except:
				continue;

		staff_query_3_input_list = []
		#//*[@id="zymc"]
		#////*[@id="rylb"]  
		#//*[@id="rydj"]

		staff_query_3_input_1 = "//*[@id='zymc']"
		staff_query_3_input_2 = "//*[@id='rylb']"
		staff_query_3_input_3 = "//*[@id='rydj']"
		staff_query_3_input_list.append(staff_query_3_input_1)
		staff_query_3_input_list.append(staff_query_3_input_2)
		staff_query_3_input_list.append(staff_query_3_input_3)
		for staff_query_3_inp in staff_query_3_input_list:
			try:
				time.sleep(0.5)
				self.browser.find_element_by_xpath(staff_query_3_inp).send_keys(query_data)
				time.sleep(1)
				self.browser.find_element_by_xpath(staff_query_3_inp).send_keys(Keys.ENTER)
				break;
			except:
				continue;

	'''
			人员筛选  第四栏

	'''
	def staff_query_4(self,query_data):
		print("[Info]  点击 人员筛选  第四栏.input data :"+ str(query_data))
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]  老
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[4]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]  新

		staff_query_4_list = []
		staff_query_4_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[4]/div/div/div/div[1]"
		staff_query_4_2 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[4]/div/div/div/div[1]"
		staff_query_4_list.append(staff_query_4_1)
		staff_query_4_list.append(staff_query_4_2)
		for staff_query_4_cik in staff_query_4_list:
			try:
				self.browser.find_element_by_xpath(staff_query_4_cik).click()
				break;
			except:
				continue;

		staff_query_4_input_list = []
		#//*[@id="rydj"]
		#//*[@id="zymc"]
		staff_query_4_input_1 = "//*[@id='rydj']"
		staff_query_4_input_2 = "//*[@id='zymc']"
		staff_query_4_input_list.append(staff_query_4_input_1)
		staff_query_4_input_list.append(staff_query_4_input_2)
		for staff_query_4_inp in staff_query_4_input_list:
			try:
				time.sleep(0.5)
				self.browser.find_element_by_xpath(staff_query_4_inp).send_keys(query_data)
				time.sleep(1)
				self.browser.find_element_by_xpath(staff_query_4_inp).send_keys(Keys.ENTER)
				break;
			except:
				continue;



	'''
			人员筛选  第五栏  选择

	'''
	def staff_query_5(self,query_data,list_number):
		
		print("[Info]  点击 人员筛选  第五栏.input data :"+ str(query_data))
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]  老
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[4]/div/div/div/div[2]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[2]
		
		staff_query_5_list = []
		staff_query_5_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div["+str(list_number+1)+"]/div/div/div/div[2]"
		staff_query_5_2 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div["+str(list_number+1)+"]/div/div/div/div[2]"
		staff_query_5_list.append(staff_query_5_1)
		staff_query_5_list.append(staff_query_5_2)
		for staff_query_5_cik in staff_query_5_list:
			try:
				self.browser.find_element_by_xpath(staff_query_5_cik).click()
				break;
			except:
				continue;
		
		staff_query_5_input_list = []
		#//*[@id="ryrs"]
		#//*[@id="ryrs"]
		staff_query_5_input_1 = "//*[@id='ryrs']"
		staff_query_5_input_2 = "//*[@id='zymc']"
		staff_query_5_input_list.append(staff_query_5_input_1)
		staff_query_5_input_list.append(staff_query_5_input_2)
		for staff_query_5_inp in staff_query_5_input_list:
			try:
				time.sleep(0.5)
				self.browser.find_element_by_xpath(staff_query_5_inp).send_keys(query_data)
				time.sleep(1)
				self.browser.find_element_by_xpath(staff_query_5_inp).send_keys(Keys.ENTER)
				break;
			except:
				continue;


	'''
		 	人员筛选  添加条件

	'''
	def add_staff_query(self,list_number):
		time.sleep(0.5)
		#添加查询条件
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[6]/button
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[6]/button
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[5]/button
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[5]/button
		query_add_xp = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div["+str(list_number+2)+"]/button"
		query_add_xp_new = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div["+str(list_number+2)+"]/button"
		try:
			self.browser.find_element_by_xpath(query_add_xp).click()
		except:
			self.browser.find_element_by_xpath(query_add_xp_new).click()
		
		print("[Info]  人员筛选 点击 添加条件.")



	def add_ryzz(self):
		time.sleep(1)
		query_add_xp = "//button[@data-title='人员筛选']"
		self.browser.find_element_by_xpath(query_add_xp).click()
		print("[Info]  人员筛选 点击 添加条件.")


	'''
			获取添加的人员筛选条件

	'''
	def get_staff_query_data(self):
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[3]/div/ul
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[3]/div/ul
		query_data_xp = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[3]/div/ul"
		query_data_xp_new = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[3]/div/ul"
		try:
			query_result = self.browser.find_element_by_xpath(query_data_xp).text
		except:
			query_result = self.browser.find_element_by_xpath(query_data_xp_new).text
		print("\n"+query_result+"\n")
		if(query_result == ''):
			return False
		return query_result




	'''
			人员筛选  点击选择方法
	'''
	#browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()



	'''
			截图功能

	'''
	def screenshot(self,save_path):
		time.sleep(0.5)
		self.browser.get_screenshot_as_file(save_path)
	'''	
		手动点击 人员分类条件  1
	'''
	def click_renyan_1(self,query_data):
		print("[Info]  点击 人员筛选  第一栏.input data :"+ str(query_data))
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]  老
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]  新
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]
		staff_query_1_list = []
		staff_query_1_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]"
		staff_query_1_2 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]"
		staff_query_1_list.append(staff_query_1_1)
		staff_query_1_list.append(staff_query_1_2)
		for staff_query_1_cik in staff_query_1_list:
			try:
				self.browser.find_element_by_xpath(staff_query_1_cik).click()
				break;
			except:
				continue;
		time.sleep(1)
		self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
	

	def ryzz_1(self,query_data):
		print("点击人员筛选 下拉框1")
		time.sleep(3)
		click_query_1_1 = "/html/body//div[text()='*资格类型']"
		self.browser.find_element_by_xpath(click_query_1_1).click()
		time.sleep(0.5)
		#self.browser.find_element_by_xpath(click_query_1_1).click()
		time.sleep(0.5)
		self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
		print("人员筛选 选择了"+query_data)


	'''	
		手动点击 人员分类条件  2
	'''
	def click_renyan_2(self,query_data):
		print("[Info]  点击 人员筛选  第二栏.input data :"+ str(query_data))
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]  老
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]  新

		staff_query_2_list = []
		staff_query_2_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]"
		staff_query_2_2 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]"
		staff_query_2_list.append(staff_query_2_1)
		staff_query_2_list.append(staff_query_2_2)
		for staff_query_2_cik in staff_query_2_list:
			try:
				self.browser.find_element_by_xpath(staff_query_2_cik).click()
				break;
			except:
				continue;
		time.sleep(1)
		self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
	'''	
		手动点击 人员分类条件  3
	'''
	def click_renyan_3(self,query_data):
		print("[Info]  点击 人员筛选  第三栏.input data :"+ str(query_data))
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]  老
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]  新
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div
		staff_query_3_list = []
		staff_query_3_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div/div[1]"
		staff_query_3_2 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div/div/div/div[1]"
		staff_query_3_3 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div"
		staff_query_3_4 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[3]/div"

		staff_query_3_list.append(staff_query_3_1)
		staff_query_3_list.append(staff_query_3_2)
		staff_query_3_list.append(staff_query_3_3)
		staff_query_3_list.append(staff_query_3_4)
		#/html/body/div[4]
		for staff_query_3_cik in staff_query_3_list:
			try:
				self.browser.find_element_by_xpath(staff_query_3_cik).click()
				break;
			except:
				continue;
		time.sleep(1)
		try:
			self.browser.find_element_by_xpath("/html/body/div[4]//li[@title='"+query_data+"']").click()
		except:
			self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
		
	'''	
		手动点击 人员分类条件  4
	'''
	def click_renyan_4(self,query_data):
		print("[Info]  点击 人员筛选  第四栏.input data :"+ str(query_data))
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]  老
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[4]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]  新

		staff_query_4_list = []
		staff_query_4_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[4]/div/div/div/div[1]"
		staff_query_4_2 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[4]/div/div/div/div[1]"
		staff_query_4_list.append(staff_query_4_1)
		staff_query_4_list.append(staff_query_4_2)
		for staff_query_4_cik in staff_query_4_list:
			try:
				self.browser.find_element_by_xpath(staff_query_4_cik).click()
				break;
			except:
				continue;
		time.sleep(1)
		
		#self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
		#/html/body/div[9]
		try:
			self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
		except:
			self.browser.find_element_by_xpath("/html/body/div[9]//li[@title='"+query_data+"']").click()
		

	'''	
		手动点击 人员分类条件  5
	'''
	def click_renyan_5(self,query_data):
		print("[Info]  点击 人员筛选  第五栏.input data :"+ str(query_data))
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[1]  老
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[4]/div/div/div/div[2]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[2]/div/div/div/div[2]
		#
		staff_query_5_list = []
		staff_query_5_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div["+str(list_number+1)+"]/div/div/div/div[2]"
		staff_query_5_2 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div["+str(list_number+1)+"]/div/div/div/div[2]"
		staff_query_5_list.append(staff_query_5_1)
		staff_query_5_list.append(staff_query_5_2)
		for staff_query_5_cik in staff_query_5_list:
			try:
				self.browser.find_element_by_xpath(staff_query_5_cik).click()
				break;
			except:
				continue;
		time.sleep(1)
		self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()

	'''
			手动点击   企业筛选  条件 1
	'''
	def click_qiye_1(self,query_data):
		print("点击企业筛选 下拉框1")
		# 3. 点击企业筛选 下拉框1 
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div[3]/div
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[1]/div/div/div/div[2]/div
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div/div[1]
		#"/html/body//ul//span[text()='"+QY_input_data_1_val+"']"
		click_query_1_1 = "/html/body//div[text()='*企业资质']"
		click_query_1_2 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div"
		click_query_1_new = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[3]/div/div[2]/div/div[1]/div/div/div"

		click_query_1_list = []
		click_query_1_list.append(click_query_1_1)
		click_query_1_list.append(click_query_1_2)
		click_query_1_list.append(click_query_1_new)

		for click_query_1 in click_query_1_list:
			try:
				self.browser.find_element_by_xpath(click_query_1).click()
				break;
			except:
				continue;
		time.sleep(0.5)

		for i in range(10):
			try:
				el = self.browser.find_element_by_xpath("//li[@title='"+query_data+"']")
				if el.is_displayed():
					break
			except:
				pass
			time.sleep(1)
		else:
			print(query_data+"Time out")

		self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
		print("企业筛选 选择了"+query_data)


	def qiyezz_1(self,query_data):
		print("点击企业筛选 下拉框1")
		time.sleep(3)
		click_query_1_1 = "/html/body//div[text()='*企业资质']"
		self.browser.find_element_by_xpath(click_query_1_1).click()
		time.sleep(0.5)
		#self.browser.find_element_by_xpath(click_query_1_1).click()
		time.sleep(0.5)
		self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
		print("企业筛选 选择了"+query_data)


	'''
			手动点击   企业筛选  条件 2
	'''
	def click_qiye_2(self,query_data):
		print("点击企业筛选 下拉框2")
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div/div/div[1]  新系统

		click_query_2_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div"
		click_query_2_2 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[2]/div/div"

		click_query_2_list = []
		click_query_2_list.append(click_query_2_1)
		click_query_2_list.append(click_query_2_2)

		for click_query_2 in click_query_2_list:
			try:
				self.browser.find_element_by_xpath(click_query_2).click()
				break;
			except:
				continue;
		time.sleep(0.5)
		self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
		print("企业筛选 选择了"+query_data)
	'''
			手动点击   企业筛选  条件 3
	'''
	def click_qiye_3(self,query_data):
		print("点击企业筛选 下拉框3")
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]/div//*[@id="xl"]
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[4]/div/div/div/div[2]/div
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div/div[2]
		#//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div/div   新
		click_query_3_1 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div"
		click_query_3_2 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[3]/div/div"
		click_query_3_list = []
		click_query_3_list.append(click_query_3_1)
		click_query_3_list.append(click_query_3_2)
		for click_query_3 in click_query_3_list:
			try:
				self.browser.find_element_by_xpath(click_query_3).click()
				break;
			except:
				continue;
		time.sleep(0.5)
		self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
		print("企业筛选 选择了"+query_data)
	'''
			手动点击   企业筛选  条件 4
	'''
	def click_qiye_4(self,query_data):
		print("点击企业筛选 下拉框4")
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[4]/div/div/div
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[4]/div/div/div/div[1]
		click_query_4 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[4]/div/div"
		click_query_4_new = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[4]/div/div"
		try:
			self.browser.find_element_by_xpath(click_query_4).click()
		except:
			self.browser.find_element_by_xpath(click_query_4_new).click()
		
		time.sleep(0.5)
		self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
		print("企业筛选 选择了"+query_data)



	def qiyezz_4(self,query_data):
		print("点击企业筛选 下拉框1")
		time.sleep(1)
		#click_query_1_1 = "/html/body//div[text()='*等级区分']"
		#self.browser.find_element_by_xpath(click_query_1_1).click()
		#time.sleep(0.5)
		#self.browser.find_element_by_xpath(click_query_1_1).click()
		#time.sleep(0.5)
		self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
		print("企业筛选 选择了"+query_data)



	'''
			手动点击   企业筛选  条件 5
	'''
	def click_qiye_5(self,query_data):
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[5]/div/div/div
		qiye_query_5 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[5]/div/div"
		qiye_query_5_new = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[2]/div/div[5]/div/div"
		try:
			self.browser.find_element_by_xpath(qiye_query_5).click()
		except:
			self.browser.find_element_by_xpath(qiye_query_5_new).click()
		
		time.sleep(0.5)
		self.browser.find_element_by_xpath("//li[@title='"+query_data+"']").click()
	
	'''
		  企业筛选	联动查询  按钮 点击

	'''
	def qiye_liandong_button(self):
		print("点击了 企业筛选	联动查询  按钮 ") 
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/div/button
		#//*[@id="root"]/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/div/button
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/div/button
		liandong_button_1 = "//*[@id='root']/div/div[1]/div[1]/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/div/button"
		liandong_button_2 = "//*[@id='root']/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/div/button"

		

		try:
			#点击联动查询
			self.browser.find_element_by_xpath(liandong_button_1).click()
			time.sleep(1)
		except:
			#点击联动查询
			self.browser.find_element_by_xpath(liandong_button_2).click()
			time.sleep(1)

		'''
		#输入联动查询的两个输入框
		js_1 = """
			//document.getElementById('modal_xmmc').value="aaa";
			document.getElementById('modal_zbje_2').value="1";

		"""
		js_10 = """
			//document.getElementById('modal_xmmc').value="aaa";
			document.getElementById('modal_zbje_2').value="10";

		"""
		self.browser.execute_script(js_1)
		time.sleep(1)

		#选择第二个联动查询框
		ld_input_2 = "/html/body/div[5]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/div/div/div/div"
		self.browser.find_element_by_xpath(ld_input_2).click()
		self.browser.find_element_by_xpath("//li[@title='"+ld_input_data2+"']").click()
		'''

		'''
		# 取消联动查询
		liandong_close_button_1 = "/html/body/div[5]/div/div[2]/div/div[1]/div[3]/button[1]"
		self.browser.find_element_by_xpath(liandong_close_button_1).click()
		'''


		print(" 显示企业筛选	联动查询 界面")
		
	'''
				确定 button
	'''
	def liandong_ok_button(self,post_number):
		
		time.sleep(1)

		print("点击了 联动查询  确定按钮 ") 
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/div/button

		liandong_ok_button_1 = "/html/body/div["+str(post_number+2)+"]/div/div[2]/div/div[1]/div[3]/button[2]"
		liandong_ok_button_2 = "//span[text()='确 认']"
		liandong_ok_button_3 = ""

		self.browser.find_element_by_xpath(liandong_ok_button_1).click()

		'''
		liandong_ok_button_list = []
		liandong_ok_button_list.append(liandong_ok_button_1)
		liandong_ok_button_list.append(liandong_ok_button_2)
		liandong_ok_button_list.append(liandong_ok_button_3)

		for ok_button in liandong_ok_button_list:
			try:
				self.browser.find_element_by_xpath(ok_button).click()
				break;
			except:
				continue;

		'''

	'''
			取消 button
	'''
	def liandong_close_button(self,post_number):
		time.sleep(1)

		print("点击了 联动查询  取消按钮 ") 
		#//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[2]/div/div[3]/div/div/button
		liandong_close_button_1 = "/html/body/div["+str(post_number+2)+"]/div/div[2]/div/div[1]/div[3]/button[1]"
		liandong_close_button_2 = "//span[text()='取 消']"
		liandong_close_button_3 = ""

		self.browser.find_element_by_xpath(liandong_close_button_1).click()

		'''
		liandong_close_button_list = []
		liandong_close_button_list.append(liandong_close_button_1)
		liandong_close_button_list.append(liandong_close_button_2)
		liandong_close_button_list.append(liandong_close_button_3)

		for close_button in liandong_close_button_list:
			try:
				self.browser.find_element_by_xpath(close_button).click()
				break;
			except:
				continue;
		'''

	'''
			企业联动查询第一个输入框

	'''
	def qiye_ld_input_1(self,ld_input_data1,post_number):
		print("联动查询 输入框 输入内容 ")
		'''
		js_1 = """
			//document.getElementById('modal_xmmc').value="aaa";
			document.getElementById('modal_zbje_2').value="1";

		"""
		js_10 = """
			//document.getElementById('modal_xmmc').value="aaa";
			document.getElementById('modal_zbje_2').value="10";

		"""
		self.browser.execute_script(js_1)
		time.sleep(0.5)
		#self.browser.execute_script("window.scrollBy(0,200)","")
		#time.sleep(0.5)
		'''

		time.sleep(0.5)
		print("选择第五个联动查询框")
		#/html/body/div[5]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[5]
		#/html/body/div[7]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[5]
		ld_input_1 = "/html/body/div["+str(post_number+2)+"]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[5]"
		self.browser.find_element_by_xpath(ld_input_1).click()
		#//*[@id='modal_zbje_2']
		#self.browser.find_element_by_xpath("//li[@title='"+ld_input_data2+"']").click()
		time.sleep(0.5)
		self.browser.find_element_by_xpath("//*[@id='modal_zbje_2']").send_keys(ld_input_data1)
		time.sleep(1)
		self.browser.find_element_by_xpath("//*[@id='modal_zbje_2']").send_keys(Keys.ENTER)
	'''
			企业联动查询第二个 选择框
	'''
	def qiye_ld_input_2(self,ld_input_data2,post_number):
		time.sleep(0.5)
		print("选择第二个联动查询框")
		ld_input_2 = "/html/body/div["+str(post_number+2)+"]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[1]/div/div/div/div"
		self.browser.find_element_by_xpath(ld_input_2).click()
		self.browser.find_element_by_xpath("//li[@title='"+ld_input_data2+"']").click()

	'''
			企业联动查询第三个 选择框
	'''
	def qiye_ld_input_3(self,ld_input_data3,post_number):
		time.sleep(0.5)
		print("选择第三个联动查询框")
		ld_input_3 = "/html/body/div["+str(post_number+2)+"]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[2]/div/div/div[1]"
		self.browser.find_element_by_xpath(ld_input_3).click()
		self.browser.find_element_by_xpath("//li[@title='"+ld_input_data3+"']").click()


	'''
			企业联动查询第四个 选择框
	'''
	def qiye_ld_input_4(self,ld_input_data4,post_number):
		time.sleep(0.5)
		print("选择第四个联动查询框")
		ld_input_4 = "/html/body/div["+str(post_number+2)+"]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[3]/div/div/div"
		self.browser.find_element_by_xpath(ld_input_4).click()
		self.browser.find_element_by_xpath("//li[@title='"+ld_input_data4+"']").click()


	'''
			企业联动查询第五个 选择框
	'''
	def qiye_ld_input_5(self,ld_input_data5,post_number):
		time.sleep(0.5)
		print("选择第五个联动查询框")
		ld_input_5 = "/html/body/div["+str(post_number+2)+"]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[4]/div/button"
		self.browser.find_element_by_xpath(ld_input_5).click()
		self.browser.find_element_by_xpath("//li[@title='"+ld_input_data5+"']").click()

	'''
			企业联动查询第六个输入框

	'''
	def qiye_ld_input_6(self,ld_input_data6,post_number):
		time.sleep(0.5)
		print("选择第五个联动查询框")
		ld_input_6 = "/html/body/div["+str(post_number+2)+"]/div/div[2]/div/div[1]/div[2]/div[1]/div/div[1]/div/div[6]/div/div/div/div[1]"
		self.browser.find_element_by_xpath(ld_input_6).click()
		self.browser.find_element_by_xpath("//li[@title='"+ld_input_data6+"']").click()


	#屏幕上拉
	def top_windos(self):
		time.sleep(0.5)
		self.browser.execute_script("""
		(function () {
		 window.scroll(0, 0);
        })();
		""")
		time.sleep(0.5)

	#屏幕下拉
	def next_windos(self):
		time.sleep(0.5)
		self.browser.execute_script("""
		(function () {
		 window.scroll(0, 3000);
        })();
		""")
		time.sleep(0.5)


	#进入重庆分类
	def open_chongqin(self):
		time.sleep(1)
		ld_input_6 = '//*[@id="root"]/div/div[1]/div[2]/div/div/div/div[2]/div[1]/div[1]/ul/li[2]'
		self.browser.find_element_by_xpath(ld_input_6).click()





