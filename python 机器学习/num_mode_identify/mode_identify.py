import numpy as np 

#数字识别类
class AutoMemory(object):

	def __init__(self,std_input_matrix):
		'''
		初始化
		'''
		#标准输入
		self.std_input_matrix = std_input_matrix
		self.weight_matrix = np.dot(self.std_input_matrix.T,self.std_input_matrix)

	def mode_visible(self,mode_number,damage_percent=0,noise_num=0):
		'''
		可视化打印
		'''
		mode_number =  np.array(mode_number).reshape(6,5)
		if damage_percent != 0:
			print("{:.0%}被遮挡:".format(damage_percent))
		if noise_num != 0:
			print("{}个噪声:".format(noise_num))
		for item in mode_number:
			num = 0
			for i in item:
				if i==1:
					print(chr(9679),end="")
				else:print(chr(9711),end= "")
				num +=1
				if num==5:
					print("\n")

	def damage(self,mode_number,damage_percent=0,noise_num=0):
		'''
		:params mode_number:标准数字矩阵
			    damage_percent:受损百分比
			    noise_num:随机噪声数
	    :return mode_number:
		'''
		#无污染
		if damage_percent == 0 and noise_num == 0:
			mode_number = mode_number
		#百分比受损
		elif damage_percent !=0 and noise_num == 0:
			damage_start = 30-round(damage_percent*6)*5
			for i in range(damage_start,30):
				mode_number[i] = -1
		#随机噪声
		elif damage_percent == 0 and noise_num != 0:
			index_list = np.random.choice(mode_number.shape[0], size=noise_num)
			for index in index_list:
				mode_number[index] = -mode_number[index]
		return mode_number	

	def mode_idetify(self,mode_number,damage_percent=0,noise_num=0):
		'''
		:params mode_number:数字矩阵
			    damage_percent:受损百分比
	    :return 识别结果
		'''
		mode_number = self.damage(mode_number,damage_percent,noise_num)
		self.mode_visible(mode_number,damage_percent,noise_num)
		liner_input = np.dot(self.weight_matrix,mode_number)
		idetify_result = np.sign(liner_input)
		print("识别结果：")
		self.mode_visible(idetify_result)
		return idetify_result	

			
		
if __name__ == '__main__':
	std_input_matrix = np.array([[-1,1,1,1,-1,1,-1,-1,-1,1,1,-1,-1,-1,1,1,-1,-1,-1,1,1,-1,-1,-1,1,-1,1,1,1,-1],
								 [-1,1,1,-1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1],
								 [1,1,1,-1,-1,-1,-1,-1,1,-1,-1,-1,-1,1,-1,-1,1,1,-1,-1,-1,1,-1,-1,-1,-1,1,1,1,1]])
	am =  AutoMemory(std_input_matrix)
	mode0,mode1,mode2 = std_input_matrix[0],std_input_matrix[1],std_input_matrix[2]
	am.mode_idetify(mode0,0.67,0)







