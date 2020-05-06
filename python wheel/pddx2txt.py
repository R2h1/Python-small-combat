# coding=utf-8

"""
Description: DOC,DOCX,PDF文件转化TXT文本
    
    -----@R2h----

"""

import os,fnmatch,time
from win32com import client as wc


def tranType(self,filename):
    '''
    由文件后缀修改文件名
    :params filename:原文件名
    :return new_filename :修改后新文件名
    '''
    new_filename = None
    if fnmatch.fnmatch(filename.lower(),'*.pdf') or fnmatch.fnmatch(filename,'*.doc'):
        new_filename = filename[:-4]+'.txt'
    elif fnmatch.fnmatch(filename,'*.docx'):
        new_filename = filename[:-5]+'.txt'
    else:
        print('警告：您输入[',typename,']不合法，本工具支持pdf/doc/docx格式,请输入正确格式。')
        return
    print('新的文件名：',new_filename)
    return new_filename

'''
pddx2Txt:pdf/doc/docx to txt的简写
'''
def pddx2Txt(self,filePath,savePath=None):
    '''
    doc,docx,pdf文件转txt
    :params filePath: 文件路径  
            savePath: 指定保存路径
    '''
    dirs,filename = os.path.split(filePath)
    new_filename = self.tranType(filename)

    if savePath is None: 
        savePath = dirs
    else:
        savePath = savePath
    txt_newpath = os.path.join(savePath,new_name)
    print('保存路径：',txt_newpath)

    #加载处理应用,/doc/docx/pdf转化txt
    try:
        wordapp = wc.Dispatch('Word.Application')
    except Exception as e:
        wordapp = wc.Dispatch('kwps.Application')
    mytxt = wordapp.Documents.Open(filePath)
    mytxt.SaveAs(txt_newpath,4) #参数4表示提取文本
    mytxt.Close()



'''
遍历目录，对子文件单独处理
'''
class TraversalFun(object):
    
    def __init__(self,rootDir,func=None,saveDir=None):
        '''
        初始化
        :params rootDir:待处理文件夹和文件所在目录
                func:参数方法
                saveDir:保存路径
        '''
        self.rootDir = rootDir 
        self.func = func   
        self.saveDir = saveDir 

    def TraversalDir(self):
        '''
        遍历目录文件
        '''
        dirs,filename = os.path.split(self.rootDir)
        print(dirs)

        # 保存目录
        save_dir = None
        if self.saveDir == None: 
            save_dir = os.path.abspath(os.path.join(dirs,'new_'+filename))
        else: save_dir = self.saveDir
        # 创建目录文件
        if not os.path.exists(save_dir): os.makedirs(save_dir)
        print("保存目录："+save_dir)

        # 遍历文件并将其转化txt文件
        self.AllFiles(self.rootDir,save_dir)


   
    def AllFiles(self,rootDir,save_dir=None):
        '''
        递归遍历所有文件，并提供具体文件操作功能
        ：params rootDir：根目录
                 save_dir: 保存目录
        '''
        # 返回指定目录包含的文件或文件夹的名字的列表
        for lists in os.listdir(rootDir):
            # 待处理文件夹名字集合
            path = os.path.join(rootDir, lists)

            # 核心算法，对文件具体操作
            if os.path.isfile(path):
                self.func(os.path.abspath(path),os.path.abspath(save_dir))

            # 递归遍历文件目录
            if os.path.isdir(path):
                newpath = os.path.join(save_dir, lists)
                if not os.path.exists(newpath):
                    os.mkdir(newpath)
                #递归遍历
                self.AllFiles(path,newpath)



if __name__=='__main__':
    time_start=time.time()

    # 根目录文件路径
    rootDir = r"../dataSet/Corpus/EnPapers"
    # saveDir = r"../dataSet/Corpus/TxtEnPapers"
    tra=TraversalFun(rootDir,pddx2Txt,saveDir) # 默认方法参数打印所有文件路径
    tra.TraversalDir()                   # 遍历文件并进行相关操作

    time_end=time.time()
    print('totally cost',time_end-time_start,'s')