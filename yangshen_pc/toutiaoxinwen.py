#!/usr/bin/env python
# -*- coding=utf-8 -*-
__author__ = 'man'

'''
	鲁班建业模拟操作脚本
		
'''
import os,sys
from multiprocessing import Process
import time






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
	def next_windos(self,px):
		time.sleep(0.5)
		self.browser.execute_script("\
		(function () {\
		 window.scroll(0, "+str(px)+");\
        })();\
		")
		time.sleep(0.5)

	def get_val_1(self,xpathdata):
		return self.browser.find_element_by_xpath(xpathdata)




yb_base = YJT_test()
#global yb_base



yb_base.open_web()
#鲁班建业地址、
L_url = "http://mini.eastday.com/#jiankang"
yb_base.open_url(L_url)
time.sleep(1)

#获取到url 将 url 保存


xp1 = '//*[@id="data-list"]/li[3]'
print(yb_base.get_val_1(xp1))
#yb_base.next_windos(1000)


