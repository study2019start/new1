from mysqlmodel import mysql_model
import xlrd
from datetime import datetime
import pandas as pd
import os
import  time
class update(object):
    def __init__(self,dataname,filename,wherelist):
        self.d=dataname
        self.f=filename
        self.wh=wherelist
        self.lis=[]

    def conn(self):
        cn=mysql_model(self.d,"user","7940","192.168.1.3",)
        redata=self.readexcel()
        listp1=[  x[self.wh[0]] for  x in redata ]
        resp=[]
        inlist=[]
        inlist.append(listp1) #in 搜索 当中的数值
        df1=pd.DataFrame(redata,columns=self.wh)
        
        # for flp in redata:
        #     pp=cn.select({self.wh[0]:flp[self.wh[0]]},"reports",self.wh)
        #     print(pp)
        #     resp.append(pp)
        flienew=os.path.join(os.getcwd(),datetime.now().strftime("%Y%m%d-%S")+".xlsx")
        print(inlist)
        resp=cn.selectmul([self.wh[0]],'reports',inlist,self.wh)
        df2=pd.DataFrame(resp,columns=['fd1','fd33_2','fd34_2','ck_2','fd35_2','fd36_2'])
        
        df2['fd33_2'].fillna(0,inplace=True)
        df2['ck_2'].fillna("-1",inplace=True)
        df3=df2.loc[(df2["fd33_2"]>0 )| ((df2["ck_2"] !="-1") & (df2["ck_2"] !=""))]
        df3.to_excel(flienew)
        flienew2=os.path.join(os.getcwd(),datetime.now().strftime("%Y%m%d-%S")+".xlsx")
        df2.to_excel(flienew2)
        #df2['count']=df2['fd33_2'].apply(lambda x:  1 if x>0  else  0)
        #if df2['count'].sum() <3 :

        #df2.fillna("",inplace=True)
        df=pd.merge(df1,df2,how='left',on='fd1')
        df.drop(df[(df2["fd33_2"]>0) | ((df2["ck_2"] !="-1") & (df2["ck_2"] !=""))].index,inplace=True)
        print(df.shape[0])
        #df['fd33']=df['fd33']+df['fd33_2']
        #df['fd34']=df['fd34']+df['fd34_2']
        #df['checkno']=df['checkno']+df['ck_2']
        #resultr=df[self.wh].to_dict('records')
        resultr2=df[self.wh[1:]].to_dict('records')
        
        
        searhf1= df[[self.wh[0]]]
        
       
        searhf=searhf1.to_dict('records')#[ {self.wh[0]:x[self.wh[0]]} for x in resultr]
        cn.update(resultr2,searhf,'reports')
        return True

        #else:
            #return False
        #print(resultr)


    def readexcel(self):
        # book = xlrd.open_workbook(self.f)
        # sheet = book.sheet_by_index(0) #book.sheet_by_name('sheet1')
        # ra = sheet.nrows
        # #na = sheet.ncols
        # dataa =[]
        # row1v=sheet.row(0)
        ddf=pd.read_excel(self.f,sheet_name = 0,header=None)
        ddf=ddf.drop(ddf.index[0])
        ddf.rename(columns={0:'fd1',1:'fd33',2:'fd34',3:'checkno',4:'fd35',5:'fd36'}, inplace=True)
        ddf['fd35']=ddf['fd35'].apply(lambda x: x.strftime("%Y-%m-%d"))
        ddf['fd36']=ddf['fd36'].apply(lambda x: x.strftime("%Y-%m-%d"))
        datadci=ddf.to_dict("records")
        # print(datadci)

        # for i in range(1,ra):
        #     dic={}
        #     v1=sheet.cell_value(i,0)
        #     v2=sheet.cell_value(i,1)
        #     v3=sheet.cell_value(i,2)
        #     v4=sheet.cell_value(i,3)
        #     v5=xlrd.xldate.xldate_as_datetime(sheet.cell_value(i,4) ,1).strftime("%Y-%m-%d")
        #     v6=xlrd.xldate.xldate_as_datetime(sheet.cell_value(i,5), 1).strftime("%Y-%m-%d")
        #     dic['fd1']=v1
        #     dic['fd33']=v2
        #     dic['fd34']=v3
        #     dic['checkno']=v4
        #     dic['fd35']=v5
        #     dic['fd36']=v6
        #     self.lis.append(v1)
        #     dataa.append(dic)
        # return dataa
        return datadci


if __name__ == "__main__":
    t=time.time()
    fileurl=r"E:\王昱鹏0830.xlsx"
    dan="im2006"
    whl=['fd1','fd33','fd34','checkno','fd35','fd36']
    up=update(dan,fileurl,whl)
    up.conn()
    print((time.time()-t)/60)

    