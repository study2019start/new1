import pymysql
import json
from DBUtils.PooledDB import PooledDB
import pandas as pd
#db = {'host':'localhost', 'user':'root', 'password':'111', 'db':'web', 'charset':'utf8'}
from excel import model_excel





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


    def updateorinsertmany(self,whe,searchwhere,tablename,upcode=True):# 更新内容字典列表，指定的条件列表，表名,upcode表示更新条件是否一致
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
        if shailist and upcode :   #更新
            for k,v in shailist[0].items():
                s.append(k+"="+s1)
            if shailistwhere[0]:
                wherep=" where "
                for ki,vi in searchwhere[0].items():
                    s2.append(ki+"="+s1)
            for ii,rs in enumerate(shailist):
                value1=[]
                for ki,vi in rs.items():
                    value1.append(vi)
                if shailistwhere[ii]:
                    for kii,vii in shailistwhere[ii].items():
                        value1.append(vii)
                value.append(value1)
            st ="update %s  set %s  " % (tablename,','.join(s))
            st= st +wherep+" %s " % ("and".join(s2))
            try:
                req = cur.executemany(st,value)
                dbb.commit()
            except Exception as e:

                dbb.rollback()
        elif shailist:
   
            s=[]
            s2=[]
            for ii,rs in enumerate(shailist):
                value1=[]
                for ki,vi in rs.items():
                    s.append(ki+"="+s1)
                    value1.append(vi)
                if shailistwhere[ii]:
                    wherep=" where "
                    for ki,vi in shailistwhere[ii].items():
                        s2.append(ki+"="+s1)
                st ="update %s  set %s  " % (tablename,','.join(s))
                st= st +wherep+" %s " % ("and".join(s2))
                try:
                    req = cur.execute(st,value1)
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
     
            try:
                req = cur.executemany(st+"("+','.join(s)+")",value)
                dbb.commit()
            except Exception as e:
                print(e)
                dbb.rollback()
        cur.close()
        dbb.close()
        return req




    def select(self,mu,tablename,selectlist=None,between=None,listname=False): #条件 表名 查找的字段  时间范围
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
                    if k[-3:]=="_lk":
                        mv = str(k[:-3])+" like "+spp
                        mure = mure+('%'+v+'%',)
                    else:
                        mv = str(k)+" = "+spp
                        mure = mure+(v,)
                    mulis = mulis+(mv,)
                    
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
        print(mure)
        req = cur.execute(sqlt,mure)
        col=cur.description
        info = cur.fetchall()
        if listname:
            
            ruturn_info=[dict(zip([xx[0] for xx in col],x)) for x  in info]
        else:
            ruturn_info=info
        cur.close()
        dbb.close
        return ruturn_info

    def selectmul(self,mu,tablename,listt,searchlistt=None,listname=False):# in条件的字段 表名 in中的值
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
        col=cur.description
        info = cur.fetchall()
        if listname:
            
            ruturn_info=[dict(zip([xx[0] for xx in col],x)) for x  in info]
        else:
            ruturn_info=info
        cur.close()
        dbb.close
        return ruturn_info



    

def create_args_string(num):
    L = []
    for _ in range(num):
        L.append('?')
    return ', '.join(L)

class ModelMetaclass(type):

    def __new__(cls, name, bases, attrs):
        if name=='Model':
            return type.__new__(cls, name, bases, attrs)
        tableName = attrs.get('__table__', None) or name

        mappings = dict()
        fields = []
        primaryKey = None
        
        for k, v in attrs.items():
            if isinstance(v, Field):
               
                mappings[k] = v
                if v.primary_key:
                    # 找到主键:
                    if primaryKey:
                        pass
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
           pass
        for k in mappings.keys():
            attrs.pop(k)
        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mappings__'] = mappings # 保存属性和列的映射关系
        attrs['__table__'] = tableName
        attrs['__primary_key__'] = primaryKey # 主键属性名
        attrs['__fields__'] = fields # 除主键外的属性名
        attrs['__select__'] = 'select `%s`, %s from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) values (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        #attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)


class Model(dict, metaclass=ModelMetaclass):
    def __init__(self, **kw):
       
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)
    
    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mappings__[key]
            print(field.default)
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                
                setattr(self, key, value)
        return value      

    def select_mysql(self,**kw):
        select_result=None
        args=[]
        primary_key=self.getValue("__primary_key__")
        str_sql_list=[]
        sp2l=[]
        sp="%s"
        between_str=[]
        like_str=[]
        str_order_by=""
        str_sql=self.__select__
        if kw:
            if "between" in kw.keys():
                bet=kw["between"]
                if type(bet) is list:
                    for betw in bet:
                        if type(betw) is dict:
                            for k,v in betw.items():
                                if type(v) is list and len(v)==2:
                                    between_str.append(k+" between " +sp + " and " + sp)  
                                    args.append(v[0])
                                    args.append(v[1])
                elif type(bet) is dict:
                    for k,v in bet.items():
                        if type(v) is list and len(v)==2:
                            between_str.append(k+" between " +sp + " and " + sp)
                            args.append(v[0])
                            args.append(v[1])
                str_sql_list.append(" and ".join(between_str))
                kw.pop("between")
            if "like" in kw.keys():
                like_1=kw['like']
                if type(like_1) is dict:
                    for k,v in like_1.items():
                        like_str.append("`"+k+"` like "+sp)
                        args.append('%'+v+'%')
                kw.pop("like")
            if "order" in kw.keys():
                
                orderby=kw["order"]
                if type(orderby) is dict:
                    str_order_by=" order by "+orderby.keys()[0]+"  "+orderby[orderby.keys()[0]]
                elif type(orderby) is list and len(orderby)==2:
                    str_order_by="order by "+orderby[0]+" "+orderby[1]
                elif type(orderby) is str:
                    str_order_by="order by "+orderby

                kw.pop("order")
            for k,v in kw.items():
                if k[-3:]=="_gt":
                    sp2l.append(k[:-3]+">"+sp)
                elif k[-3:]=="_ge":
                    sp2l.append(k[:-3]+">="+sp)
                elif k[-3:]=="_lt":
                    sp2l.append(k[:-3]+"<"+sp)
                elif k[-3:]=="_le":
                    sp2l.append(k[:-3]+"<="+sp)
                elif k[-3:]=="_ne":
                    sp2l.append(k[:-3]+"<>"+sp) 
                else:
                    sp2l.append(k+"="+sp)
                args.append(v)
            
            if like_str:
                str_sql_list.append(" and ".join(like_str)) 
            if sp2l:
                str_sql_list.append(" and ".join(sp2l)) 
            str_sql1=" ".join([str_sql,"where"," and ".join(str_sql_list),str_order_by])

        
        print(str_sql1)
        print(args)
        select_result=self.execute_select(str_sql1,args,True)
        

        return MModel(select_result,primary_key)


    def save_self(self):
        tableName=self.getValue('__table__')
        primaryKey=self.getValue('__primary_key__')
        sp=r'%s'
        if primaryKey:
            str_sql1="select * from "+tableName+" where "+primaryKey+"="+sp
            args1=[self.getValue(primaryKey)]
            if self.execute_select(str_sql1,args1):
                fields=[x for x in self.__fields__ if self.getValue(x)!=None]
                
                mappings=self.getValue('__mappings__')
                str_sql='update `%s` set %s ' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)))
                str_sql=str_sql.replace('?',sp)
                args=[ self.getValue(x) for x in self.__fields__ if self.getValue(x) !=None ]
        else:
            str_sql=self.getValue('__insert__').replace('?',"%s")
            args=[ self.getValue(x) for x in self.__fields__  ]
        print(str_sql)
        print(args)
        #row= self.exectue(str_sql,args)
        #return row


    def update_mysql(self, **kw):
        args=[ self.getValue(x) for x in self.__fields__ if self.getValue(x) !=None ]
        tableName=self.getValue('__table__')
        mappings=self.getValue('__mappings__')
        fields=[x for x in self.__fields__ if self.getValue(x)!=None]
        primaryKey=self.getValue('__primary_key__')
        str_sql='update `%s` set %s ' % (tableName, ', '.join(map(lambda f: '`%s`=?' % (mappings.get(f).name or f), fields)))
        sp=r'%s'
        str_sql=str_sql.replace('?',sp)
        str_sql_list=[]
        between_str=[]
        sp2l=[]
        rows=None
        if kw:
            if "between" in kw.keys():
                bet=kw["between"]
                if type(bet) is list:
                    for betw in bet:
                        if type(betw) is dict:
                            for k,v in betw.items():
                                if type(v) is list and len(v)==2:
                                    between_str.append(k+" between " +sp + " and " + sp)  
                                    args.append(v[0])
                                    args.append(v[1])
                elif type(bet) is dict:
                    for k,v in bet.items():
                        if type(v) is list and len(v)==2:
                            between_str.append(k+" between " +sp + " and " + sp)
                            args.append(v[0])
                            args.append(v[1])
                str_sql_list.append(" and ".join(between_str))
                kw.pop("between")
            
            for k,v in kw.items():
                if k[-3:]=="_gt":
                    sp2l.append(k[:-3]+">"+sp)
                elif k[-3:]=="_ge":
                    sp2l.append(k[:-3]+">="+sp)
                elif k[-3:]=="_lt":
                    sp2l.append(k[:-3]+"<"+sp)
                elif k[-3:]=="_le":
                    sp2l.append(k[:-3]+"<="+sp)
                elif k[-3:]=="_ne":
                    sp2l.append(k[:-3]+"<>"+sp) 
                else:
                    sp2l.append(k+"="+sp)
                args.append(v)
            if sp2l:
                str_sql_list.append(" and ".join(sp2l))
            
            str_sql=' '.join([str_sql,"where"," and ".join(str_sql_list)])
            print(str_sql)
            print(args)
            rows= self.exectue(str_sql,args)

        elif primaryKey:
            str_sql=str_sql+ ' where  `'+primaryKey+"` = "+sp
            args.append(self.getValue(primaryKey))
            print(str_sql)
            print(args)
            rows= self.exectue(str_sql,args)
        
        else:
            print("无更新条件")

        
        return rows


    def connection(self,dataname="im2006",us='root',pwd="111",host1="localhost",ch="utf8"):
        self.db= PooledDB(pymysql,maxconnections=8,host=host1,user=us,port=3306,passwd=pwd,db=dataname,charset=ch,use_unicode=True)
        



    def execute_select(self,stringsql,args,listname=False):
        dbb = self.db.connection()
        cur = dbb.cursor()
        ruturn_info=None
        #try:
        req = cur.execute(stringsql,args)
        col=cur.description
        info = cur.fetchall()
        if listname:
            ruturn_info=[dict(zip([xx[0] for xx in col],x)) for x  in info]
        else:
            ruturn_info=info
        #except Exception:
            #print("发生异常",Exception) 
        cur.close()
        dbb.close()
        return ruturn_info


    def exectue(self,stringsql,args):
        dbb = self.db.connection()
        cur = dbb.cursor()
        try:
            req = cur.execute(stringsql,args)
            dbb.commit()
        except Exception:
            print("发生异常",Exception) 
            dbb.rollback()
        
        cur.close()
        dbb.close()
        return req


class MModel(object):
    def __init__(self,select_result,primary_key=None):
        self.result=select_result
        
        self.primary_key=primary_key

    @classmethod
    def update(cls,**kw):
        pass
    
    @classmethod
    def bindFunction1(cls,name,select_r,*args):
        def func1(select_r,*args):
            print(select_r)
            return select_r  
        func1.__name__ = name
        return func1

class Field(object):

    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

class IntegerField(Field):

    def __init__(self, name=None, primary_key=False, default=0):
        super().__init__(name, 'bigint', primary_key, default)

class DoubleField(Field):
    def __init__(self, name=None, primary_key=False, default=0.0):
        super().__init__(name, 'double', primary_key, default)

class StringField(Field):

    def __init__(self, name=None, primary_key=False, default=""):
        super().__init__(name, 'string', primary_key, default)


if __name__ == "__main__":
    pass
    my=mysql_model("im2006",us='root',pwd="111",host1="127.0.0.1",ch="utf8")#("im2006",us='user',pwd="7940",host1="192.168.1.3",ch="utf8")
    fp=my.select([{"fd1_lk":"临"}],"reports",["fd1","fd3","person","carryondate","fd26"],{"carryondate":["2000-01-01","2015-11-01"]},True)
    df=pd.DataFrame(fp,columns=["fd1","fd3","person","carryondate","fd26"])
    print(fp)
    ex=model_excel()
    ex.xlwingwirte(df,"E:\\esx.xlsx","Sheet1",False,"A1")
