import pypyodbc
import re 
import threading
import time
import re
import pandas as pd
import xlwings
from excel import model_excel
import datetime
re1=r"\d{4}-\d{1,2}-\d{1,2}"
class access_model(object):
    def __init__(self,dbname):
        self.db1 = "Driver={Microsoft Access Driver (*.mdb,*.accdb)};DBQ="+str(dbname)
        self.re=r'(?P<value>(?=[\x21-\x7e]+)[^A-Za-z0-9])'
    def insert(self,wherelist,tablename):
        field = []
        s = []
        for k,v in wherelist.items():
            field.append(k)
            if is_number(v):
                s.append(v)
            else:
                s.append("'"+str(v)+"'")
        dbb = pypyodbc.win_connect_mdb(self.db1)
        cur = dbb.cursor()
        st ="insert into %s  ( %s ) values  ( %s )" % (tablename,','.join(field),','.join(s))
        req = cur.execute(st)
        dbb.commit()
        cur.close()
        dbb.close()
        return req

    def inserttusql(self,wherelist,tablename,whereseach):# 插入的字典列表，表名称，查询是否存在的字典列表
        dbb = pypyodbc.win_connect_mdb(self.db1)
        cur = dbb.cursor()
        sqllist=[]
        for ii,wh in enumerate(whereseach):
            stw=""
            lp=""
            for k,v in wh.items():
                if is_number(v) :
                    lp=str(v)
                elif re.match(re1,v):
                    lp="#"+str(v)+"#"
                else:
                    lp="'"+str(v)+"'"
                if stw == "":
                    stw="  where " + k + "=" +lp
                else:
                    stw= " and " + k+ "="+lp
                
             
            x="select ID from "+tablename+stw 
            cur.execute(x)
            inf=cur.fetchall()
            if not inf:
                sqllist.append(wherelist[ii])
        
        for wherels in sqllist:
            field = []
            s = []
            if '' not in wherels.values():
                for k,v in wherels.items():
                        field.append(k)
                        if is_number(v) :
                            s.append(v)
                        elif re.match(re1,v):
                            s.append("#"+str(v)+"#")
                        else:
                            s.append("'"+str(v)+"'")
                st ="insert into %s(%s) values  (%s)" % (tablename,','.join(field),','.join(s))
                
                req = cur.execute(st)
                dbb.commit()
        cur.close()
        dbb.close()
        

    def manyinsert(self,list1,list2,tablename):
        dbb = pypyodbc.win_connect_mdb(self.db1)
        cur = dbb.cursor()
        for ff in list2:
            s = []
            
            ll=""
            for k,v in ff.items():
                if is_number(v):
                    s.append(str(v),)
                else:
                    s.append("'"+str(v)+"'",)
            ll="("+','.join(s)+")"
            
        
            st ="insert into %s  ( %s ) values   %s " % (tablename,','.join(list1),ll)
            req = cur.execute(st)
        dbb.commit()
        cur.close()
        dbb.close()
        return req


    def update(self,whe2,list,tablename):
    
        dbb = pypyodbc.win_connect_mdb(self.db1)
        cur = dbb.cursor()
        req =False
        for i,whe in enumerate(whe2):
            s = ()
            s1=()
            for k,v in whe.items():
                if isinstance(v,int) or isinstance(v,float):
                    s=s+(str(k)+"="+str(v),)
                else:
                    s = s+(str(k)+"="+"'"+str(v)+"'",)
            for k1,v1 in list[i].items():
                if isinstance(v1,int) or isinstance(v1,float):
                    s1 = s1+(str(k1)+"="+str(v1),)
                else:
                    s1 = s1+(str(k1)+"="+"'"+str(v1)+"'",)
            
            try:
                st ="update %s  set %s  where %s" % (tablename,','.join(s),' and '.join(s1))
                print(st)
                
                cur.execute(st)
                req = True
                dbb.commit()
            except:
                dbb.rollback()
                req =False
                print("error")
        cur.close()
        dbb.close
        return req


    def muselect(self,mu,tablename):
        dbb = pypyodbc.win_connect_mdb(self.db1)
        cur = dbb.cursor()
        mulis=()
        alllis="where "
        mure=()
        mure=mure+(tablename,)
        if mu:
            print(mu)
            for v,v1 in mu.items():
                if isinstance(mu[v],int) or isinstance(mu[v],float):
                    mu=str(v)+"="+str(mu[v])
                else:
                    st=str(mu[v])
                    #if re.search(self.re,st):
                        #st=re.sub(self.re,replace1,st)
                    mu = str(v)+"='"+st.replace('\'','\'\'')+"'"
                mulis = mulis+(mu,)
            alllis = alllis+(' and ').join(mulis)
        else:
            alllis=""
        x=" select * from %s  " % tablename
        x=x+alllis
        print(x)
        try:
            req = cur.execute(x)
            info = cur.fetchall()
        except Exception as Argument:
            print (Argument)
            info=[]     
        cur.close()
        dbb.close
        return info


    def mudel(self,mu,tablename):
        dbb = pypyodbc.win_connect_mdb(self.db1)
        cur = dbb.cursor()
        mulis=()
        alllis="where "
        if mu:
            for v,v1 in mu.items:
                if isinstance(mu[v],int) or isinstance(mu[v],float):  
                    mu=str(v)+"="+str(mu[v])
                else:
                    st=str(mu[v])
                    if re.search(self.re,st):
                        st=re.sub(self.re,replace1,st)
                        st=st
                    mu = str(v)+"='"+st+"'"
                mulis = mulis+(mu,) 
            alllis = alllis+(' and ').join(mulis)
        else:
            alllis=""
        x=" delete   from %s  " % tablename
        x=x+alllis
        print(x)
        req = cur.execute(x)
        print(req)
        cur.close()
        dbb.close()
        return req

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

def replace1(match):
    value = str(match.group('value'))
    st='#'
    st1='#'
    return st+value+st1

if __name__=="__main__":
    file_path=r"F:\地价\信衡2021年第一季度任务表.xls"
    df=pd.read_excel(file_path,hearder=None,sheet_name='Sheet1',skiprows=1,usecols="B:M")
    df.columns=['gujiashi','zsbh','guojiashi','idn','fd3','jb','qu','yt','sddmj','sdlmj','xzdmj','xzlj']
    d1=datetime.date.today()
    y1=d1.year
    m1=d1.month
    if m1<=3:

        df['jidu']=str(y1-1)+"年第四季度"
    elif m1<=6:
        df['jidu']=str(y1)+"年第一季度"
    elif m1<=9:
        df['jidu']=str(y1)+"年第二季度"
    else:
        df['jidu']=str(y1)+"年第三季度"
    df['guojiaorshiji']=df['guojiashi'].apply(lambda x: 0 if x=="市级" else 1)
    df.drop(["zsbh","guojiashi","fd3","jb","qu","yt"],axis=1,inplace=True)
    dict_df=df.to_dict("records")
    list1=['gujiashi','idn','sddmj','sdlmj','xzdmj','xzlmj','jidu','guojiaorshiji']
    #ex=model_excel()
    #ex.xlwingwirte(df,r"E:\sxls.xlsx",'Sheet1',False,'A1')
    databaur=r"F:\地价\test\test\conn\Database1.accdb"
    access_m=access_model(databaur)
    access_m.manyinsert(list1,dict_df,"jd_table")
    print(dict_df)
    print(len(dict_df))
