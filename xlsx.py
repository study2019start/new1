from openpyxl import Workbook
from openpyxl.utils import get_column_letter
from openpyxl import load_workbook
import math
import os
import time


def  print1(fd1,fd2,source,target):
    wb= load_workbook(fd1)
    jb=30
    sheets = wb['Sheet1']
    rows=sheets.max_row
    print(rows)
    tablerowscount=rows-2 #总户数
    sumfen=math.ceil(tablerowscount/jb)
    
    for i in range(0,sumfen):
        fd2p=os.path.join(fd2,'J-'+str(i*jb+1).zfill(4)+'-J-'+str((i+1)*jb).zfill(4)+'-s.xlsx')
        if os.path.isfile(fd2p):
            tfd2p=fd2p
        else:
            tfd2p=os.path.join(fd2,'J-0001-J-0030-s.xlsx')
        print(fd2p)
        wb2 =load_workbook(tfd2p)
        sheets2 = wb2['评估汇总']
        print(sheets2.max_row)
        for x in range(i*jb+3,(i+1)*jb+3):
            if x > rows:
                break
            for ii,sourcev in enumerate(source):
                temp=sheets[sourcev+str(x)].value
                sheets2[target[ii]+str(x-i*jb)]=temp
                print(temp)
        wb2.save(fd2p)
        #pr=[]
        #pr1=[]
       # for row in rows:
           # pr.append(row[2].value)
        #print(pr)


if __name__=='__main__':
    lst1=['C','D','E','F','G']
    lst2=['B','C','D','F','G']
    print1(r'E:\vba\金陵东路64号地块给评估公司清册.xlsm',r'E:\vba',lst1,lst2)



