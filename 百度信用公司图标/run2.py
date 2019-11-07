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


os.environ["webdriver.chrome.driver"] = chromedriver_EXE_path
browser = webdriver.Chrome(chromedriver_EXE_path)
browser.get("https://xin.baidu.com/s?q=&t=0&fl=1&castk=LTE%3D")
time.sleep(1)
browser.maximize_window()
a = input("input:")

#输入公司名称
input_query_3 = "/html/body/div[2]/div/div[2]/div[3]/div/div/div/input"
browser.find_element_by_xpath(input_query_3).send_keys("华为")
time.sleep(2)

click_query_3 = '/html/body/div[2]/div/div[2]/div[3]/div/div/input'
browser.find_element_by_xpath(click_query_3).click()
time.sleep(1)
print(browser.page_source)


