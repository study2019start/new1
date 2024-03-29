from mysqlmodel import mysql_model
import pandas as pd 
from datetime import datetime
import time
import os 
import xlwings as xlw
from dateutil.relativedelta import relativedelta
import numpy as np
from excel import model_excel

import re
import configparser

class he(object):
    def __init__(self,searchlist,searchlist2,filename,host,database,tablename,us,psw,wheredic=None):
        self.s=searchlist
        self.s2=searchlist2
        if searchlist:

            self.ts=searchlist
        else:
            self.ts=searchlist2
        self.f=filename
        self.h=host
        self.d=database
        self.t=tablename
        self.w=wheredic
        self.pw=psw
        self.u=us
        self.t1=datetime.now().strftime("%Y-%m-%d")
        t2=datetime.now()+relativedelta(months=-15)
        
        self.t3=t2.strftime("%Y-%m-%d")
        mi=configparser.ConfigParser()
        mi.readfp(open(r'in.ini'))
        key1=mi.get('whq','months')
        t=0-int(key1)
        self.t4=(datetime.now()+relativedelta(months=t)).strftime("%Y-%m-%d")

    def search(self,columnsl):
        smo=mysql_model(self.d,self.u,self.pw,self.h,"gbk")
        lsr=smo.select(self.w,self.t,self.ts,{'fd10':[self.t3,self.t1]})
        
        p=pd.DataFrame(lsr,columns=columnsl)
         
        return p

    def search2(self,columnsl):
        smo=mysql_model(self.d,self.u,self.pw,self.h,"gbk")
        lsr=smo.select(self.w,self.t,self.ts,{'fd10':[self.t4,self.t1]})
        
        p=pd.DataFrame(lsr,columns=columnsl)
         
        return p
     
    def readTorF(self):
        df=pd.read_excel(self.f,hearder=None,sheet_name=0,skiprows=4,usecols="K:m")
        
        return (df.iloc[:,1].isna().sum()>30)
          
    def readexcel(self):
        df=pd.read_excel(self.f,header=None,sheet_name=0,skiprows=4,usecols='A:I')
        
        df[5]=df[5].apply(lambda x: repl(x)) 
        return df

    def readexcel2(self):
        df=pd.read_excel(self.f,header=None,sheet_name = 0,skiprows=4,usecols='k:m')
        
        df.dropna(inplace=True)
        
        npp=np.digitize(df[12].values,[0,10000000],right=True)
        
        pricelist=[0,0.00022,0.0002]
         
        df[12]=df[12].values*np.array(pricelist)[npp]
        df[10]=df[10].apply(lambda x: x.replace("号",""))
        #df[12]=df[12].apply(lambda x: x/10000*2 if x>10000000 else x/10000*2.2)
        #df.sort_values(ascending=False,by=13,inplace=True)
        
        return df

    def m(self):
        if self.readTorF():
            self.ts=self.s
            self.model()
        else:
            self.ts=self.s2
            self.model2()


    def model(self):
        df1=self.readexcel()
        if df1.shape[0]>10 :
            df1.drop(df1[df1[0].map(np.isnan)].index)
            df2=self.search(['报告编号','地址','客户','完成日期','总价','估价人员'])
            df2["地址"]=df2["地址"].apply(lambda x:repl(x))
            df2["总价"]=df2["总价"]*10000
            df2["完成日期"]=df2["完成日期"].apply(lambda x:x.strftime("%Y%m%d"))
            df2["估价人员"]=df2["估价人员"].apply(lambda x:x.replace("殷?","殷旸"))
            file2=datetime.now().strftime("%Y-%m-%d,%H-%M-%S")
            f1=self.f.rfind(".")
            #f2=self.f.rfind("\\")
            st1=self.f[f1:len(self.f)] #后缀名
            #st2=self.f[f2:f1] #文件名
            #st3=self.f[0:f2] #文件所在目录
            fd2fullname=os.path.join(os.getcwd(),file2+st1)
            df2.to_excel(fd2fullname)
            df2['总价']=df2['总价'].astype(int)
            #df3=df1.drop_duplicates(subset=[2],keep='first')   #删除重复客户
            
            #df4=df2.drop_duplicates(subset=['客户'],keep='first') #查询到的表删除重复客户
            #df4=df4[['报告编号','客户']]
            #df5=pd.merge(df3,df4,how='left',left_on=2,right_on='客户')

            df7=df2[['报告编号','地址']]
            df=pd.merge(df1,df7,how='left',left_on=5,right_on='地址')
            
            #df6=df5[[0,'报告编号']]
            #df=pd.merge(df,df6,how='left',on=0,) 
            #df['报告编号_x']=df.apply(lambda x: x['报告编号_x'] if x["报告编号_x"] is not np.nan else x['报告编号_y'],axis=1)
            dft=pd.merge(df,df2,how='left',left_on='报告编号',right_on="报告编号")
            dft.drop_duplicates(subset=[0],keep='first',inplace=True)
            sna=dft['报告编号'].isna().sum()
            print(sna)
            xlww=model_excel()
            xlww.xlwingwirte(dft[['报告编号','完成日期','总价','估价人员']],self.f,None,False,'K5')
            
            return sna
        else:
            return -1
        

    def model2(self):
        ff1=self.readexcel2()
        ff2=self.search2(['报告编号','估价人员'])
        dftf=pd.merge(ff1,ff2,how='left',left_on=10,right_on='报告编号')
        dftf['估价人员'].replace("殷?","殷旸",inplace=True)
        dfff=dftf.groupby(['估价人员'],as_index=False)
        ff2=dfff[12].agg(np.sum)
        print(ff2)
        pff=dfff.size()
        pff=pff.reset_index(name='数量')
        ff3=pd.merge(ff2,pff,how="left")
        print(ff3)
        xlww=model_excel()
        xlww.xlwingwirte(dftf[[10,12,'估价人员']],self.f,'结果',True,'A1')
        #width =0.5
        #plt.rcParams['font.sans-serif'] = ['SimHei'] 
        xlww.xlwingwirte(ff3,self.f,'结果',True,'A1')
        #ax=ff2.plot.bar(x='估价人员',y=12,width = width,label ='收入')
       # plt.xticks(rotation=1)
        #mmax=ff2[12].max() // 50
       # for x, y in enumerate(ff2[12]):
       #     plt.text(x=x-0.15, y=y+mmax, s='%.2f'  %y)
        
        #ax.spines['right'].set_visible(False)
        #ax.spines['top'].set_visible(False)
       # plt.gcf().set_size_inches(10, 5)
       # plt.tight_layout()
       # flijpg=datetime.now().strftime("%Y-%m-%d%H%M%S")+".jpg"
        #plt.savefig(os.getcwd()+"/图片/"+flijpg)
        #plt.show()

    
def repl(fp):
    ls=['徐汇','青浦','杨浦','黄浦','浦东新','虹口','金山','奉贤','闵行','崇明','长宁','嘉定','宝山','普陀','县','卢湾','松江','上海','区','室','市',' ','闸北','静安','城桥镇']
    for lp in ls:
        fp=str(fp).replace(lp,"")
    fp=str(fp).replace("_","-")
    fp=re.sub(r'\(.*\)','',fp)
    fp=re.sub(r'\（.*\）','',fp)
    fp=re.sub(r'\(.*\）','',fp)
    fp=re.sub(r'\（.*\)','',fp)
     
    return fp

if __name__ == "__main__":
    filepath=r"F:\_个人贷款房地产押品评估费用（2021年1月1日-2021年3月31日发放）信衡.xls"
    where=[{"category":"G"}]
    slist=[]#['fd1','fd3','fd7','fd10','fd20','fd26']
    slist2=['fd1','fd26']
    host='192.168.1.3'
    database='im2006'
    m=he(slist,slist2,filepath,host,database,"reports","user","7940",where)
    m.model2()