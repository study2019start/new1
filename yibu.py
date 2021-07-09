import os
from mysqlmodel import mysql_model
from excel import model_excel
import pandas as pd
import time

def select_mysql_to_excel(database,user,pwd,host,tablename,where,search_list,between):
    smo=mysql_model(database,user,pwd,host,"gbk")
    lsr=smo.select(where,tablename,search_list,between,False)
    df1=pd.DataFrame(lsr)
    df1.columns=['id','报告类型','项目编号','房地产座落','委托单位','借款方','不动产权利人','委托方联系人','估价时点','完成日期','估价目的','估价设定用途','建筑面积','房地产总价','房地产单价','估价人员','协办人员','开票金额','开票日期','到帐日期','付款单位','项目来源(总部)','项目来源(分部)','项目来源联系人','项目进度','项目状态','备注','暗号','委托号','收据金额','内评价格']
    df=df1[(df1['报告类型']=='X')| (df1['报告类型']=='F') | (df1['报告类型']=='T') | (df1['报告类型']=='Z')]
    df=df[~df['项目编号'].str.contains('临')]
    ex=model_excel()
    n_t=time.strftime("%Y%m%d%H%M%S")
    df['建筑面积']=df['建筑面积'].astype("float64")
    df['房地产总价']=df['房地产总价'].astype("int64")
    print(df.info())
    ex.xlwingcreate(df,r"e:\工行"+n_t+r".xlsx")


 
if __name__ == "__main__":
    where=[{"fd37":"中国工商银行"}]
    slist=[]#['fd1','fd3','fd7','fd10','fd20','fd26']
    search_list=['id','category','fd1','fd3','fd4','fdjk','fdzq','fd7','fd9','fd10','fd11','fd15','fd18','fd20','fd21','fd26','fd2','fd33','fd35','fd36','payunit','fd37','fd38','fd39','fd41','projstatus','fd42','countersign','entrustno','receiptvalue','innervalue']
    host='192.168.1.3'
    database='im2006'
    between_time={'fd10':["2021-01-01","2021-07-01"]}
    select_mysql_to_excel(database,'user','7940',host,'reports',where,search_list,between_time)