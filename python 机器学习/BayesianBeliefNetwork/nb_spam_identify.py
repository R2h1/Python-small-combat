# -*- coding: utf-8 -*-
import numpy as np
import random
import re

def txt_parse(filepath,is_spam=False):
	'''
	读取邮件内容生成带个内容词条
	:params filepath:邮件.txt所在路径
	:params is_spam:是否为垃圾邮件
	：return 带标签的内容词条
	'''
	content = open(filepath,"r").read()
	tokens_list = re.split(r"\W+",content)
	txt_item = [item.lower() for item in tokens_list if len(item)>0]
	if is_spam:
		txt_item.append(1)
	else:
		txt_item.append(0)
	return txt_item

def creat_entry_lists():
	'''
	生成邮件词条完整列表
	:return txt_list:邮件词条列表
	'''
	txt_list = []
	for i in range(1,26):
		spam_item = txt_parse("spam/{}.txt".format(i),is_spam=True)
		txt_list.append(spam_item)
		ham_item = txt_parse("ham/{}.txt".format(i),is_spam=False)
		txt_list.append(ham_item)
	return txt_list

def creat_only_voclist(txt_list):
	'''
	生成邮件特征列表
	:params txt_list:完整邮件样本
	:return vocab_only_list:邮件特征列表
	'''
	vocab_only_list = set([])
	for item in txt_list:
		vocab_only_list = vocab_only_list | set(item[:-1])
	vocab_only_list = list(vocab_only_list)
	return vocab_only_list

def make_input_vector(vocab_only_list, txt_list):
	'''
	由特征词汇表邮件样本特征化0或1
	:params vocab_only_list:特征词汇表
	:params txt_list:邮件样本列表
	:return return_vector :特征化列表
	'''
	vocab_character_list = []
	for item in txt_list:
		return_vector = [0]*len(vocab_only_list)
		for word in item[:-1]:
			if word in vocab_only_list:
				return_vector[vocab_only_list.index(word)] += 1
		if item[-1]:
			return_vector.append(1)
		else:
			return_vector.append(0)
		vocab_character_list.append(return_vector)
	return vocab_character_list

def creat_data_set(vocab_character_list):
	'''
	随机挑选10个作为测试集，剩下40个作为训练集
	:params vocab_character_list:特征化列表
	:return train_set:训练集
	:return test_set:测试集
	'''
	test_set = []
	for i in range(10):
		test_set_index = int(random.uniform(0, len(vocab_character_list)))
		test_set.append(vocab_character_list[test_set_index])
		del(vocab_character_list[test_set_index])
	train_set = vocab_character_list
	return train_set,test_set

def train_bys(train_set):
	'''
	朴素贝叶斯训练函数
	:params train_set:训练集
	:return p0_list:非垃圾邮件条件概率列表
			p1_list:垃圾邮件条件概率列表
			p1_mail:垃圾邮件概率
	'''
	train_set = np.array(train_set)
	num_total_mail = len(train_set)
	class_list = [item[-1] for item in train_set]
	p1_mail = sum(class_list)/float(num_total_mail)
	num_words = len(train_set[0])-1
	p0_num_array = np.ones(num_words)
	p1_num_array = np.ones(num_words)
	p0_denom = 2.0
	p1_denom = 2.0
	for i in range(num_total_mail):
		chara_item = train_set[i][:-1]
		if class_list[i] == 0:
			#计算非垃圾邮件每个单词出现频数
			p0_num_array += chara_item
			p0_denom += sum(chara_item)
		else:
			#计算垃圾邮件每个单词出来频数
			p1_num_array += chara_item
			p1_denom += sum(chara_item)
	#计算非垃圾邮件与垃圾邮件每个单词的条件概率		     
	p0_list = np.log(p0_num_array/p0_denom)
	p1_list = np.log(p1_num_array/p1_denom)
	return p0_list,p1_list,p1_mail


def test_bys(test_set,p0_list,p1_list,p1_mail):
	'''
	朴素贝叶斯垃圾邮件分类函数
	;params test_set:待分类测试集
			p0_list:非垃圾邮件条件概率列表
			p1_list:垃圾邮件条件概率列表
			p1_mail:
	'''
	test_set = np.array(test_set)
	err_count = 0
	is_spam = 0
	for item  in test_set:
		test_chara = item[:-1]
		p0 = sum(test_chara * p0_list) + np.log(1.0 - p1_mail)
		p1 = sum(test_chara * p1_list) + np.log(p1_mail)
		if p1 > p0:
		   is_spam = 1   
		else: 
		   is_spam = 0
		if is_spam != item[-1]:
			err_count += 1
			print("识别错误邮件：",test_chara)
	print("识别错误率：{:.2%}".format(float(err_count) / len(test_set)))

def nb_spam_identify():
	'''
	朴素贝叶斯垃圾邮件识别函数
	'''
	txt_list =  creat_entry_lists()
	vocab_only_list = creat_only_voclist(txt_list)
	vocab_character_list = make_input_vector(vocab_only_list,txt_list)
	train_set,test_set = creat_data_set(vocab_character_list)
	p0_list,p1_list,p1_mail = train_bys(train_set)
	test_bys(test_set,p0_list,p1_list,p1_mail)


if __name__ == '__main__':
	nb_spam_identify()


