import MySQLdb
import json
#db = MySQLdb.connect( "localhost", "root", "111", "xiaoqu", charset='utf8' )

class xiaoqu_mysql_zong(object):
    def __init__(self):
        self.db = MySQLdb.connect( "localhost", "root", "111", "xiaoqu", charset='utf8' )

    def insertloucen(self,wherelist):
        field = []
        value = []
        s = ()
        s1 = "%s"
        for k,v in wherelist.items():
            field.append(k)
            value.append(v)
            s = s+(s1,)
        cur = self.db.cursor()
        st ="insert into loucen ( %s ) values " % ','.join(field)
        req = cur.execute(st+"("+','.join(s)+")",value)
        self.db.commit()
        cur.close()
        return req

    def selectdizhi(self,s):
        cur = self.db.cursor()
        i = cur.execute("select * from dizhi "+s)
        req = cur.fetchmany(i)
        self.db.commit()
        cur.close()
        return req




    def insert(self,bname,wherelist):
        field = []
        value = []
        s = ()
        s1 = "%s"
        for k,v in wherelist.items():
            field.append(k)
            value.append(v)
            s = s+(s1,)
        cur = self.db.cursor()
        st ="insert into "+bname+" ( %s ) values " % ','.join(field)
        req = cur.execute(st+"("+','.join(s)+")",value)
        self.db.commit()
        cur.close()
        return req

    def update(self,whe,id):
        value = []
        s = ()
        s1 = "%s"
        for k,v in whe.items():
            value.append(v)
            s = s+(k+"="+s1,)
        value.append(id)
        cur = self.db.cursor()
        st ="update  zongtable set %s  " % ','.join(s)
        req = cur.execute(st+" where id= %s ",value)
        self.db.commit()
        cur.close()
        return req

    def select(self,s):
        cur = self.db.cursor()
        i = cur.execute("select * from zongtable "+s)
        req = cur.fetchmany(i)
        self.db.commit()
        cur.close()
        return req

    def selectid(self,id):
        cur = self.db.cursor()
        i = cur.execute("select * from zongtable where id= ? ",(id))
        req = cur.fetchmany(i)
        self.db.commit()
        cur.close()
        return req

    def muselect(self,mu):
        cur = self.db.cursor()
        mulis=()
        mure=()
        for v in mu:
            mv = str(v)+" = %s" 
            mulis = mulis+(mv,)
            ms = mu[v]
            mure = mure+(ms,)
        alllis = (' and ').join(mulis)
        print(alllis)
        req = cur.execute("select * from zongtable where "+alllis,mure)
        
        info = cur.fetchmany(req)
        
        self.db.commit()
        cur.close()
        return info

    def clos(self):
        self.db.close()