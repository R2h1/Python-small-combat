'''
QQ音乐下载器v1.0

只能下载QQ音乐网页版可以播放的歌曲
	-----@R2h----
'''

import requests
import time 
import re
import json
from jsonpath import jsonpath
from selenium import webdriver
from contextlib import closing

#request请求头
HEADERS = {
		'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
		}
#无头浏览器配置
OPTIONS = webdriver.ChromeOptions()
#开启无界面模式
OPTIONS.add_argument('--headless')
# 禁用gpu
OPTIONS.add_argument('--disable-gpu')


class QQMusicDownloader(object):

	def __init__(self,songname_singer=None):
		self.songname_singer = songname_singer
		#创建浏览器
		self.browser = webdriver.Chrome('./chromedriver',options=OPTIONS)
		#隐式等待3秒
		self.browser.implicitly_wait(2)
		#requsets请求头
		self.headers = HEADERS
		#歌曲搜索url
		self.search_url = 'https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w={}'.format(self.songname_singer)
		#获取下载链接的url
		self.get_vkey_url = 'https://u.y.qq.com/cgi-bin/musicu.fcg?data='
		#歌曲下载地址
		self.download_url = 'http://ws.stream.qqmusic.qq.com/{}'
		#获取歌曲下载链接所需的参数
		self.params = {
			"req":{
				"module":"CDN.SrfCdnDispatchServer",
				"method":"GetCdnDispatch",
				"param":{
					"guid":"",
					"calltype":0,
					"userip":""}
			},
			"req_0":{
				"module":"vkey.GetVkeyServer",
				"method":"CgiGetVkey",
				"param":{
					"guid":"",
					"songmid":"",    #歌曲的songmid
					"songtype":[0],
					"uin":"0",
					"loginflag":1,
					"platform":"20"}
			},
			"comm":{
				"uin":0,
				"format":"json",
				"ct":24,
				"cv":0},
		}

	def brower_get_song_mid(self):
		'''
		获取歌曲的songmid
		:return:歌曲的songmid
		'''
		#打开搜索歌曲url
		self.browser.get(self.search_url)
		print('歌曲:{}     正搜索中...'.format(self.songname_singer))
		#强制等待3秒
		time.sleep(2)
		#定位歌曲精准链接
		song_url = (self.browser.find_element_by_xpath('//ul[@class="songlist__list"]/li[1]/div/div[2]/span[1]/a')
			.get_attribute("href"))
		#正则匹配出歌曲的songmid
		song_mid = re.findall(r'song/(.+?).html',song_url)
		return song_mid

	def get_data(self,url):
		'''
		requests请求网页，
		得到带有下载链接的json字符串
		：params:请求的url
		'''
		try:
			res = requests.get(url,headers=self.headers,timeout=5)
			return res.text
		except Exception as e:
			return None

	def create_param(self,songmid):
		'''
		构造获取歌曲下载url所需的参数，
		拼接出获取下载链接的url
		：params:歌曲songmid
		 :return:获取下载链接的url
		'''
		#参数所需guid时间戳
		guid = str(round(time.time()))
		#设置guid
		self.params['req']['param']['guid'] = guid
		self.params['req_0']['param']['guid'] = guid
		#设置参数所需songmid
		self.params['req_0']['param']['songmid'] = songmid
		#字典转换为字符串
		data=json.dumps(self.params)
		#拼接url
		url = self.get_vkey_url+data
		return url

	def get_download_url(self,id):
		'''
		获取歌曲下载链接
		:params:歌曲id
		:return:歌曲下载链接
		'''
		#构造params，拼接成获取下载链接的url
		url = self.create_param(id)
		#带有下载链接的json字符串
		text = self.get_data(url)
		#返回的json字符串并转换为字典
		result = json.loads(text)
		#jsonpath解析出下载链接
		if jsonpath(result,'$..purl')[0] == '':
			print("获取歌曲下载链接失败")
			return
		download_url = self.download_url.format(jsonpath(result,'$..purl')[0])
		return download_url

	def downloader(self,url):
		'''
		下载歌曲
		：params:下载链接
		：return:None
		'''
		if url is None:
			return
		with closing(requests.get(url,headers =self.headers,stream = True)) as res:
			print('--------------开始下载--------------')
			with open('./'+self.songname_singer+'.m4a','wb') as f:
				print("歌曲:{}     正在下载...".format(self.songname_singer))
				for chunk in res.iter_content(chunk_size = 1024):
					f.write(chunk)	
			print("歌曲:{}.m4a 下载成功...".format(self.songname_singer))

	def run(self):
		#自动化调用浏览器，获取song_mid
		song_mid = self.brower_get_song_mid()
		#获取下载链接
		downloader_url =self.get_download_url(song_mid)
		#下载歌曲
		self.downloader(downloader_url)
		#关闭浏览器
		self.browser.quit()


if __name__ == '__main__':
	musicdl = QQMusicDownloader("我是如此相信")
	musicdl.run()
	
