'''
实现代码雨(code_rain)
  @datetime: 2019/7/23

----- @R2h1 ------
'''

import random
import sys
import  pygame
from pygame.locals import *

#设置显示窗口的宽与高
PANEL_WIDTH = 1280
PANEL_HEIGHT = 768


FONT_PX = 25


#初始化pygame
pygame.init()

#创建一个显示Surface，FULLSCREEN-全屏显示，32-颜色的位数
windows = pygame.display.set_mode(size=(PANEL_WIDTH,PANEL_HEIGHT),flags=FULLSCREEN,depth=32)

#从系统字体创建一个字体大小为25的 Font 对象
font = pygame.font.SysFont('browa',20)

#创建图像对象,SRCALPHA-每个像素包含一个alpha通道(灰度)
surface = pygame.Surface((PANEL_WIDTH,PANEL_HEIGHT),flags=pygame.SRCALPHA)
#修改图像对象的像素格式(生成一个Surface副本)，去掉了alpha
pygame.Surface.convert(surface)

#背景图像填充
surface.fill(pygame.Color(0,0,0,16))
#全屏显示填充
windows.fill((0,0,0))

#字母版,chr(97)-chr(122)为小写26字母
letter = [chr(i) for i in range(97,123)]

#使用font.render()创建26个字母的文本图像列表，颜色为绿色(0,255,0)
texts = [font.render(letter[i],True,(0,255,0)) for i in range(26)]

#按屏幕宽度计算在画板图像放多少列坐标的字体图像的列表
drops = [0 for i in range(int(PANEL_WIDTH/FONT_PX))]

#死循环确保窗口一直显示
while 1:
	#相当于遍历所有鼠标和键盘的事件
	for event in pygame.event.get():
		#单击关闭窗口事件，退出
		if event.type == pygame.QUIT:
			sys.exit()
		elif event.type == pygame.KEYDOWN:
			#获取键盘上所有键的状态，按下为1，否则为0
			chang = pygame.key.get_pressed()
			#按下空格键（32）事件，退出
			if (chang[32]):
				sys.exit()

	#暂停30毫秒
	pygame.time.delay(20)

	#再绘制背景到全屏图像上，左上角起始位置，遮住上一次绘制的文本图像
	windows.blit(surface,(0,0))

	#遍历每一列
	for i in range(len(drops)):
		#随机选择字母图像
		text = random.choice(texts)

		#再绘制第 i 列文本图像，blit()-将text绘制到 全屏显示Surface的(i*FONT_PX,drops[i]*FONT_PX)位置上
		windows.blit(text,(i*FONT_PX,drops[i]*FONT_PX))

		#每绘制一次文本图像，该列的代表值+1，下一次就会向下移动
		drops[i] += 1
		#当列值的10倍大于屏幕高度或者随机数大于0.95，列值重置
		if drops[i]*10 > PANEL_HEIGHT or random.random() > 0.95:
			drops[i] = 0
	#更新整个待显示的Surface对象到屏幕上
	pygame.display.flip()

#退出pygame
pygame.quit()






