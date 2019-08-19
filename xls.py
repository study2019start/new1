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
    if str(sheet.cell_value(0,0)).find('住宅')>0:
        v2 = sheet.cell_value(2,11)
        v3 = sheet.cell_value(5,3)
        v4 = sheet.cell_value(5,11)
        v5 = sheet.cell_value(8,3)
        v6 = sheet.cell_value(8,11)
        v7 = sheet.cell_value(9,11)
        v8 = sheet.cell_value(11,3)
        v9 = sheet.cell_value(13,3)
        v10 = sheet.cell_value(13,11)
        v11 = sheet.cell_value(1,12)
    elif  str(sheet.cell_value(0,0)).find('办公')>0:
        v2 = sheet.cell_value(2,7)
        v3 = sheet.cell_value(5,3)
        v4 = sheet.cell_value(5,7)
        v5 = sheet.cell_value(8,3)
        v6 = sheet.cell_value(8,7)
        v7 = sheet.cell_value(9,7)
        v8 = sheet.cell_value(11,4)
        v9 = sheet.cell_value(12,3)
        v10 = sheet.cell_value(11,6)
        v11 = sheet.cell_value(1,8)
    else:
        v2 = sheet.cell_value(2,11)
        v3 = sheet.cell_value(5,3)
        v4 = sheet.cell_value(5,11)
        v5 = sheet.cell_value(8,3)
        v6 = sheet.cell_value(8,11)
        v7 = sheet.cell_value(9,11)
        v8 = sheet.cell_value(13,3)
        v9 = sheet.cell_value(12,3)
        v10 = sheet.cell_value(12,11)
        v11 = sheet.cell_value(1,12)
    dataa.append(v1)
    dataa.append(v2)
    dataa.append(v3)
    dataa.append(v4)
    dataa.append(v5)
    dataa.append(v6)
    dataa.append(v7)
    dataa.append(v8)
    dataa.append(v9)
    dataa.append(v10)
    dataa.append(v11)
    return(dataa) #读取指定单元格的数据


def exlcelwrite(a, filename):
    book = xlwt.Workbook()            #创建excel对象
    sheet = book.add_sheet('sheet1')  #添加一个表
    c = 0  #保存当前列
    for d in a: #取出data中的每一个元组存到表格的每一行
        for index in range(len(d)):   #将每一个元组中的每一个单元存到每一列
            sheet.write(c,index,d[index])
        c += 1
    book.save(filename)



if __name__ == '__main__': 
    p=r"E:\工作\2019区段地价\静安区\4.样点信息补充材料"
    bianli(p)
    bb=[]
    r=r"E:\工作\2019区段地价\静安区\ja1.xls"
    for  aa in a:
        bb.append(read_excel(aa))
    exlcelwrite(bb,r)