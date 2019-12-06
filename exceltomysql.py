import xlrd
from mysqlmodel import mysql_model
import asyncio
import datetime
import time 
import threading
from access import access_model
import os

queueLock = threading.Lock()
class thred(threading.Thread):
    def __init__(self,n,li,dbn):
        threading.Thread.__init__(self)
        self.name1=n
        self.li=li
        self.dbname=dbn
        self.lie=[]
    def run(self):
        rs=xunh(self.name1,self.li)
        for i,rs1 in enumerate(rs):
            s= self.read_excel(rs1)
            self.accessup(s,str(self.li[i]).replace(".xls","").replace(".xlsx",""),self.dbname)


    def read_excel(self,filename):
        dataa = []
        book = xlrd.open_workbook(filename)
        sheet = book.sheet_by_index(0) #book.sheet_by_name('sheet1')
        ra = sheet.nrows
        na= sheet.ncols 
        for aa in range(0,na):
            self.lie.append(sheet.cell_value(0,aa))
        for i in range(1,ra):
            a=[]
            for s in range(0,na):
                v = sheet.cell_value(i,s)
                a.append(v)
            dataa.append(a)
        return dataa

    def accessup(self,s,tablename,dbn):
        mm=access_model(dbn)
        l1=[]
        l2=[]
        lis=self.lie[1:len(self.lie)]
        for ss in s:
            dd={}
            id1={}
            for i,l in enumerate(lis):
                dd[l]=ss[i+1]

            id1[self.lie[0]]=str(ss[0])
            l1.append(dd)
            l2.append(id1)
        #print(l1)
        queueLock.acquire()
        mm.update(l1,l2,tablename)
        self.lie=[]
        queueLock.release()

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


def accessselectm(s,tablename,dbn):
    mm=access_model(dbn)
    res=mm.muselect(s,tablename)
    return res


async def pr(ss):
    end = time.time()
    s=end*1000
    i=str(s).find('.')
    d=str(s)[i:i+4]
    
    print(str(time.strftime("%H:%M:%S",time.localtime(end)))+" :"+str(d)+"--"+str(ss))
    
def xunh(n,li):
    ls=[]
    for lli in li:
        ls.append(os.path.join(n,lli))
    return ls
       

if __name__ == "__main__":
    t=time.time()
    #coo1=[0,1000,2000,3000,4000,5000]
    br=r'F:\地价\2019区段\x7'
    r=[]
    r2=[r'虹口—租赁住宅子单元价格.xls']
    #r'静安—住宅样点价格信息更新1021.xls',r'静安—办公样点价格信息更新.xls',r'静安—商业样点价格信息更新1021.xls',
   # r'虹口—住宅样点信息更新.xls',r'虹口—商业样点信息更新.xls',r'虹口—办公样点信息更新1021.xls‘
    thread=[]
    t1=thred(br,r,"表格\\\静安\\静安样点信息.mdb")
    t2=thred(br,r2,"表格\\\虹口\\虹口样点信息.mdb")
    t1.start()
    t2.start()
    thread.append(t1)
    thread.append(t2)
    for tt in thread:
        tt.join()
    #path=r"D:\21.xls"
    
    #b = xlrd.open_workbook(path)
    #readex(b,0)
    #tasks=[asyncio.ensure_future(readex(b,x)) for x in coo1]
    #loop=asyncio.get_event_loop()
    #loop.run_until_complete(asyncio.wait(tasks))
    end=time.time()-t
    print(end)