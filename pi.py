import random

def pai(times):
	'''
	:param x:实验次数
	:return :圆周率pi
	'''
	cir = 0
	for i in range(times):
		x = random.uniform(0,1)
		y = random.uniform(0,1)
		if x**2+y**2<1:
			cir += 1
	return 4*cir/times

if __name__ == '__main__':
	PI= round(pai(500000),2)
	print(PI)