import pypyodbc
import re 
import threading
import time

class access_model(object):
    def __init__(self,dbname):
        self.db1 = "Driver={Microsoft Access Driver (*.mdb,*.accdb)};DBQ="+str(dbname)
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
                    mu = str(v)+"=["+st+"]"
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

def replace1(match):
    value = str(match.group('value'))
    st='['
    st1=']'
    return st+value+st1