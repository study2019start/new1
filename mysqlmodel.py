import pymysql
import json
from DBUtils.PooledDB import PooledDB
db = {'host':'localhost', 'user':'root', 'password':'111', 'db':'web', 'charset':'utf8'}

class mysql_model(object):
    def __init__(self):
        self.db1 = PooledDB(pymysql,maxconnections=8,host='localhost',user='root',port=3306,passwd='111',db='web',use_unicode=True)
    
    async def insert(self,wherelist,tablename):
        field = []
        value = []
        s = ()
        s1 = "%s"
        for k,v in wherelist.items():
            field.append(k)
            value.append(v)
            s = s+(s1,)
        dbb = self.db1.connection()
        cur = dbb.cursor()
        st ="insert into %s  ( %s ) values " % (tablename,','.join(field))
        req = cur.execute(st+"("+','.join(s)+")",value)
        dbb.commit()
        cur.close()
        dbb.close()
        
        return req

    def manyinsert(self,list1,list2,tablename):
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


    def update(self,whe,id,tablename):
        value = []
        s = ()
        s1 = "%s"
        for k,v in whe.items():
            value.append(v)
            s = s+(k+"="+s1,)
        value.append(id)
        dbb=self.db1.connection()
        cur = dbb.cursor()
        st ="update %s  set %s  " % (tablename,','.join(s))
        req = cur.execute(st+" where id= %s ",value)
        dbb.commit()
        cur.close()
        dbb.close
        return req



    def selectid(self,id,tablename):
        dbb=self.db1.connection()
        cur =dbb.cursor()
        args1 = [tablename,str(id)]
        i = cur.execute("select * from %s  where OBJECTID_1= %s",args1)
        req = cur.fetchmany(i)
        dbb.commit()
        cur.close()
        dbb.close()
        return req

    def muselect(self,mu,tablename):
        dbb=self.db1.connection()
        cur = dbb.cursor()
        mulis=()
        mure=()
        mure=mure+(tablename,)
        alllis="where "
        if mu :
            for v in mu:
                mv = str(v)+" = %s" 
                mulis = mulis+(mv,)
                ms = mu[v]
                mure = mure+(ms,)
            alllis = alllis + (' and ').join(mulis)
        else:
            alllis=""
        req = cur.execute("select * from tudi_cj %s"+alllis,mure)
        info = cur.fetchmany(req)
        cur.close()
        dbb.close
        return info

