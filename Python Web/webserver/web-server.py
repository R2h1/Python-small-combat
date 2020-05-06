'''
简单的web服务器
'''

import os,sys
import subprocess
from http.server import BaseHTTPRequestHandler,HTTPServer


class base_case(object):
	'''
	条件处理基类
	'''
	#文件处理
	def handle_file(self,handler,full_path):
		try:
			with open(full_path,'r') as r:
				content = r.read()
			content = handler.create_page(content)
			handler.send_content(content.encode('utf-8'))

		except IOError as msg:
			msg = "'{0}' cannot be read :{1}".format(handler.path,msg)
			handler.handle_error(msg)

	def index_path(self,handler):
		return os.path.join(handler.full_path,'index.html')

	#断言方法，由子类实现
	def test(self,handler):
		assert False,'Not implemented'

	def act(self,handler):
		assert False,'Not implemented'


class cass_no_path(base_case):
	'''
	路径不存在
	'''
	def test(self,handler):
		return not os.path.exists(handler.full_path)
	def act(self,handler):
		raise ServerException("'{0}' not found".format(handler.path))


class case_cgi_file(object):
	'''
	可执行脚本
	'''
	def run_cgi(self,handler):
		#获取脚本输出
		content = subprocess.check_output(["python",handler.full_path],shell=False)
		handler.send_content(content)

	#判断目标路径是否为py文件
	def test(self,handler):
		return os.path.isfile(handler.full_path) and handler.full_path.endswith('.py')

	def act(self,handler):
		self.run_cgi(handler)


class cass_is_file(base_case):
	'''
	路径是文件
	'''
	def test(self,handler):
		return os.path.isfile(handler.full_path)
	def act(self,handler):
		self.handle_file(handler,handler.full_path)


class case_directory_index_file(object):

	#判断目标路径是否是目录and目录下是否有index.html
	def test(self,handler):
		return os.path.isdir(handler.full_path) and os.path.isfile(self.index_path(handler))
	
	def act(self,handler):
		self.handle_file(handler,self.index_path(handler))


class cass_other(base_case):
	'''
	其他情况
	'''
	def test(self,handler):
		return True
	def act(self,handler):
		raise ServerException("Unknown object '{0}'".format(handler.path))


class ServerException(Exception):
	'''服务器内部错误'''
	pass


class RequestHandler(BaseHTTPRequestHandler):
	'''
	处理请求并返回页面
	'''
	#注意这里的顺序，需要先判断是否是需要执行的脚本文件，再判断是否为普通文件
	CASES = [cass_no_path(),case_cgi_file(),cass_is_file(),case_directory_index_file(),cass_other()]
	
	Error_Page = '''\
		<html>
		<body>
		<h1>Error accessing {path}</h1>
		<p>{msg}</p>
		</body>
		</html>
	'''

	#异常响应
	def handle_error(self,msg):
		content = self.Error_Page.format(path=self.path,msg=msg)
		self.send_content(content.encode('utf-8'),404)


	#处理GET请求
	def do_GET(self):
		try:
			#文件完整路径
			self.full_path = os.getcwd() + self.path

			#遍历条件类
			for case in self.CASES:
				if case.test(self):
					case.act(self)
					break

		except Exception as msg:
			self.handle_error(msg)

	#index.html的页面设计
	def create_page(self,content):
		values = {
			'date_time':self.date_time_string(),
			'client_host':self.client_address[0],
			'client_port':self.client_address[1],
			'command':self.command,
			'path':self.path
		}
		content = content.format(**values)
		return content

	#发送响应内容给客户端
	def send_content(self,content,status=200):
		self.send_response(status)
		self.send_header('Content-Type','text/html')
		self.send_header('Content-Length',str(len(content)))
		self.end_headers()
		self.wfile.write(content)

if __name__ == '__main__':
	serverAddress = ('',8080)
	server = HTTPServer(serverAddress,RequestHandler)
	server.serve_forever()

