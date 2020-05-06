import numpy as np
import operator
from os import listdir
from sklearn.neighbors import KNeighborsClassifier


def dataVector(filename,label):
	with open(filename) as f:
		lines = f.readlines()
	resVector = np.zeros((1,1025))
	lineNum = 0
	for line in lines:
		for index,digit in enumerate(line):
			if index == 32 :
				continue
			resVector[0,lineNum*32+index] = int(digit)
		lineNum += 1
	resVector[0,1024] = label
	return resVector
			
def hardwritingMat(fileDir):
	dataDir = listdir(fileDir)
	dataTxtNum = len(dataDir)
	dataMat = np.zeros((dataTxtNum,1025))
	for index,item in enumerate(dataDir):
		label = item.split("_")[0]
		dataMat[index,:] = dataVector(fileDir+"/{}".format(item),label)
	return dataMat,dataDir

if __name__ == '__main__':
	#构建模型
	trDataMat,trDataDir = hardwritingMat('trainingDigits')
	kneigh = KNeighborsClassifier(n_neighbors=3,algorithm='auto')
	kneigh.fit(trDataMat[:,0:1024],trDataMat[:,1024])
	#模型测试
	tsDataMat,tsDataDir = hardwritingMat('testDigits')

	tsDataNum = tsDataMat.shape[0]
	errNum = 0
	for i in range(tsDataNum):
		resDigit = kneigh.predict([tsDataMat[i,0:1024]])[0]
		if resDigit != tsDataMat[i,1024]:
			errNum += 1
			print("({}识别错误)识别结果为{}，真实结果为{}".format(tsDataDir[i],resDigit,tsDataMat[i,1024]))
	print("识别错误率为{:2%}".format(float(errNum)/tsDataNum))



