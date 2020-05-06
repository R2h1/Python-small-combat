from itertools import combinations

# 导入数据，并剔除支持度计数小于min_support的1项集
def load_data(data):
    I_dict = {}
    for i in data:
        for j in i:
            I_dict[j] = I_dict.get(j, 0) + 1
    F_dict = {}
    for k,v in I_dict.items():
        F_dict[k] = v
    for k in I_dict.keys():
        if F_dict.get(k) < min_support:
            del F_dict[k]
    return F_dict


# 判断频繁项集是否大于min_support
def get_support_set(p_set):
    item_supp_set = []
    for item in p_set:
        count = 0
        for ds in data_set:
            if item.issubset(ds):
                count += 1
        print("{}:{}".format(item,count))
        if count >= min_support:
            item_supp_set.append([item, count])
    return item_supp_set


# 找出所有频繁项集
# 以二项集为初始集
def get_all_items(two_set, k=3):
    all_frequent = []
    flag = True
    while flag:
        mid_set = []
        temp = []
        t_ = [ks[0] for ks in two_set]
        for kk in t_:
            for tt in kk:
                if tt not in temp:
                    temp.append(tt)
        k_ = [set(t) for t in combinations(temp, k)]
        for ff in k_:
            count_k = 0
            for d in t_:
                if ff.issuperset(d):
                    count_k += 1
            if count_k == k:
                mid_set.append(ff)
        frequent_mid_set = get_support_set(mid_set)
        if mid_set:
            k += 1
            two_set = frequent_mid_set
            all_frequent.extend(frequent_mid_set)
        else:
            flag = False
    return all_frequent


if __name__ == '__main__':
    data = [['I1', 'I2', 'I3'],
            ['I1', 'I2', 'I4'],
            ['I1','I2','I5'],
            ['I1', 'I2'],
            ['I1', 'I3'],
            ['I2', 'I4'],
            ['I2', 'I5'], 
            ['I1', 'I5'],
            ['I1', 'I4'],
            ['I1', 'I2', 'I4', 'I5'],
            ]
    data_set = [set(d) for d in data]
    min_support = 2
    one = [[{lk}, lv] for lk, lv in load_data(data).items()]
    two = [set(t) for t in combinations(list(load_data(data).keys()), 2)]
    print("候选集：")
    two_f_set = get_support_set(two)
    all_frequent_set = one + two_f_set + get_all_items(two_f_set)
    print("频繁项目集：")
    for afs in all_frequent_set:
        print(afs)