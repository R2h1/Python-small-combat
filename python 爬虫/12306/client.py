import sys

from PyQt5.QtWidgets import QApplication,QWidget,QDesktopWidget,QMessageBox,QPushButton
from PyQt5.Qt import QLineEdit
#抢票界面
class ClientUI(QWidget):
	def __init__(self):
		super().__init__()
		#UI界面绘制方法
		self.initUI()

	def initUI(self):
		#窗口显示在屏幕中央
		self.center()
		#设置窗口大小为宽500，高300
		self.resize(500,300)
		#窗口标题
		self.setWindowTitle('抢票软件V1.0')
		#查询刷票按钮
		qy = QPushButton("刷票",self)
		qy.resize(40,30)
		qy.move(450,80)
		#登录按钮
		lbt = QPushButton('登录',self)
		lbt.resize(40,30)
		lbt.move(400,20)
		#验证码图片按钮
		vbt = QPushButton('选择验证码',self)
		vbt.resize(80,30)
		vbt.move(300,20)


		#创建文本框
		username = QLineEdit(self)
		username.resize(100, 30)
		username.move(20, 20)
		password = QLineEdit(self)
		password.resize(100, 30)
		password.move(140, 20)

		# 按钮点击事件关联
		#self.button.clicked.connect(self.on_click)

		#显示在屏幕上
		self.show()
		
   
	def center(self):
		#获得窗口
		qr = self.frameGeometry()
		#获得屏幕中心点
		cp = QDesktopWidget().availableGeometry().center()
		#显示到屏幕中心
		qr.moveCenter(cp)
		self.move(qr.topLeft())
	#关闭事件的弹窗
	def closeEvent(self, event):
		reply = QMessageBox.question(self, 'Message',
			"关闭程序？", QMessageBox.Yes | 
			QMessageBox.No, QMessageBox.Yes)
		if reply == QMessageBox.Yes:
			event.accept()
		else:
			event.ignore()   

if __name__ == '__main__':
	#创建pyqt5应用程序
	app = QApplication(sys.argv)
	#创建UI对象
	ex = ClientUI()
	#执行应用程序并由系统干净退出
	sys.exit(app.exec_()) 
