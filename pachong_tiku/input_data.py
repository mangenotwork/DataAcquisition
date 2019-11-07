import csv
import time
import mandb


'''
CREATE TABLE timu_1(
	temp_id INT UNSIGNED AUTO_INCREMENT,/*  主(不可重复) 临时id */
	njtype varchar(50) NOT NULL,/* 年级类型 */
	tmtype varchar(500) NOT NULL,/* 题目类型 */
	urls varchar(500) NOT NULL,/* 数据源链接 */
	tmdata TEXT NOT NULL,/* 题目文本 */
	daandata TEXT NOT NULL,/* 题目答案 */
	jiexi TEXT NOT NULL,/* 题目解析 */

	PRIMARY KEY (temp_id)
)ENGINE=InnoDB DEFAULT CHARSET=utf8;	

'''


#
def adddata(listss):
	try:
		man_db = mandb.DB()
		sql = "INSERT INTO timu_2 ( njtype, tmtype, urls, tmdata, daandata, jiexi) \
					VALUES ('"+listss[0]+"', '"+listss[1]+"', '"+listss[2]+"', \
					'"+str(listss[3]).replace("'","\"")+"', '"+str(listss[4]).replace("'","\"")+"', '"+str(listss[5]).replace("'","\"")+"' );"
		man_db.execute(sql)
	except Exception as e:
		print(e)
		return adddata(listss)
	



csv_path = "f:/timu_yinyu_4.csv"

#解决读取存在大字段的数据
csv.field_size_limit(500 * 1024 * 1024)

with open(csv_path, 'r',encoding='utf-8') as f:
	data = csv.reader((line for line in f), delimiter=",")
	#data = csv.reader((line for line in f), delimiter=",")
	#print(len(data))
	n=1
	
	for row in data:
		
		#131072
		
		if n>=101315:
			print(n)
			print(row)
			#print(d_date)
			adddata(row)
			print("\n\n\n\n")
		
		
		n+=1
	print(n)
	
