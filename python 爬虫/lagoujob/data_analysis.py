import pickle,os,re
#柱状图，饼图，漏斗图，配置
from pyecharts.charts import Bar,Pie,Funnel
from pyecharts import options
#主题
from pyecharts.globals import ThemeType



#读取数据
def read_data(path):
	with open(path,'rb') as f:
		return pickle.load(f)

#柱状图
def drawbar(title,data,savepath):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	bar = (Bar(init_opts=options.InitOpts(theme=ThemeType.LIGHT))
		.add_xaxis([i for i,j in data.items()])
		.add_yaxis('平均薪资',[j for i,j in data.items()])
		.reversal_axis()
		.set_series_opts(label_opts=options.LabelOpts(position="right"))
		.set_global_opts(title_opts=options.TitleOpts(title),
			toolbox_opts=options.ToolboxOpts(),
			xaxis_opts=options.AxisOpts(name="平均薪资",axislabel_opts=options.LabelOpts(formatter="{value}k")),
			yaxis_opts=options.AxisOpts(
				name='城市'
            )))
	bar.render(os.path.join(savepath,'{}.html'.format(title)))


def drawpie(title,data,savepath):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	pie = (Pie()
		.add("", list(zip([i for i,j in data.items()],[j for i, j in data.items()])))
        .set_global_opts(title_opts=options.TitleOpts(title=title)
        	,toolbox_opts=options.ToolboxOpts())
        .set_series_opts(label_opts=options.LabelOpts(formatter="{b}:{d}%")))
	pie.render(os.path.join(savepath,'{}.html'.format(title)))



def drawfunnel(title,data,savepath):
	if not os.path.exists(savepath):
		os.mkdir(savepath)
	pie = (Funnel()
		.add("", list(zip([i for i,j in data.items()],[j for i, j in data.items()])),
			label_opts=options.LabelOpts(position='inside'))
        .set_global_opts(title_opts=options.TitleOpts(title=title),
        	toolbox_opts=options.ToolboxOpts(),
        	legend_opts=options.LegendOpts( pos_left='20px',pos_top='40px',orient='vertical')))
	pie.render(os.path.join(savepath,'{}.html'.format(title)))



if __name__ == '__main__':
	salaryDict={}
	data = read_data('info.pkl')
	print(data)
	for key ,value in data.items():
		average=0
		num=0
		for item in value:
			num +=1
			salary = item[-1].split('-')
			try:
				#该城市其中一个职位的平均薪资
				avr_salary = (float(salary[0].replace('k','').replace('K',''))+
					float(salary[1].replace('k','').replace('K','')))/2
			except:
				continue
			#该城市职位累计薪资
			average +=avr_salary
		salaryDict[key] = round(average/num,2)
	drawbar('各大城市python相关职位平均薪资柱状图',salaryDict,'./python_job_analysis')


	eduDict = {}
	for key ,value in data.items():
		for item in value:
			edu = item[-3]
			if edu in eduDict:
				eduDict[edu] +=1
			else:
				eduDict[edu]=1
	drawpie('各大城市python相关职位学历要求',eduDict,'./python_job_analysis')


	companySizeDict = {}
	for key, value in data.items():
		for item in value:
			companySize = item[5]
			if companySize in companySizeDict:
				companySizeDict[companySize] += 1
			else:
				companySizeDict[companySize] = 1
	drawfunnel('各大城市招聘Python相关岗位的公司规模', companySizeDict, './python_job_analysis')


