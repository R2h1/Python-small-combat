import time
import random
from requests.packages import urllib3
from selenium import webdriver
#显性等待
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
#图像处理
from PIL import Image
from io import BytesIO
#打码api
from yundama_api import yundama
from get_station_number import *
#禁用requests的警告
urllib3.disable_warnings()

#无头浏览器配置
#OPTIONS = webdriver.ChromeOptions()
#开启无界面模式
#OPTIONS.add_argument('--headless')
# 禁用gpu
#OPTIONS.add_argument('--disable-gpu')

class GrabTrainTicket(object):

	def __init__(self,userName=None,pwd=None,date=None,fromStation=None,toStation=None):
		#创建浏览器对象
		self.browser = webdriver.Chrome('./chromedriver')
		#隐式等待
		#self.browser.implicitly_wait(3)
		#创建显性等待对象
		self.wait = WebDriverWait(self.browser,10,0.5)
		#用户名
		self.userName = userName
		#密码
		self.pwd = pwd
		#出发日期
		self.date = date
		#出发地
		self.fs = ps.parse_station(fromStation)
		#目的地
		self.ts = ps.parse_station(toStation)

	def check_ticket(self):
		'''查询车票'''
		check_ticket_url = 'https://kyfw.12306.cn/otn/leftTicket/init?linktypeid=dc&fs={}&ts={}&date={}&flag=N,N,Y'
		self.browser.get(check_ticket_url.format(self.fs,self.ts,self.date))
		flag=True
		#历时排序(用时短到长),需要点两下
		self.browser.find_element_by_id('l_s').click()
		time.sleep(1)
		self.browser.find_element_by_id('l_s').click()
		#循环查询
		while flag:
			
			#获取所有车次元素
			#tr_list_elements=self.wait.until(EC.visibility_of_element_located((By.ID,'queryLeftTable')))
			#tr_list_elements=tr_list_elements.find_elements_by_xpath

			tr_list_elements = self.browser.find_elements_by_xpath('//tbody[@id="queryLeftTable"]/tr')
			#遍历车次元素
			for i,tr_element in enumerate(tr_list_elements):
				if i % 2 == 0:
					#print(tr_element.find_element_by_class_name('start-t').text)
					try:	
						tr_element.find_element_by_class_name('btn72').click()
						flag = False
						break
					except:
						continue
			if flag == False:
				break
			#点击查询按钮
			self.browser.find_element_by_id('query_ticket').click()
			time.sleep(2)

	def login(self):
		'''登录12306'''
		time.sleep(1)
		#点击账号登录
		self.wait.until(EC.visibility_of_element_located((By.LINK_TEXT,'账号登录'))).click()
		time.sleep(1)
		self.browser.find_element_by_id('J-userName').send_keys(self.userName)
		time.sleep(1)
		self.browser.find_element_by_id('J-password').send_keys(self.pwd)
		#获取验证码图片和验证码对象
		login_img,login_img_element = self.get_code_img()
		#识别验证码
		result = yundama('login_img.png',6701)
		#str = ','.join(result)
		#print('识别结果：第{}张图片'.format(str))
		positions = [
			(40,75),
			(118,71),
			(170,64),
			(265,65),
			(22,139),
			(129,146),
			(184,150),
			(276,140),
		]
		for num in result :
			position = positions[int(num)-1]
			action = ActionChains(self.browser)
			time.sleep(random.uniform(0.5,1))
			action.move_to_element_with_offset(login_img_element,position[0],position[1]).click().perform()
		time.sleep(1)
		self.browser.find_element_by_id('J-login').click()

	def get_code_img(self):
		'''获取验证码图片和验证码对象'''
		full_page_img = self.browser.get_screenshot_as_png()
		full_page_img = Image.open(BytesIO(full_page_img))
		#获取验证码图片对象
		login_img_element = self.wait.until(EC.visibility_of_element_located((By.ID,'J-loginImg')))
		location = login_img_element.location
		size = login_img_element.size
		x1,y1,x2,y2 = location['x']-size['width']//2-6,location['y'],location['x']+size['width']//2,location['y']+size['height']
		login_img = full_page_img.crop((x1,y1,x2,y2))
		login_img.save('login_img.png')
		return login_img,login_img_element

	def confirm_order(self):
		'''确认订单'''
		#选择乘客
		self.wait.until(EC.visibility_of_element_located((By.ID,'normalPassenger_4'))).click()
		time.sleep(1)
		try:
			#学生
			self.wait.until(EC.visibility_of_element_located((By.ID,'dialog_xsertcj_ok'))).click()
			print('学生票')
			time.sleep(1)
		except:
			print('成人票')
		finally:
			#点击提交订单
			self.browser.find_element_by_id('submitOrder_id').click()
			time.sleep(1)
			#点击确认提交
			self.wait.until(EC.visibility_of_element_located((By.ID,'qr_submit_id'))).click()
			print('订单确认，请前往12306官网支付')

	def send_notice(self):
		pass

	def run(self):
		'''运行主逻辑'''
		#查询车票
		self.check_ticket()
		#登录
		self.login()
		#确认订单
		self.confirm_order()
		#发送短信提醒
		self.send_notice()
		time.sleep(10)
		#关闭浏览器
		self.browser.quit()


if __name__ == '__main__':
	userInfo = ('18796280952','13419125342a','2019-07-30','北京','广州')
	grabtt = GrabTrainTicket(*userInfo)
	grabtt.run()



