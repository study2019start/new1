import pymysql

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

    def select(self):
        cur = self.db.cursor()
        i = cur.execute("select * from lou")
        req = cur.fetchmany(i)
        self.db.commit()
        return req

    def selectid(self,id):
        cur = self.db.cursor()
        i = cur.execute("select * from lou where z_id= ? ",(id))
        req = cur.fetchmany(i)
        self.db.commit()
        return req

    def clos(self):
        self.db.close()