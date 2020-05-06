'''
精美图片下载
'''
import requests
import json
import time
import random
from contextlib import closing

class Imgdownloader(object):

	#初始化
	def __init__(self):
		self.headers= {
		'Referer': 'https://unsplash.com/',
		'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) \
		AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36',
		}
		self.base_url = 'https://unsplash.com/napi/photos'
		self.img_urls = []
		self.page = 0
		self.per_page =12


	def get_img_urls(self):
		'''获取图片链接地址
		'''
		
		for i in range(self.per_page):
			self.page = self.page+i+1
			params={
			"page":self.page,
			"per_page":self.per_page,
			}
			res =requests.get(self.base_url,params = params)
			#json转换为字典
			res_dict = json.loads(res.text)

			for item in res_dict:

				url = item['urls']['regular']

				self.img_urls.append(url)

			#每次获取一页链接，随机休眠
			time.sleep(random.random())
		print("图片urls获取成功")

	def img_download(self,urls):
		'''
		下载图片到本地存储
		'''
		num = 0
		for url in urls:

			num = num + 1
			img_path = str(num) +".jpg"
			with closing(requests.get(url,headers =self.headers,stream = True)) as res:
				with open(img_path,'wb') as f:
					print("正在下载第{}张照片".format(num))
					for chunk in res.iter_content(chunk_size = 1024):
						f.write(chunk)	
				print("{}.jpg 下载成功".format(num))


if __name__ == '__main__':
	#图片下载对象
	imgdl = Imgdownloader()
	print("获取图片链接中...")
	#对象获取图片链接
	
	imgdl.get_img_urls()


	print("开始下载图片：")
	#下载图片
	imgdl.img_download(imgdl.img_urls)

	print('所有图片下载完成')




