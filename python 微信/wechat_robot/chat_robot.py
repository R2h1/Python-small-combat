# -*- coding: utf-8 -*-
import json
import time
import requests
import itchat

#Turling_key
KEY = '54d7869f48ff4f1f8d856d52d3c7cdf2'

def get_response(msg):
	'''
	发送数据包给图灵服务器
	'''
	apiUrl = 'http://openapi.tuling123.com/openapi/api/v2'
	#动态生成userid
	uid = 'rrh'
	#字典转json
	data ={
	"reqType":0,
    "perception": {
        "inputText": {
            "text": msg,
        }
    },
    "userInfo": {
        "apiKey": KEY,
        "userId": uid,
    }
}
	
	try:
		data_json = json.dumps(data)
		response = requests.post(apiUrl,data=data_json).json()
		return response['results'][0]['values']['text']
	except:
		return

#处理消息并自动回复
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
	#默认回复
	defaultReply = '【{}】，这句话俺听不懂啦'.format(msg['Text'])
	FromUserName = msg['FromUserName']
	reply = get_response(msg['Text'])

	if reply:
		itchat.send(reply,toUserName=FromUserName)
	else:
		itchat.send(defaultReply,toUserName=FromUserName)


if __name__ == '__main__':
	itchat.auto_login(hotReload=True)
	itchat.run()