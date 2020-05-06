#numpy导入自然指数，创建矩阵，产生随机数，矩阵乘法的方法
from numpy import exp,array,random,dot

class NeuralNetwork(object):

	def __init__(self):

		#指定随机数发生器种子，保证每次获得相同结果的随机数
		random.seed(1)
		#对含有3个输入一个输出的单个神经元建模
		#即3*1矩阵(树突)赋予随机权重值。范围（-1，1）
		#即（a，b)范围的c*d矩阵随机数为（b-a）*random.random((c,d))+a
		self.dendritic_weights = 2*random.random((3,1))-1

	#Sigmoid函数，s形曲线，用于对输入的加权总和x做(0,1)正规化
	#它可以将一个实数映射到(0,1)的区间
	def __sigmoid(self,x):
		return 1/(1+exp(-x))

	#Sigmoid函数的导数（梯度）（当前权重的置信程度，越小代表越可信）
	#这里的x指的是1/(1+exp(-x))，即output输出
	def __sigmoid_derivative(self,x):
		return x*(1-x)

	#训练该神经网络，并调整树突的权重
	def train(self,training_inputs,training_outputs,number_of_training_iterations):
		'''
		training_inputs：训练集样本的输入
		training_outputs：训练集样本的输出
		number_of_training_iterations：训练次数
		1.我们使用Sigmoid曲线计算（输入的加权和映射到0至1之间）作为神经元的输出
		2.如果输出是一个大的正（或负）数，这意味着神经元采用这种（或另一种）方式，
		3.从Sigmoid曲线可以看出，在较大数值处，Sigmoid曲线斜率（导数）小，即认为当前权重是正确的，就不会对它进行很大调整。
		4.所以，乘以Sigmoid曲线斜率便可以进行调整
		'''
		for iteration in range(number_of_training_iterations):
			#训练集导入神经网络
			output = self.think(training_inputs)

			#计算误差（实际值与期望值的差）
			error = training_outputs - output

			#将误差乘以输入，再乘以S形曲线的梯度(默认学习率为1，偏置值为0)
			adjustment = dot(training_inputs.T,error*self.__sigmoid_derivative(output))

			#对树突权重进行调整
			self.dendritic_weights += adjustment

		#神经网络
	def think(self,inputs):

		#输入与权重相乘并正规化
		return self.__sigmoid(dot(inputs,self.dendritic_weights))




if __name__ == '__main__':
	#初始化神经网络nn
	nn = NeuralNetwork()
	#初始权重
	print("初始树突权重：{}".format(nn.dendritic_weights))

	#训练集，四个样本，每个样本有3个输入，1个输出
	#训练样本的输入
	training_inputs_sample = array([[0,0,1],
									[1,1,1],
									[1,0,1],
									[0,1,1]])
	#训练样本的输出
	training_outputs_sample = array([[0,1,1,0]]).T
	print(training_outputs_sample)

	#用训练集训练nn，重复一万次，每次做微小的调整
	nn.train(training_inputs_sample,training_outputs_sample,100000)

	#训练后的树突权重
	print("训练后树突权重：{}".format(nn.dendritic_weights))

	#用新数据进行测试
	test_result = nn.think(array([1,0,0]))
	print('测试结果：{}'.format(test_result))




