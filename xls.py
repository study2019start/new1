import os
import xlrd
import xlwt

class xlsread(object):
    def __init__(self,path):
       self.p=path


    def readx(self):
        book = xlrd.open_workbook(self.p)
        sheet = book.sheet_by_index(0)
        ro=sheet.nrows
        lo=sheet.ncols
        da=[]
        for row in range(0,ro):
            sa=[]
            for l in range(0,lo):
                sa.append(sheet.cell_value(row,l))

            da.append(sa)
        
        return da



global a
a = []
def bianli(path,find):
    global a
    if os.path.exists(path):
        list = os.listdir(path) #列出文件夹下所有的目录与文件
        for i in range(0,len(list)):
            path1 = os.path.join(path,list[i])
            if os.path.isfile(path1):
                if path1.find(find)>0:
                    a.append(path1)
            else:
                bianli(path1,find)

def read_excel(filename):
    dataa = []
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0) #book.sheet_by_name('sheet1')
    v1 = sheet.cell_value(2,3)
    print(filename)
    if str(sheet.cell_value(0,0)).find('住宅')>0:
        v2 = sheet.cell_value(2,3)
        v3 = sheet.cell_value(3,5)
        v4 = sheet.cell_value(3,11)
        v5 = sheet.cell_value(4,5)
        v6 = sheet.cell_value(4,11)
        v7 = sheet.cell_value(5,3)
        v8 = sheet.cell_value(1,12)
    elif  str(sheet.cell_value(0,0)).find('办公')>0:
        v2 = sheet.cell_value(2,3)
        v3 = sheet.cell_value(3,4)
        v4 = sheet.cell_value(3,7)
        v5 = sheet.cell_value(4,4)
        v6 = sheet.cell_value(4,7)
        v7 = sheet.cell_value(5,3)
        v8 = sheet.cell_value(1,8)
    else:
        v2 = sheet.cell_value(2,3)
        v3 = sheet.cell_value(3,5)
        v4 = sheet.cell_value(3,11)
        v5 = sheet.cell_value(4,5)
        v6 = sheet.cell_value(4,11)
        v7 = sheet.cell_value(5,3)
        v8 = sheet.cell_value(1,12)
    dataa.append(v1)
    dataa.append(v2)
    dataa.append(v3)
    dataa.append(v4)
    dataa.append(v5)
    dataa.append(v6)
    dataa.append(v7)
    dataa.append(v8)
    return dataa  #读取指定单元格的数据

def read_excel2(filename): #获取新 旧名称
    dataa = []
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0) #book.sheet_by_name('sheet1')
    ro = sheet.nrows
    for i in range(1,ro):
        dis={}
        dis['old']=sheet.cell_value(i,0)
        dis['newn']=sheet.cell_value(i,1)
        dataa.append(dis)
    return dataa


def read_excel3(a):  # 地价数据抽取
    dataa1 = []
    for aa in a:# 遍历xls文件路径
        book = xlrd.open_workbook(aa)
        sheet = book.sheet_by_index(0) #book.sheet_by_name('sheet1')
        ro = sheet.nrows
        for i in range(5,ro):
            dataa = [] #存储一行的数据
            if sheet.cell_value(i,1):
                v1=sheet.cell_value(i,1)
                v2=sheet.cell_value(i,5)#设定楼面价
              
                dataa.append(v1)
                dataa.append(v2)
             
            else:
                break
            dataa1.append(dataa)  #存储所有行的数据
    return dataa1

def exlcelwrite(a, filename):
    book = xlwt.Workbook()            #创建excel对象
    sheet = book.add_sheet('sheet1')  #添加一个表
    c = 0  
    for d in a: #取出data中的每一个元组存到表格的每一行
        for index in range(len(d)):   #将每一个元组中的每一个单元存到每一列
            sheet.write(c,index,d[index])
        c += 1
    book.save(filename)

def newname(namelist,filename):#重命名文件夹
    if os.path.exists(filename):
        for l in namelist:
            print(l)
            if os.path.isdir(os.path.join(filename,l['old'])):
                o = os.path.join(filename,l['old'])
                n = os.path.join(filename,l['newn'])
                os.rename(o,n)

if __name__ == '__main__': 
    
    p=r"F:\地价\任务"
    f1="准宗地调查表"
    bb=[]
    r=r"F:\地价\2020-8.xls"
    bianli(p,f1)
    bb=read_excel3(a)
    print(bb)
    exlcelwrite(bb,r)
   # newname(da,r"F:\地价\2019区段\静安照片 - 副本")
    # p=r"E:\工作\2019区段地价\虹口息补充材料"
    # bianli(p)
    # bb=[]
    # r=r"E:\工作\2019区段地价\虹口息补充材料\hk.xls"
    # for  aa in a:
    #     bb.append(read_excel(aa))
    # exlcelwrite(bb,r)