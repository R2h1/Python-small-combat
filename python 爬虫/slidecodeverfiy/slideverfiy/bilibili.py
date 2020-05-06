import time
import random
from io import BytesIO
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from PIL import Image

from get_tracks import creat_tracks

class Bilibili(object):

	def __init__(self):
		#创建浏览器对象
		self.driver = webdriver.Chrome()
		#隐式等待
		self.driver.implicitly_wait(3)
		self.url = 'https://passport.bilibili.com/login'
		#用户名
		self.user = '18796280952'
		#密码
		self.pwd = '13419125342a'

	def close(self):
		'''
		关闭浏览器
		'''
		self.driver.quit()

	def input_user_pwd(self):
		'''
		   输入用户名和密码
		'''
		#进入登陆页面
		self.driver.get(self.url)

		#文本框输入用户名
		tb_user = self.driver.find_element_by_id('login-username')
		tb_user.send_keys(self.user)
		#文本框输入密码
		tb_pwd = self.driver.find_element_by_id('login-passwd')
		tb_pwd.send_keys(self.pwd)

	def get_screenshot(self):
		'''
		获取屏幕截图
		'''
		screenshot = self.driver.get_screenshot_as_png()
		screenshot = Image.open(BytesIO(screenshot))

		return screenshot
	def update_style(self):
		'''
			修改图片的style属性，显示无缺口的图片
		'''
		js = 'document.querySelectorAll("canvas")[3].style="display:block"'
		self.driver.execute_script(js)
		time.sleep(2)

	def get_position(self):
		'''
			获取截取验证码时的四条边
		'''
		#定位到登陆按钮
		bt_login = self.driver.find_element_by_xpath('//a[@class="btn btn-login"]')
		#模拟点击
		bt_login.click()
		time.sleep(2)
		#获取验证码图片对象
		code_img = self.driver.find_element_by_xpath('//canvas[@class="geetest_canvas_slice geetest_absolute"]')
		time.sleep(2)

		location = code_img.location
		size = code_img.size

		#screenshot = self.get_screenshot()
		#print(screenshot.size)

		#计算图片截取区域(左上，右下，的坐标值)
		left,top,right,buttom = location['x'],location['y'],location['x']+size['width'],location['y']+size['height']
		return left,top,right,buttom




	def get_image(self):
		'''
			截取验证码图片
		'''
		#获取验证码位置
		position = self.get_position()
		#从屏幕截图中抠出有缺口的验证码图片
		captcha1 = self.get_screenshot().crop(position)
		#修改style属性，显示无缺口的验证码图片
		self.update_style()
		#从屏幕截图中抠出无缺口的验证码图片
		captcha2 = self.get_screenshot().crop(position)

		with open('captcha1.png','wb') as f1 ,open('captcha2.png','wb') as f2:
			captcha1.save(f1)
			captcha2.save(f2)

		return captcha1,captcha2

	def is_pixel_equal(self,img1,img2,x,y):
		'''
			判断两张图片的同一像素点的RGB值是否相等
		'''
		pixel1,pixel2= img1.load()[x,y],img2.load()[x,y]
		#print(pixel1,pixel2)
		#设定一个比较基准
		sub_index = 60

		#比较
		if abs(pixel1[0]-pixel2[0])< sub_index and abs(pixel1[1]-pixel2[1])< sub_index and abs(pixel1[2]-pixel2[2])< sub_index:
			return True
		else:
			return False



	def get_gap_offset(self,img1,img2):
		'''
			获取缺口的偏移量
		'''
		x = int(img1.size[0]/4.2)
		for i in range(x,img1.size[0]):
			for j in range(img1.size[1]):
				#两张图片对比,(i,j)像素点的RGB差距，过大则该x为偏移值
				if not self.is_pixel_equal(img1,img2,i,j):
					x = i
					return x
		return x


	def operate_slider(self,track):
		'''
		   拖动滑块
		'''
		#获取拖动按钮
		#trackback_tracks = [-1,-1,-2,-1]
		slider_bt = self.driver.find_element_by_xpath('//div[@class="geetest_slider_button"]')

		#点击拖动验证码的按钮不放
		ActionChains(self.driver).click_and_hold(slider_bt).perform()
		
		#print(track)

		for i in track:
			ActionChains(self.driver).move_by_offset(xoffset=i,yoffset=0).perform()
			time.sleep(random.random()/100)
		time.sleep(random.random())
		#松开滑块按钮
		ActionChains(self.driver).pause(0.5).release().perform()
		time.sleep(5)


	def do_captcha(self):
		'''
			实现处理验证码
		'''
		#有缺口，无缺口图片
		img1,img2 = self.get_image()
		#比较两个验证码图片获取验证码滑块的偏移量
		offset = self.get_gap_offset(img1,img2)
		print(offset)

		#使用偏移值计算移动操作
		tracks = creat_tracks(offset-5,12,3)

		#操作滑块按钮，模拟拖动滑块做验证登录
		self.operate_slider(tracks)

	def login(self):
		'''
		实现主要的登陆逻辑
		'''
		#来到登陆界面并输入账号密码
		self.input_user_pwd()
		#处理验证码
		self.do_captcha()
		time.sleep(10)
		#关闭浏览器
		self.close()

	def run(self):
		self.login()



if __name__ == '__main__':
	bili =Bilibili()
	bili.run()

