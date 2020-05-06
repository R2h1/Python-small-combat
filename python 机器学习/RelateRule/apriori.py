'''
Apriori算法关联规则
'''
from itertools import combinations

# from copy import deepcopy

#导入数据并剔除小于minsup_count的1-项集合
def candidate_count(data):
	print(data)
	k_set = {}
	for i in data:
		for j in i:
			k_set[j] = k_set.get(j,0) +1
	#复制
	# c_set = deepcopy(k_set)
	c_set = {}
	for k,v in k_set.items():
		c_set[k] = v
	#剔除小于minsup_count的
	for key in k_set.keys():
		if k_set.get(key) < minsup_count:
			del c_set[key]
	return c_set


# 判断频繁项集是否大于minsup_count
def get_support_set(p_set):
    item_supp_set = []
    for item in p_set:
        count = 0
        for ds in data_set:
        	#item是da的子集，计数
            if item.issubset(ds):
                count += 1
        #大于最小支持数
        if count >= minsup_count:
            item_supp_set.append([item, count])
    return item_supp_set


if __name__ == '__main__':
	dataD = [['I1','I2','I5'],
			   ['I2','I4'],
			   ['I2','I3'],
			   ['I1','I2','I4'],
			   ['I1','I3'],
			   ['I2','I3'],
			   ['I1','I3'],
			   ['I1','I2','I3','I5'],
			   ['I1','I2','I3']]
	data_set = [set(d) for d in dataD]
	minsup_count = 2
	one_set = candidate_count(dataD)
	one_f_set = [[{k},v] for k,v in one_set.items()]




