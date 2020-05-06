import time,requests
import qrcode
import re

tid = int(str(round(time.time(),3)).replace(".",""))
url = 'https://login.wx.qq.com/jslogin'
data ={
	'appid':'wx782c26e4c19acffb',
	'redirect_uri':'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage',
	'fun':'new',
	'lang':'zh_CN',
	'_':tid
}
headers = {
	'Connection':'keep-alive',
	'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
	'Referer':'https://wx.qq.com/'
}

res = requests.get(url,headers=headers,params=data,verify=False)

code = re.findall(r'uuid = "(.+?)"',res.text)[0]

code_url = 'https://login.weixin.qq.com/l/'+code

qrcode_im = qrcode.make(code_url)

qrcode_im.save('wechatcode.png')

