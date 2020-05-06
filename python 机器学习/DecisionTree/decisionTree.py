# -*- coding: UTF-8 -*-
from math import log
 

def createDataSet():
    '''
    生成测试数据
    '''
    dataSet = [[0, 2, 0, 0, 'no'],         #数据集
               [0, 2, 0, 1, 'no'],
               [1, 2, 0, 0, 'yes'],
               [2, 1, 0, 0, 'yes'],
               [2, 0, 1, 0, 'yes'],
               [2, 0, 1, 1, 'no'],
               [1, 0, 1, 1, 'yes'],
               [0, 1, 0, 0, 'no'],
               [0, 0, 1, 0, 'yes'],
               [2, 1, 1, 0, 'yes'],
               [0, 1, 1, 1, 'yes'],
               [1, 1, 0, 1, 'yes'],
               [1, 2, 1, 0, 'yes'],
               [2, 1, 0, 1, 'no']]

    labels = ['no', 'yes']             #分类属性
    return dataSet, labels                #返回数据集和分类属性
 
def calcShannonEnt(dataSet):
    '''
    计算香农熵
    '''
    #数据集的数量
    sampleNum = len(dataSet)  
    #标签(Label)出现次数的字典                      
    labelCounts = {}                     
    for item in dataSet:
        #Label计数                   
        labelCounts[item[-1]] = labelCounts.get(item[-1],0)+1
    shannonEnt = 0.0      #样本经验熵(香农熵)                   
    for key in labelCounts:
        #标签概率                           
        prob = float(labelCounts[key]) / sampleNum
        #公式香农熵计算 -p(xi)log2(p(xi))求和，xi为类别
        shannonEnt -= prob * log(prob, 2)           
    return shannonEnt                                #返回经验熵(香农熵）


def splitDataSet(dataSet, axis, value):
    """
    按照给定特征划分数据集
    :params dataSet:待划分的数据集
            axis:划分数据集的特征
            value:需要返回的特征的值
    :return retDataSet:结果数据集
    """   
    retDataSet = []                              
    for item in dataSet:
        if item[axis] == value:  
            retDataSet.append(item)
    return retDataSet                               
 

def chooseBestFeatureToSplit(dataSet):
    """
    选择最优特征
    :params dataSet:数据集
    :returns bestFeature:信息增益最大的(最优)特征的索引值
    """
    #特征数
    CharctNum = len(dataSet[0]) - 1
    #计算数据集的香农熵               
    sampleShannonEnt = calcShannonEnt(dataSet)
    #信息增益                
    bestInfoGain = 0.0
    #最优特征的索引值                               
    bestFeature = -1
    #遍历所有特征                                
    for i in range(CharctNum):                        
        #获取dataSet的第i个特征的不同的几种值
        unqFeatList = set([item[i] for item in dataSet])
        #经验条件熵
        newEntropy = 0.0
        #计算经验条件熵                            
        for value in unqFeatList:
            #第i个特征取值value,取出第等于value的样本构成子集                         
            subDataSet = splitDataSet(dataSet, i, value)         #subDataSet划分后的子集
            prob = len(subDataSet) / float(len(dataSet))           #计算子集的概率
            newEntropy += prob * calcShannonEnt(subDataSet)     #根据公式计算经验条件熵
        #计算信息增益 
        infoGain = sampleShannonEnt - newEntropy                    
        print("第{}个特征的增益为{:.3f}".format(i, infoGain))            #打印每个特征的信息增益
        if infoGain > bestInfoGain:                             #计算信息增益
            bestInfoGain = infoGain                             #更新信息增益，找到最大的信息增益
            bestFeature = i                                     #记录信息增益最大的特征的索引值
    return bestFeature                                            #返回信息增益最大的特征的索引值
 
if __name__ == '__main__':
    dataSet, features = createDataSet()
    print("最优特征索引值:" + str(chooseBestFeatureToSplit(dataSet)))