import pandas as   pd
import time
import datetime
import os
from mysqlmodel import mysql_model
from  docx   import Document
import re

re1="Y(\d{4})-\d{5}$"

def model(pathx,pathw,dataname,us,pwd,host1,ch,mu,tablename,searchlist=None):
    readexcel_r=readexcel(pathx)
     
    df=getlistl(dataname,us,pwd,host1,ch,mu,tablename,readexcel_r,searchlist)
     
    df['fd38']=df['fd38'].apply(lambda x: str(x).replace("支行",""))
    df['fd1_year']=df['fd1'].apply(lambda x: re.findall(re1,x)[0])
    df['fd10_1']=df['fd10'].apply(lambda x :riq2(x))
    df['fd10_2']=df['fd10'].apply(lambda x:qzhuan(x))
    df['fd20_z']=df['fd20'].apply(lambda x :zhuandaxie(int(x*10000)))
    print(df)

    
def riq2(riq):
    r=""
    lp=[]
    if riq:
        print(riq)
        rdatetime=datetime.datetime.strptime(str(riq),"%Y-%m-%d")
        lp.append(str(rdatetime.year))
        lp.append("年")
        lp.append(str(rdatetime.month))
        lp.append("月")
        lp.append(str(rdatetime.day))
        lp.append("日")
        r="".join(lp)
    return r

def tiword(path,dic,flname):
    flpathsave=path[:path.rfind("\\")+1]+flname+".docx"
    if os.path.exists(flpathsave):
        path=flpathsave
     
    docxx=Document(path)
    for para in docxx.paragraphs:
        for i in range(len(para.runs)):
            for k,v in dic.items():
                para.runs[i].text=para.runs[i].text.replace("["+k+"]",v)
    docxx.save(flpathsave)


def getlistl(dataname,us,pwd,host1,ch,mu,tablename,list_l,searchlist):
    mysqlm=mysql_model(dataname,us,pwd,host1,ch)
    mresult=mysqlm.selectmul(mu,tablename,list_l,searchlist)
    df=pd.DataFrame(mresult,columns=searchlist)
    return df


def readexcel(path):
    df=pd.read_excel(path,header=0,sheet_name = 0,usecols='A:A')
    df.fillna("",inplace=True)
    return df.values.tolist()



def  qzhuan(riq):
    r=[]
    riq1=str(riq)
    if riq :
        f=riq1.split("-")
        lp=["〇","一","二","三","四","五","六","七","八","九"]
        if len(f)==3:
            for i in f[0]:
                r.append(lp[int(i)])
            r.append("年")
            if len(f[1])>1 and f[1][0] !="0":
                r.append(lp[int(f[1][0])])
                r.append("十")

            r.append(lp[int(f[1][-1:])])
            r.append("月")
            if len(f[2])>1 and f[1][0] !="0":
                r.append(lp[int(f[2][0])])
                r.append("十")

            r.append(lp[int(f[2][-1:])])
            r.append("日")
    return ''.join(r)


def zhuandaxie(nums):
    nums =str(nums)
    da1=["零","壹","贰","叁","肆","伍","陆","柒","捌","玖"]
    da2=["拾","佰","仟","万","亿","兆"]
    dax=[]
    p=0
    if  is_number(nums):
        l=len(nums)  #长度
        print(l)
        if l<20:
            for i in range(0,l):
                ii=l-1-i
                nm=int(nums[i:i+1])
                if i<l-1 and nm==0:
                    if int(nums[i+1:i+2]) >0:
                        dax.append(da1[0])
                elif nm==0 :
                    pass
                else:
                    dax.append(da1[nm])
                #if (ii+4) % 4 ==0  and i>0 :
                if (ii==4 and l <9) or (ii==4 and nm >0) or ii==12 :
                    dax.append(da2[3]) 
                elif ii==8:
                    dax.append(da2[4])
                elif ii== 16:
                    dax.append(da2[5])
                elif nm >0:
                    ll=(ii+4)%4
                    dax.append(da2[ll-1])
        return "".join(dax)
    else:
        return "数字太长"

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass
 
    # try:
    #     import unicodedata
    #     unicodedata.numeric(s)
    #     return True
    # except (TypeError, ValueError):
    #     pass
 
    return False
if __name__ == "__main__":
    pp=os.path.join(os.path.abspath('.'),r"yugu\xlsx\预估报告编号.xlsx")
    p2=os.path.join(os.path.abspath('.'),r"yugu\mu\模板1.docx")
    data_n="im2006"
    us="root"#"user"
    pwd="111"#"7940"
    host="localhost"#"192.168.1.3"
    ch="utf8"
    mu=["fd1"]
    tablename="reports"
    searchlist=["district","fd3","fd1","fd42","fd4","fd18","fd15","fd20","fd21","fd10","fd37","fd38"]
    model(pp,p2,data_n,us,pwd,host,ch,mu,tablename,searchlist)
    

    #print("".join(zhuandaxie(str(50000000020000))))
