import pypyodbc
import re 
import threading
import time

class access_model(object):
    def __init__(self):
        self.db1 = "Driver={Microsoft Access Driver (*.mdb,*.accdb)};DBQ=F:\\地价\\2019区段\\静安区\\3.2014年区段子单元—静安.mdb"
        self.re=r'(?P<value>(?=[\x21-\x7e]+)[^A-Za-z0-9])'
    def insert(self,wherelist,tablename):
        field = []
        s = ()
        for k,v in wherelist.items():
            field.append(k)
            if isinstance(v,int) or isinstance(v,float):
                s=s+(str(v),)
            else:
                s = s+("'"+str(v)+"'",)
        dbb = pypyodbc.win_connect_mdb(self.db1)
        cur = dbb.cursor()
        st ="insert into %s  ( %s ) values  ( %s )" % (tablename,','.join(field),','.join(s))
        req = cur.execute(st)
        dbb.commit()
        cur.close()
        dbb.close()
        return req

    def manyinsert(self,list1,list2,tablename):
        s = ()
        ss = ()
        ll=""
        for ff in list2:
            for k,v in ff.items():
                if isinstance(v,int) or isinstance(v,float):
                    s=s+(str(v),)
                else:
                    s = s+("'"+str(v)+"'",)
            ll="("+','.join(s)+")"
            ss=ss+(ll,)
        dbb = pypyodbc.win_connect_mdb(self.db1)
        cur = dbb.cursor()
        st ="insert into %s  ( %s ) values   %s " % (tablename,','.join(list1),','.join(ss))
        req = cur.execute(st)
        dbb.commit()
        cur.close()
        dbb.close()
        return req


    def update(self,whe2,idlist,tablename):
        
        dbb = pypyodbc.win_connect_mdb(self.db1)
        cur = dbb.cursor()
        for i,whe in enumerate(whe2):
            s = ()
            for k,v in whe.items():
                if isinstance(v,int) or isinstance(v,float):
                    s=s+(str(k)+"="+str(v),)
                else:
                    s = s+(str(k)+"="+"'"+str(v)+"'",)
            try:
                st ="update %s  set %s  where ydid = %s" % (tablename,','.join(s),idlist[i])
                print(st)
                time.sleep(20)
                req = cur.execute(st)
                dbb.commit()
            except:
                dbb.rollback()

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
            for v in mu:
                if isinstance(mu[v],int) or isinstance(mu[v],float):
                    mu=str(v)+"="+str(mu[v])
                else:
                    st=str(mu[v])
                    if re.search(self.re,st):
                        st=re.sub(self.re,replace1,st)
                    mu = str(v)+"='"+st+"'"
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

def replace1(match):
    value = str(match.group('value'))
    st='['
    st1=']'
    return st+value+st1