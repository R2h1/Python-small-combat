import numpy as np 
import operator
from collections import namedtuple,Counter

#训练集数据个数和特征矩阵
tr_dataSet = namedtuple("tr_dataSet",('trArrLen','trCharctMat'))
#特征归一化矩阵
tr_nomoSet = namedtuple('tr_nomoSet',('normalCharctMat','rangeVals','minVals'))

def knnClassfiy(test,dataSet,labels,k):
	'''
	KNN分类器
	:params test:待分类元组
			dataSet:数据集元组
			labels:标签
			k:k值
	:return resLable: 
	'''
	#测试集复制trSize个，与测试集作差，然后平方求和再开放，返回列表
	distances = (((test - dataSet)**2).sum(axis=1))**0.5
	#取前k个距离最近的类别
	klables = [labels[index] for index in distances.argsort()[0:k]]
	#计数器Counter，对列表中元素出现次数计数，most_common(n)返回出现次数前n个(元素,次数)元组
	resLable = Counter(klables).most_common(1)[0][0]
	#返回 测试结果
	return resLable

def dataParse(filename):
	'''
	数据解析
	:params filename:数据集文本
	:return tr_dataSet: 数据集元组(元组个数,数据集特征矩阵)
	'''
	with open(filename) as f:
		dataLists = f.readlines()
	arrLen = len(dataLists)
	charctMat = np.zeros((arrLen,4))
	index = 0
	for line in dataLists:
		stdLine = line.strip().split('\t')
		classLable = stdLine[-1]
		if classLable == "didntLike":
			stdLine[-1] = 1
		elif classLable == "smallDoses":
			stdLine[-1] =2
		elif classLable == "largeDoses":
			stdLine[-1] =3
		charctMat[index,:] = stdLine[0:4]
		index += 1
	return tr_dataSet(arrLen,charctMat)

def toNormal(charctMat):
	'''
	特征归一化
	:params charctMat:待归一化特征矩阵
	:return tr_nomoSet: 信息元组(特征归一化矩阵,原取值范围,原最小值)
	'''
	minVals,maxVals = charctMat.min(0),charctMat.max(0)
	rangeVals = (maxVals-minVals)
	rangeVals[3],minVals[3] = 1,0
	normalCharctMat = (charctMat-minVals)/rangeVals
	return tr_nomoSet(normalCharctMat,rangeVals[:3],minVals[:3])


if __name__ == '__main__':
    #训练集的特征矩阵(包括标签)
	trArrLen,trCharctMat = dataParse("datingTestSet.txt")
	#归一化特征矩阵，特征范围，特征最小值
	normalCharctMat,rangeVals,minVals = toNormal(trCharctMat)
	tsRat = 0.10
	tsNum = int(trArrLen*tsRat)
	trNum = trArrLen-tsNum
	errNum = 0
	for i in range(tsNum):
		resLable = knnClassfiy(normalCharctMat[i,0:3],normalCharctMat[:trNum,0:3],normalCharctMat[:trNum,3],4)
		if resLable != normalCharctMat[i,3]:
			print("(第{}个分类错误)分类类别：{} \t 真实类别：{}".format(i,resLable,normalCharctMat[i,3]))
			errNum += 1
		# else:
		# 	print("(分类正确)分类类别：{} \t 真实类别：{}".format(resLable,normalCharctMat[i,3]))
	print("错误率：{:.2%}".format(float(errNum)/tsNum))
	resList = ['讨厌','有点喜欢','非常喜欢']
	#(飞行里程数,视频游戏百分比,冰淇淋公升数)
	flyMiles,precentGame,iceCream = (44000,12,0.5)
	print("对于一位每年飞行里程数:{}公里,视频游戏百分比:{}%,每周冰淇淋公升数:{}升的男性".format(flyMiles,precentGame,iceCream))
	inputArr = np.array([flyMiles, precentGame, iceCream])
	normlInputArr = (inputArr - minVals) / rangeVals
	resLable = knnClassfiy(normlInputArr,normalCharctMat[:trArrLen,0:3],normalCharctMat[:trArrLen,3],4)
	print("你可能{}这个人".format(resList[int(resLable)-1]))





