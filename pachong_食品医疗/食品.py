import base2
import time



aaa = base2.YJT_test()

aaa.open_url("http://qy1.sfda.gov.cn/datasearch/face3/base.jsp?tableId=120&tableName=TABLE120&title=%CA%B3%C6%B7%C9%FA%B2%FA%D0%ED%BF%C9%BB%F1%D6%A4%C6%F3%D2%B5(SC)&bcId=145275419693611287728573704379")


datalist = '//*[@id="content"]/div/table[2]'
get_datas = aaa.get_txt_public_xpath(datalist)
print(get_datas)

time.sleep(1)
#下拉

aaa.next_windos()
time.sleep(2)
#按下一页
#//*[@id="content"]/div/table[4]/tbody/tr/td[4]/img
#//*[@id="content"]/table[4]/tbody/tr/td[5]
#aaa.click_public_1('//*[@id="content"]/table[4]/tbody/tr/td[5]')



#输入页数
#//*[@id="goInt"]
#aaa.input_public_1('//*[@id="goInt"]','2')
#time.sleep(2)



#//*[@id="content"]/div/table[4]/tbody/tr/td[7]/input
#aaa.click_public_1('//*[@id="content"]/div/table[4]/tbody/tr/td[7]/input')
