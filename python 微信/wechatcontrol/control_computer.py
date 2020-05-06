import os
import itchat
from PIL import ImageGrab
import cv2



#使用指南
usehelpMsg = "使用方法：\n\
    1.运行CMD命令：cmd xxx(xxx为命令):\n\
    例如-关机命令：cmd shutdown -s -t 0 \n\
    2.电脑摄像头进行拍照：cap\n\
    3.获取屏幕截屏：pc"

#处理消息
@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
	message = msg['Text']
	toName = msg['ToUserName']
	# 临时保存截屏图片地址
	path ='temp.jpg' 

	if toName == 'filehelper':

		#调用电脑摄像头拍摄
		if message == 'cap':
			# 要使用摄像头，需要使用cv2.VideoCapture(0)创建VideoCapture对象，
			# 参数：0指的是摄像头的编号。如果你电脑上有两个摄像头的话，访问第2个摄像头就可以传入1
			cap = cv2.VideoCapture(0)
			#获取一帧
			ret,img = cap.read()
			cv2.imwrite('wechatTemp.png',img)
			#发送照片给文件助手
			itchat.send('@img@%s'%'wechatTemp.png','filehelper')
			#释放资源
			cap.release()

		#屏幕截图
		if message == "pc":  # 截图
			# 实现截屏功能
			image = ImageGrab.grab()  
			image.save(path, 'JPEG')  # 设置保存路径和图片格式
			itchat.send_image(path, 'filehelper')
			
		#cmd命令控制电脑
		if message[0:3] == 'cmd':
			os.system(message.strip(message[0:4]))

if __name__ == '__main__':
	itchat.auto_login(hotReload = True)
	itchat.send(usehelpMsg,'filehelper')
	itchat.run()
