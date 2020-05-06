'''
查看微信撤回消息
'''
import re
import os
import time
import itchat
import platform
from itchat.content import *


#存放接受消息的信息
msg_info = {}

#表情有一个bug，接受信息和接受note的msg_id不一致
face_package = None

#处理接受的消息，放入msg_info字典，对字典中超时消息清理以防内存占用，不存储不具有撤回功能的消息。
#微信中支持撤回的包括【文本，图片，名片，分享，语言，附件，视频，地图（位置）】
#[TEXT, PICTURE, MAP, CARD, SHARING, RECORDING, ATTACHMENT, VIDEO, FRIENDS, NOTE]
@itchat.msg_register([TEXT,PICTURE,MAP,CARD,SHARING,RECORDING,ATTACHMENT,VIDEO,FRIENDS],isFriendChat = True,isMpChat = True)
def handle_msg(msg):
	#全局变量
	global face_pacakage
	#通过格式化本地时间戳获取接受消息的时间
	msg_rev_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
	#消息发送人
	try:
		msg_from = itchat.search_friends(userName=msg['FromUserName'])['NickName']
	except:
		msg_from = '微信官方账号'
	#消息id
	msg_id =msg['MsgId']
	#发送消息的时间
	msg_send_time = msg['CreateTime']
	#消息内容
	msg_content = None
	#消息链接
	msg_url = None

	#文本或者好友邀请
	if msg['Type'] in ['Text','Friends']:
		msg_content = msg['Text']
		print('%s 发送[文本/好友邀请]: %s\n' % (msg_from,msg_content))

	#语言,附件，视频，图片
	elif msg['Type'] in ['Recording','Attachment','Video','Picture']:
		msg_content = msg['FileName']
		#保存文件
		msg['Text'](str(msg_content))
		print('%s 发送[语言/附件/视频/图片]: %s\n' % (msg_from,msg_content))

	#名片
	elif msg['Type'] == 'Card':
		msg_content = msg['RecommendInfo']['NickName'] + '的名片，'
		if msg['RecommendInfo']['Sex'] == 1:
			msg_content += '性别男。'
		else:
			msg_content += '性别女。'
		print('%s 发送[名片]: %s\n' % (msg_from,msg_content))

	#位置
	elif msg['Type'] == 'Map':
		x, y, location = re.search\
		("<location x=\"(.*?)\" y=\"(.*?)\".*label=\"(.*?)\".*", msg['OriContent']).group(1, 2, 3)
		if location is None:
			msg_content = r"纬度:" + x.__str__() + ", 经度:" + y.__str__()
		else:
			msg_content = r"" + location
		print('%s 发送[位置]: %s\n' % (msg_from,msg_content))

	#分享的
	elif msg['Type'] == 'Sharing':
		msg_content = msg['Text']
		msg_url = msg['Url']
		print('%s 发送[分享]: %s\n' % (msg_from,msg_content))

	face_package = msg_content

	#更新msg_info字典
	msg_info.update(
		{
		msg_id:{
			"msg_from": msg_from,
			"msg_send_time": msg_send_time,
			"msg_rev_time": msg_rev_time,
			"msg_type": msg["Type"],
			"msg_content": msg_content,
			"msg_url": msg_url
			}
		}
	)

#监听是否有消息撤回(NOTE)并进行相应操作
@itchat.msg_register([NOTE],isFriendChat=True,isGroupChat=True, isMpChat=True)
def send_msg_filehelper(msg):
	global face_package
	if "撤回了一条消息" in msg['Content']:
		#re匹配最后一次撤回消息的id
		recall_msg_id = re.search(r"<msgid>(.*?)</msgid>",msg['Content']).group(1)
		#读取msg_info中该id对应的消息
		recall_msg = msg_info.get(recall_msg_id)

		#撤回的是表情包
		if len(recall_msg_id) < 11:
			itchat.send_file(face_package,toUserName = 'filehelper')
			os.remove(face_package)
		else:
			msg_body = itchat.search_friends()['NickName'] +',您好：\n\n['+recall_msg.get('msg_from')+']撤回了一条'+recall_msg.get('msg_type')+\
			'消息\n' + recall_msg.get('msg_rev_time')+'\n内容如下：\n'+recall_msg.get('msg_content')
			if recall_msg['msg_type'] == 'Sharing':
				msg_body = msg_body +"\n就是这个链接：" + recall_msg.get('msg_url')

			#将撤回的消息(msg_body)发送到文件助手
			itchat.send(msg_body,toUserName = 'filehelper')

			#有文件的话也要将文件发送
			if recall_msg['msg_type'] in ['Recording','Attachment','Video','Picture']:
				file = '@fil@%s' % (recall_msg['msg_content'])
				itchat.send(msg=file, toUserName='filehelper')
				os.remove(recall_msg['msg_content'])
			print(msg_body)

			#一次撤回信息查看后删除msg_info字典中的信息
			msg_info.pop(recall_msg_id)



if __name__ == '__main__':

	#platform.platform()获取操作系统名称及版本号
	if platform.platform()[:7] == 'Windows':
		itchat.auto_login(enableCmdQR=False, hotReload=True)
	else:
		itchat.auto_login(enableCmdQR=True, hotReload=True)
	itchat.run()

