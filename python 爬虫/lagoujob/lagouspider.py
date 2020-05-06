import requests,os,json,time,random,pickle,urllib
import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from requests.packages import urllib3
urllib3.disable_warnings()

headers = {
	'Accept': 'application/json, text/javascript, */*; q=0.01',
	'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
	'Referer':''
}



def creat_urls(positon):
	#城市列表
	citys = ['北京','深圳','上海','广州','杭州','成都','南京','武汉','重庆','天津']
	#城市起始url
	url = 'https://www.lagou.com/jobs/list_{}?city={}&cl=false&fromSearch=true&labelWords=&suginput="'
	city_urls = []
	for city in citys:
		#中文字符编码处理
		city_quote = urllib.parse.quote(city)
		city_url = url.format(positon,city_quote)
		city_urls.append(city_url)
	city_and_url = list(zip(city_urls,citys))
	return city_and_url

def get_data(city_and_url):
	url = city_and_url[0]
	city = city_and_url[1]
	headers['Referer'] = url
	#招聘信息url
	job_url =  'https://www.lagou.com/jobs/positionAjax.json?px=default&city={}&needAddtionalResult=false'.format(urllib.parse.quote(city))
	info_dict = {}
	info_dict[city] = []
	start=1
	while start<=26:
		s = requests.Session()
		print(url)
		s.get(url, headers=headers, timeout=5,verify=False)
		cookie = s.cookies
		s.headers = headers
		for page in range(start,start+5):
			print('[INFO]: Get <%s>-<Page.%s>' % (city, page))
			data = {
				'first': 'true',
				'pn': str(page),
				'kd': 'python'
			}
			try:
				res = s.post(job_url,data=data,headers=headers)
				result = json.loads(res.text)['content']['positionResult']['result']
			except:
				print('[Warning]: <%s>-<Page.%s> lost...' % (city, page))
				break			
			for item in result:
				info_dict[city].append([item.get('companyFullName', '无'), 
								item.get('companyShortName', '无'), 
								item.get('positionName', '无'), 
								item.get('positionAdvantage', '无'), 
								item.get('industryField', '无'), 
								item.get('companySize', '无'), 
								item.get('jobNature', '无'), 
								item.get('education', '无'), 
								item.get('workYear', '无'), 
								item.get('salary', '无')])
				time.sleep(2)
		start += 5
		time.sleep(10)
	print(info_dict[city])		
	return info_dict

def save(info_dict,fileName):
	infoDict={}
	for item in info_dict:
		infoDict.update(item)
	with open('{}.pkl'.format(fileName),'wb') as f:
		pickle.dump(infoDict, f)
	print('保存成功')

def lagou_spider(positon,fileName):
	'''
	爬取10个主要城市的某职位招聘信息
	'''
	#城市(url,city)列表
	city_and_url = creat_urls(positon)
	#进程池
	pool = multiprocessing.Pool(10)
	info_dict = pool.map(get_data,city_and_url)
	save(info_dict)
	pool.close()
	pool.join()


if __name__ == '__main__':
	lagou_spider("区块链","区块链-info")



