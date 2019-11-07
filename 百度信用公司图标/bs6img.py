import base64
 
with open("F:/yzm/1a8c.png", 'rb') as f:
    base64_data = base64.b64encode(f.read())
    s = base64_data.decode()
    print("data:image/png;base64,"+s)
