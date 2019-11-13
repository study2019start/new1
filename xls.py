import os
import xlrd
import xlwt

global a
a = []
def bianli(path):
    global a
    if os.path.exists(path):
        list = os.listdir(path) #列出文件夹下所有的目录与文件
        for i in range(0,len(list)):
            path1 = os.path.join(path,list[i])
            if os.path.isfile(path1):
                if path1.find("xls")>0:
                    a.append(path1)
            else:
                bianli(path1)

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
    return  dataa  #读取指定单元格的数据

def read_excel2(filename):
    dataa = []
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0) #book.sheet_by_name('sheet1')
    ro = sheet.nrows
    for i in range(0,ro):
        dis={}
        dis['old']=sheet.cell_value(i,0)
        dis['newn']=sheet.cell_value(i,1)
        dataa.append(dis)
    return dataa


def exlcelwrite(a, filename):
    book = xlwt.Workbook()            #创建excel对象
    sheet = book.add_sheet('sheet1')  #添加一个表
    c = 0  #保存当前列
    for d in a: #取出data中的每一个元组存到表格的每一行
        for index in range(len(d)):   #将每一个元组中的每一个单元存到每一列
            sheet.write(c,index,d[index])
        c += 1
    book.save(filename)

def newname(namelist,filename):
    if os.path.exists(filename):
        lis= os.listdir(filename)
        for l in lis:
            if os.path.isdir(os.path.join(filename,l)):
                o = os.path.join(filename,l['old'])
                n = os.path.join(filename,l['newn'])
                os.rename(o,n)

if __name__ == '__main__': 
    p=r"E:\工作\2019区段地价\虹口息补充材料"
    bianli(p)
    bb=[]
    r=r"E:\工作\2019区段地价\虹口息补充材料\hk.xls"
    for  aa in a:
        bb.append(read_excel(aa))
    exlcelwrite(bb,r)