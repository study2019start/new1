import xlrd
from mysqlmodel import mysql_model
import asyncio
import datetime
import time 
import threading
from access import access_model
import os
class etom():
    def __init__(self,path):
        self.li=['area','lx','dizhi','mianji','zongjia','dj','cjdate','down']


async def readex(b,start):
   
    s=start+1000
    #mm = mysql_model()
    sheet1 = b.sheet_by_index(0)
    nrows = sheet1.nrows
    if s>nrows:
        s = nrows
    lis=[]
    for start in  range(start,s):
        s=()
        for o in range(1,9):
            s=s+(sheet1.cell_value(start,o),)
        lis.append(s)
    print(lis)
    #await pr(lis)
    #await mm.manyinsert(self.li,lis,"myappweb_cjdj_info")
    #mm.manyinsert(self.li,lis,"myappweb_cjdj_info")
def read_excel(filename):
    dataa = []
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0) #book.sheet_by_name('sheet1')
    ra = sheet.nrows
    na= sheet.ncols 
    for i in range(0,ra):
        a=[]
        for s in range(2,na):
            v = sheet.cell_value(i,s)
            a.append(v)
        dataa.append(a)
    return dataa

def accessup(s,tablename):
    mm=access_model()
    l1=[]
    l2=[]
    for ss in s:
        dd={}
        dd['name1']=ss[1] 
        dd['dis']=ss[2]
        id1=str(ss[0])
        l1.append(dd)
        l2.append(id1)
    
    mm.update(l1,l2,tablename)

def accessselectm(s,tablename):
    

async def pr(ss):
    end = time.time()
    s=end*1000
    i=str(s).find('.')
    d=str(s)[i:i+4]
    
    print(str(time.strftime("%H:%M:%S",time.localtime(end)))+" :"+str(d)+"--"+str(ss))
    
def xunh(n,li):
    for lli in li:
        s=read_excel(os.path.join(n,lli))
        print(s)
        accessup(s,lli)

if __name__ == "__main__":
    t=time.time()
    #coo1=[0,1000,2000,3000,4000,5000]
    br=r'F:\地价\2019区段\静安区'
    r= [r'jasy.xls']
    xunh(br,r)
    #path=r"D:\21.xls"
    
    #b = xlrd.open_workbook(path)
    #readex(b,0)
    #tasks=[asyncio.ensure_future(readex(b,x)) for x in coo1]
    #loop=asyncio.get_event_loop()
    #loop.run_until_complete(asyncio.wait(tasks))
    end=time.time()-t
    print(end)