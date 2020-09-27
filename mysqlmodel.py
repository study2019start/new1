import pymysql
import json
from DBUtils.PooledDB import PooledDB

#db = {'host':'localhost', 'user':'root', 'password':'111', 'db':'web', 'charset':'utf8'}






class mysql_model(object):
    def __init__(self,dataname,us='root',pwd="111",host1="localhost",ch="utf8"):
        
        self.db1 = PooledDB(pymysql,maxconnections=8,host=host1,user=us,port=3306,passwd=pwd,db=dataname,charset=ch,use_unicode=True)
    
    async def insert(self,wherelist,tablename): #插入的字典 表名
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

    def manyinsert(self,list1,list2,tablename): #插入字段列表   插入的值的值是列表  多个值一个列表  表名
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
        s = []
        s2= []
        wherep=""
        s1 = "%s"
        if whe :
            for k,v in whe[0].items():
                s.append(k+"="+s1)
            if searchwhere[0]:
                wherep=" where "
                for ki,vi in searchwhere[0].items():
                    s2.append(ki+"="+s1)
            for ii,rs in enumerate(whe):
                value1=()
                for ki,vi in rs.items():
                    value1=value1+(vi,)
                if searchwhere[ii]:
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


    def updateorinsertmany(self,whe,searchwhere,tablename):# 更新内容字典列表，指定的条件列表，表名
        value = []
        field=[]
        dbb=self.db1.connection()
        cur = dbb.cursor()
        s = []
        s2= []
        shailist=[]
        shailistwhere=[]
        insertlist=[]
        wherep=""
        s1 = "%s"
        req=None
        for is1,ss1 in enumerate(searchwhere):
            valuel=[]
            sv=[]
            wheres=""
            if ss1:
                wheres=" where "
                for k,v in ss1.items():
                    
                    valuel.append(v)
                    sv.append(k+"="+s1)
            strsearch="select * from %s  %s %s " %(tablename,wheres,'and'.join(sv))
            
            rq=cur.execute(strsearch,valuel)
            dbb.commit()
            fp=cur.fetchmany(rq)
            if fp:
                shailist.append(whe[is1]) #为更新
                shailistwhere.append(ss1)
            else:
                insertlist.append(whe[is1])# 插入的值


        if shailist :
            for k,v in shailist[0].items():
                s.append(k+"="+s1)
            if shailistwhere[0]:
                wherep=" where "
                for ki,vi in searchwhere[0].items():
                    s2.append(ki+"="+s1)
            for ii,rs in enumerate(shailist):
                value1=[]
                for ki,vi in rs.items():
                    value1=value1.append(vi)
                if shailistwhere[ii]:
                    for kii,vii in shailistwhere[ii].items():
                        value1=value1.append(vii)
                value.append(value1)
                

            st ="update %s  set %s  " % (tablename,','.join(s))
            
            st= st +wherep+" %s " % ("and".join(s2))
            try:
                req = cur.executemany(st,value)
                dbb.commit()
            except Exception as e:

                dbb.rollback()
        value=[]
        s=[]
        if insertlist:
           
            for ip,minset in enumerate(insertlist):
                templ=[]
                for kk,vv in minset.items():
                    if ip==0:
                        field.append(kk)
                        s.append(s1)
                    
                    templ.append(vv)
                value.append(templ)

            st ="insert into %s  ( %s ) values " % (tablename,','.join(field))
            print(st)
            print(value)
            try:
                req = cur.executemany(st+"("+','.join(s)+")",value)
                dbb.commit()
            except Exception as e:
                print(e)
                dbb.rollback()
        cur.close()
        dbb.close()
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

    def select(self,mu,tablename,selectlist,between=None): #条件 表名 查找的字段  时间范围
        dbb=self.db1.connection()
        cur = dbb.cursor()
        mulis=()
        mure=()
        sp=""
        alllis="  where "
        sl=""
        spp="%s" 
        if selectlist:
            sl=",".join(selectlist)
        else:
            sl="*"
        if mu :
            for llmu in mu:
                for k,v in llmu.items():
                    mv = str(k)+" = "+spp
                    mulis = mulis+(mv,)
                    mure = mure+(v,)
                alllis = alllis + (' and ').join(mulis)
        else:
            alllis=""
       
        if  between:
            if alllis=="":
                alllis="  where "
            for kp,vp in between.items():
                sp=" and "+kp+"  between  " +spp+ " and "+spp
                mure=mure+(vp[0],vp[1])

        sqlt="select "+ sl + " from " +tablename+alllis+sp
        req = cur.execute(sqlt,mure)
        info = cur.fetchmany(req)
        cur.close()
        dbb.close
        return info

    def selectmul(self,mu,tablename,listt,searchlistt):# in条件的字段 表名 in中的值
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
        print(sqlt)
        req = cur.execute(sqlt,mure)
        info = cur.fetchmany(req)
        cur.close()
        dbb.close
        return info

