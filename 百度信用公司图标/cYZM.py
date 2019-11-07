# pip install captcha
from captcha.image import ImageCaptcha
import io
import base64
import random


#生成验证码
#print(TempImg.getvalue())




'''
with open(TempImg, 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
    print("data:image/png;base64,"+s)
'''



def ranstr(num):
    H = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    salt = ''
    for i in range(num):
        salt += random.choice(H)
    return salt




def c_yzm():
	#用于生成验证码的字符集
	CHAR_SET = ['0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g',
				'h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w',
				'x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N',
				'O','P','Q','R','S','T','U','V','W','X','Y','Z']
	yzm_data = random.sample(CHAR_SET, 4)
	yzm_data = "".join(yzm_data)
	#print(yzm_data)
	#忽略大小写，验证码验证值为小写
	yzm_key = yzm_data.lower()
	#print(yzm_key)
	#生成验证码
	ic = ImageCaptcha()
	#创建一个字节空间存储验证码
	TempImg = io.BytesIO()
	ic.write(yzm_data, TempImg, format='png')
	#TempImg.getvalue() 取图片
	#将图片进行base64编码并返回
	base64_data = base64.b64encode(TempImg.getvalue())
	img_base64_data = '<img src="data:image/png;base64,'+base64_data.decode()+'"/>'
	#print(img_base64_data)
	return img_base64_data,yzm_key,ranstr(18)

img,key,keyname = c_yzm()

print("\n")
print("\n")

print(img)
print("\n")
print("\n")
print("\n")




print("\n")
print(key)
print("\n")
print(keyname)






#验证功能 - 客户端
# 1. API接口生成一个验证码转换成IMGbase64 并返回 Keyname(随机码) 与 Key(验证码字符)
# 2. 将生成的Keyname 与 Key 对应存入 Redis中
# 3. 给前端返回 IMGbase64 与 Token(manyzm) = Keyname  【发放】：发放验证码与coke
# 4. 前端验证接口  传入字符串（inputstr） 带 Tonk(manyzm)
# 5. 服务端通过 Keyname 找到 Key 再与 inputstr 对比，如果错误返回 0, 正确返回 1
# 6. 删除Redis中 Keyname 与 Key 的对应数据    【销毁】：每一个发放与验证完成后则销毁验证码与key


#验证功能 - 代理端
# 1. API接口生成一个验证码转换成IMGbase64 并返回 Keyname(随机码) 与 Key(验证码字符)
# 2. 将生成的Keyname 与 Key 对应存入 Redis中
# 3. 给代理返回 IMGbase64 与  Keyname  Key
# 4. 代理端验证接口  传入字符串（inputstr） 带 Keyname
# 5. 服务端通过 Keyname 找到 Key 再与 inputstr 对比，如果错误返回 0, 正确返回 1
# 6. 删除Redis中 Keyname 与 Key 的对应数据    【销毁】：每一个发放与验证完成后则销毁验证码与key


#验证功能 - 只发放
# 1. API接口生成一个验证码转换成IMGbase64 并返回 Keyname(随机码) 与 Key(验证码字符)
# 2. 返回 IMGbase64 与  Key
