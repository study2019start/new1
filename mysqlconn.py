import pymysql
import numpy as np
#db = MySQLdb.connect( "localhost", "root", "111", "xiaoqu", charset='utf8' )

class xiaoqu_mysql_lou(object):
    def __init__(self):
        self.db=pymysql.connect( "localhost", "root", "111", "xiaoqu", charset='utf8' )
    
    def insert(self,name,wherelist):
        field = []
        value = []
        s = ()
        s1 = "%s"
        for k,v in wherelist.items():
            field.append(k)
            value.append(v)
            s = s+(s1,)
        cur = self.db.cursor()
        st ="insert into "+name+" ( %s ) values " % ','.join(field)
        req = cur.execute(st+"("+ ",".join(s)+")",value)
       
        self.db.commit()
        cur.close()
        
        return req

    def manyinsert(self,name,wherelist):
        ls=[]
        s1 = "%s"
        for where in wherelist:
            s = ()
            field = []
            value = []
            for k,v in where.items():
                field.append(k)
                value.append(v)
                s = s+(s1,)
            ls.append(value)
        cur = self.db.cursor()
        st ="insert into "+name+" ( %s ) values " % ','.join(field)
        print(st)
        req = cur.executemany(st+"("+ ",".join(s)+")",ls)
       
        self.db.commit()
        cur.close()
        
        return req

    def select(self,nam,ls,order,es,limit):
        cur = self.db.cursor()
        lf=[]
        
        whe=""
        if ls:
            whe="where "
            for k,v in ls.items:
                whe=whe+"%s=%s,"
                lf.append(k)
                lf.append(v)
            whe=whe[0:-1]
        if order:
            whe=whe+"  order by "+order
            
            if es:
                whe=whe+"  "+es
                
        if limit:
            whe=whe+" limit %s"
            lf.append(limit)
        i = cur.execute("select * from "+nam +whe,lf)
        req = cur.fetchmany(i)
        self.db.commit()
        return req
    
    def selectc(self,sv):
        cur = self.db.cursor()
        i = cur.execute("select count(%s) from %s",sv)
        req = cur.fetchmany(i)
        self.db.commit()
        return req

    def selectid(self,id,wherelist):
        cur = self.db.cursor()
        s1="%s"
        s=()
        ss=[]
        for k,v in wherelist.items:
            s=s+(s1+"="+s1,)
            ss.append(k)
            ss.append(v)

        i = cur.execute("select * from lou where z_id= ? ",(id))
        req = cur.fetchmany(i)
        self.db.commit()
        return req

    def clos(self):
        self.db.close()