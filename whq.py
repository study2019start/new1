from mysqlmodel import mysql_model
import pandas as pd 
from datetime import datetime
import time
import os 
import xlwings as xlw
from dateutil.relativedelta import relativedelta
import numpy as np
class he(object):
    def __init__(self,searchlist,filename,host,database,tablename,wheredic=None):
        self.s=searchlist
        self.f=filename
        self.h=host
        self.d=database
        self.t=tablename
        self.w=wheredic


    def search(self):
        t1=datetime.now().strftime("%Y-%m-%d")
        t2=datetime.now()+relativedelta(years=-2)
        t3=t2.strftime("%Y-%m-%d")
        smo=mysql_model(self.d,self.h)
        p=pd.DataFrame(smo.select(self.w,self.t,self.s,{'fd10':[t3,t1]}),columns=['报告编号','地址','客户','完成日期','总价','估价人员'])
         
        return p

    def readexcel(self):
        df=pd.read_excel(self.f,header=None,sheet_name = 0,skiprows=4,usecols='A:I')
        df[5]=df[5].apply(lambda x: repl(x)) 
        print(df)
        return df


    def model(self):
        df1=self.readexcel()
        df2=self.search()
        df2["地址"]=df2["地址"].apply(lambda x:repl(x))
        df2["总价"]=df2["总价"]*10000
        df2["完成日期"]=df2["完成日期"].apply(lambda x:x.strftime("%Y%m%d"))
        df2["估计人员"]=df2["估价人员"].apply(lambda x : x.replace("?","旸"))
        file2=datetime.now().strftime("%Y-%m-%d,%H-%M-%S")
        f1=self.f.rfind(".")
        f2=self.f.rfind("\\")
        st1=self.f[f1:len(self.f)] #后缀名
        st2=self.f[f2:f1] #文件名
        st3=self.f[0:f2] #文件所在目录
        fd2fullname=os.path.join(st3,file2+st1)
        #df2.to_excel(fd2fullname)
        df3=df1.drop_duplicates(subset=[2],keep='first')
        df4=df2.drop_duplicates(subset=['客户'],keep='first')
        df5=pd.merge(df3,df4,how='left',left_on=2,right_on='客户')
        
        print(df5['报告编号'].isna().sum())
        df=pd.merge(df1,df2,how='left',left_on=5,right_on='地址')
        df6=df5[[0,'报告编号','完成日期','总价','估价人员']]
        df=pd.merge(df,df6,how='left',on=0)
        print(df)
        df['报告编号_x']=df.apply(lambda x: x['报告编号_x'] if x["报告编号_x"] is not np.nan else x['报告编号_y'],axis=1)
        print(df['报告编号_x'].isna().sum())



def repl(fp):
    ls=['徐汇','青浦','杨浦','黄浦','浦东新','虹口','金山','奉贤','闵行','崇明','长宁','嘉定','宝山','上海','区','室','市',"(A)","（A）","(B)","（B）","(C)","（C）"]
    for lp in ls:
        fp=fp.replace(lp,"")
    fp=fp.replace("_","-")
    return fp

if __name__ == "__main__":
    filepath=r"F:\信衡--2020年第1季度.xls"
    where=[{"category":"G"}]
    slist=['fd1','fd3','fd7','fd10','fd20','fd26']
    host='localhost'
    database='im2006'
    m=he(slist,filepath,host,database,"reports",where)
    m.model()