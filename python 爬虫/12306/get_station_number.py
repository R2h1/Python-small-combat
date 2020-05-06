import requests


class ParseStation(object):

	def __init__(self):
		#请求头
		self.headers = {
			'Referer':'https://www.12306.cn/index/index.html',
			'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.108 Safari/537.36'
		}

		self.url = 'https://www.12306.cn/index/script/core/common/station_name_v10035.js'

	def parse_station(self,station_opt):
		try:
			res = requests.get(self.url,headers=self.headers,verify=False)
		except Exception as ex:
			print('车站英文请求响应出错')
		city_list = res.text.split('|')
		city_dict = {}
		for k,i in enumerate(city_list):
			if "@" in i:
				city_dict[city_list[k+1]] = city_list[k+2]
		station_num = city_dict[station_opt]
		station_opt_and_num = station_opt+','+station_num
		return station_opt_and_num

ps = ParseStation()