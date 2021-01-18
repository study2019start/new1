import pymysql
import json
from DBUtils.PooledDB import PooledDB
import time
import re
class mysql_model(object):
    def __init__(self,dataname,num,name,us='root',pwd="111",host1="localhost",ch="utf8"):
        
        self.db1 = PooledDB(pymysql,maxconnections=8,host=host1,user=us,port=3306,passwd=pwd,db=dataname,charset=ch)
        self.n=num
        self.name=name

    def manyinsert(self,list1,list2,tablename): #插入字段列表   插入的值的值是列表  多个值一个列表  表名
        field = []
        s = ()
        s1 = "%s"
        for k in list1:
            field.append(k)
            s = s+(s1,)
        dbb = self.db1.connection()
        cur = dbb.cursor()
        req=-1
        st ="insert into %s  ( %s ) values " % (tablename,','.join(field))
        try:
            req = cur.executemany(st+"("+','.join(s)+")",list2)
            dbb.commit()
        except Exception as e:
            print(e)
            dbb.rollback()
        cur.close()
        dbb.close()
        return req

    def read_Max(self):
        strf="select max(abs(right(fd1,char_length(fd1)-4))) as mx from reports where fd1 like '%临朱留清%'"
        dbb = self.db1.connection()
        cur=dbb.cursor()
        
        i=cur.execute(strf)
        req = cur.fetchmany(i)
        dbb.commit()
        cur.close()
        dbb.close()
        return req
    
 

    def quhao(self):
        f=self.read_Max()
        print(f)
        if f[0][0]:
            i=f[0][0]+1
        else:
            i=1
        list1=['person','depperson','distrperson','carryondate','distrdate','fd26','fd1','fd41',"category","fd11","fd12"]
        list2=[]
        nd=time.strftime("%Y-%m-%d")
        for ii in range(0,self.n):
            list2_1=['朱留清','柴书钦','朱留清',nd,nd,self.name,"临朱留清"+str(int(i+ii)),'已承接',"G","抵押价值评估","比较法"]
            list2.append(list2_1)
        print(list2)
        r=self.manyinsert(list1,list2,"reports")
        print(r)
             
def is_number_zheng(n):
    f=r"^\d{1,3}$"
    rs=re.match(f,str(n))
     
    return rs
if __name__ == "__main__":
    t=mysql_model("im2006",10,"马晓迎")
    t.quhao()
     
   
    



        