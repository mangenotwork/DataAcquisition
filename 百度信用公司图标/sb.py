import pytesseract
from PIL import Image,ImageDraw

#pytesseract.pytesseract.tesseract_cmd = 'F:/Tesseract-OCR/tesseract.exe'
#C:\\Users\\Administrator\\Desktop\\企业雷达\\百度信用公司图标\\getCapImg.jpg
#F:\\baiduimg\\0ERuBLlQ_imges.png
#F:\\yzm\\1412260-20180701125834481-1681474414.png
img = Image.open('F:\\yzm\\txtimg.png')
img = img.convert('L')
#img = img.point(lambda x: 0 if x<100 else x>=100, '1')





#img.show()
text = pytesseract.image_to_string(img,lang='chi_sim')


print(text)
