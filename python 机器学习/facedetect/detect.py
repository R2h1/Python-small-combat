#!/usr/bin/env python
#-*-coding:utf-8-*-

import base64
import requests
import json

headers={
	'Content-Type':'application/json; charset=UTF-8',
}


def get_access_key():
	'''获取请求人脸检测所需的access_token'''
	api_token = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=LpE2pKibqSeivowItQt9GTNz&client_secret=oGjD6wO4UOhQ5SpbSaaHgdRe13OeLPFs'
	try:
		res = requests.get(api_token,headers=headers)
		token = json.loads(res.text)['access_token']
		return token
	except:
		print('token请求失败')


def read_face_data(imagepath):
	'''读取人脸图像的base64数据'''

	with open(imagepath,'rb') as f:
		data = base64.b64encode(f.read())
		return data.decode('utf-8')

def face_score(data,token):
	'''人脸检测'''
	url = "https://aip.baidubce.com/rest/2.0/face/v3/detect?access_token={}".format(token)
	params = {
	"image":data,
	"image_type":"BASE64",
	"face_field":"age,gender,beauty"
	}
	params=json.dumps(params)
	try:
		res = requests.post(url,headers=headers,data=params)
		# print(res.text)
		result =  json.loads(res.text)['result']['face_list'][0]
	except:
		print('检测失败')

	detectDict = {
	'人脸置信度':result['face_probability'],
	'年龄':result['age'],
	'性别':result['gender']['type'],
	'性别置信度':result['gender']['probability'],
	'颜值评分':str(result['beauty'])+'分',
	}
	return detectDict

def main(imagepath):
	token = get_access_key()
	# print(token)
	data = read_face_data(imagepath)
	detectDict = face_score(data,token)
	print(detectDict)

if __name__ == '__main__':
	main('Zhaoliying.jpg')