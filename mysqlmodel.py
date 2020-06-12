import pymysql
import json
from DBUtils.PooledDB import PooledDB
#db = {'host':'localhost', 'user':'root', 'password':'111', 'db':'web', 'charset':'utf8'}

class mysql_model(object):
    def __init__(self,dataname):
        self.db1 = PooledDB(pymysql,maxconnections=8,host='localhost',user='root',port=3306,passwd='111',db=dataname,use_unicode=True)
    
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


    def update(self,whe,searchwhere,tablename):# 更新内容字典列表，指定的条件列表，表名
        value = []
        dbb=self.db1.connection()
        cur = dbb.cursor()
        s = ()
        s2=()
        wherep=""
        s1 = "%s"

        for k,v in whe[0].items():
            s = s+(k+"="+s1,)
        if searchwhere[0]:
            wherep=" where "
            for ki,vi in searchwhere[0].items():
                s2=s2+(ki+"="+s1,)
        for ii,rs in enumerate(whe):
            value1=()
            for ki,vi in rs.items():
                value1=value1+(vi,)
            for kii,vii in searchwhere[ii].items():
                value1=value1+(vii,)
            value.append(value1)
                 

        st ="update %s  set %s  " % (tablename,','.join(s))
        
        st= st +wherep+" %s " % ("and".join(s2))
 
        req = cur.executemany(st,value)
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

    def select(self,mu,tablename,selectlist):
        dbb=self.db1.connection()
        cur = dbb.cursor()
        mulis=()
        mure=()
       
        alllis="  where "
        sl=""
        spp="%s" 
        if selectlist:
            sl=",".join(selectlist)
        else:
            sl="*"
        if mu :
            for k,v in mu.items():
                mv = str(k)+" = "+spp
                mulis = mulis+(mv,)
                mure = mure+(v,)
            alllis = alllis + (' and ').join(mulis)
        else:
            alllis=""
        sqlt="select "+ sl + " from " +tablename+alllis

        req = cur.execute(sqlt,mure)
        info = cur.fetchmany(req)
        cur.close()
        dbb.close
        return info

    def selectmul(self,mu,tablename,listt,searchlistt):
        dbb=self.db1.connection()
        cur = dbb.cursor()
        mv=""
        mure=()
        
        sl=""
        if searchlistt:
            sl=",".join(searchlistt)
        else:
            sl="*"
        alllis="  where "
        if mu :
            for i,mm in enumerate(mu):
                if i==0:
                    mv=mm+" in("
               
                else:
                    mv=" and " +mm +" in ("
                mf=""
                for xm in listt[i]:
                    if mf=="":
                        mf=r"%s"
                    else:
                        mf=mf+r",%s"
                    mure=mure+(xm,)
                mv=mv+mf+")"
            alllis=alllis+mv
        else:
            alllis=""
        sqlt="select "+sl+" from "+tablename+alllis
        req = cur.execute(sqlt,mure)
        info = cur.fetchmany(req)
        cur.close()
        dbb.close
        return info

