import pandas as pd
import xlrd
import xlwings
from mysqlmodel import mysql_model
import time
import datetime
import re
import numpy as np
import time 

re1=r"^\d{4}-\d{1,2}-\d{1,2}"
class model(object):
    def __init__(self,path,person,insert_list,database_n,table_n,host_u,user_n,pwd):
        self.filep=path
        self.p=person
        self.d=database_n
        self.l=insert_list
        self.t=table_n
        self.h=host_u
        self.u=user_n
        self.pwd=pwd


    def msqlinset(self):
        t,df1=self.readandcheck()
        if t:
            
            mconn=mysql_model(dataname=self.d,us=self.u,host1=self.h,pwd=self.pwd,ch="gbk")
            df_ins=np.array(df1).tolist()
            
            
            mconn.manyinsert(self.l,df_ins,self.t)


    def readandcheck(self):
        # try:
        df=pd.read_excel(self.filep,header=0,sheet_name = 0,usecols='B:I')
        df.fillna("",inplace=True)
        
        df.dropna(axis=0,how='all',inplace=True)
        dfp=df.copy()
        columnl=dfp.columns.tolist()
        if columnl[0]=="日期" and columnl[1]=="区县":
            
            
            f1=dfp.apply(lambda x: timeformat(x),axis=1)
           
            df.loc[:,"quotedate"]=f1
            #df.loc[:,"日期"]=df["quotedate"]
             
            df.loc[:,"来源"]=dfp["来源"].apply(lambda x: replace(x))
            df.drop(["日期"],axis=1,inplace=True)
            df['quotedate_b']=df["quotedate"]
            df.loc[:,"person"]=self.p
            df.fillna("",inplace=True)
            print(df)   
            df.rename(columns={"区县":"district","坐落":"fd3","报价（万元）":"quoteprice","来源":"fd37","分支":"fd38","联系人":"fd39","备注":"memo1"},inplace=True)
                
                
            return True,df
        else:
            return False,None
        # except:
        #     return False,None


def timeformat(tp1):
    tp=tp1.tolist()[0]
    try:
        return tp.strftime("%Y-%m-%d")
    except:
        if re.match(re1,tp):
            return tp
        else:
            return ""


def replace(p):
    dictp={"工商银行":"中国工商银行","光大银行":"中国光大银行"}
    for k,v in dictp.items():
        if p==k:
            p=v
            
            break
    return p


if __name__ == "__main__":
    fp=r"F:\报价price.xlsx"
    inlist=["district","fd3","quoteprice","fd37","fd38","fd39","quotedate","quotedate_b","person"]
    d_n="im2006"
    table_n="price"
    h="localhost"
    u="root"
    pwd="111"
    m=model(fp,"顾李青",inlist,d_n,table_n,h,u,pwd)
    m.msqlinset()
     
    
    #print(d1)
    #print(d2)
    