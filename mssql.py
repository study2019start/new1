import pymssql
import pandas as pd

class sql_server(object):
    def __init__(self,host,us,pwd,dataname,port):
        self.connect =pymssql.connect(host=host,user=us,password=pwd,database=dataname,port=port,charset='utf8')


    def insetms(self,tablename,valuel,valuev): #表名 
        cursor=self.connect.cursor()
        s=r"%s"
        sqlv=[]
        valuee=()
        if valuel and valuev:
            sql = "insert into " + tablename +" ("+",".join(valuel)+") values("
            for  vi in valuev:
                valuee=valuee+(vi,)
                sqlv.append(s)
            sql=sql+",".join(sqlv)+")"
            rs=cursor.execute(sql,valuev)
            self.connect.commit()
            cursor.close()
            return rs


    def updateorinsert(self,tablename,where,data,selectt): #表名   where 字典条件 更新或插入的内容   查找的列  第一个要和后面searchlist对应   要匹配的列
        cursor=self.connect.cursor()
        up=[]
        insert=[]
        value=()
        s=r"%s"
        if selectt:
            sp1=",".join(selectt)
        else:
            sp1="*"
        sqlselect="select "+sp1+" from  "+tablename
        if where :
            sp2="   where  "
            sp2l=[]
            for k,v in where.items():
                t=True
                if k[-3:]=="_gt":
                    sp2l.append(k[:-3]+">"+s)
                elif k[-3:]=="_ge":
                    sp2l.append(k[:-3]+">="+s)
                elif k[-3:]=="_lt":
                    sp2l.append(k[:-3]+"<"+s)
                elif k[-3:]=="_le":
                    sp2l.append(k[:-3]+"<="+s)
                elif k[-3:]=="_ne":
                    sp2l.append(k[:-3]+"<>"+s) 
                elif k[-3:]=="_in":     #in 后面要跟列表list
                    sp2l.append(k[:-3]+"  in ("+",".join([s for _ in range(len(v))])+")")
                    t=False
                else:
                    sp2l.append(k+"="+s)
                if t:
                    value=value+(v,)
                else:
                    for ii in range(len(v)):
                        value=value+(v[ii],)
            sp2=sp2+"and".join(sp2l)
        sp3=[sqlselect,sp2]
        selectlist="".join(sp3)

        cursor.execute(selectlist,value)
        r=[ row[0] for row in cursor.fetchall()]  #以查询出来的第一个作为匹配
        if where:
            sp=list(where.keys())[0]

            if sp.find("_")>=0:
                sp=sp[:-3]

            sw=[r[sp] for r in data]
            for ip,si in enumerate(sw):
                if  si not in r:
                    insert.append(ip)
                else:
                    up.append(ip)
            if insert:
                for ins in insert:
                    insql="insert into " +tablename
                    if data:
                        insql2="  values("
                        inv1=[]
                        inv2=[]
                        inv3=[]
                        for k,v in data[ins].items():
                            inv1.append(k)
                            inv2.append(s)
                            inv3.append(v)
                        insql3=insql+"("+",".join(inv1)+")"+insql2+",".join(inv2)+")"
                        print(insql3)
                        cursor.execute(insql3,tuple(inv3))
                        self.connect.commit()
            if up:
                upsql="update "+ tablename +" set "
                for upi in up:
                    if data:
                        upv1=[]
                        upv2=[]
                        for k,v in data[upi].items():
                            upv1.append(k+"="+s)
                            upv2.append(v)
                        upsql=upsql+",".join(upv1)
        
                        upsql=upsql+"  where "  +sp +r"=%s"
                        upv2.append(data[upi][sp])
                        print(upsql)
                        cursor.execute(upsql,tuple(upv2))
                        self.connect.commit()
        cursor.close()



        



    def select(self,tablename,where,selectlist=None):  #表名list   where的字典条件  要搜索的字段
        cursor=self.connect.cursor()
        sp1=""
        sp2=""
        s=r"%s"
        value=()
        
        if selectlist:
            sp1=",".join(selectlist)
        else:
            sp1="*"
        if where :
            sp2l=[]
            sp2="   where  "
            for k,v in where.items():
                t=True
                r=True
                if k[-3:]=="_gt":
                    sp2l.append(k[:-3]+">"+s)
                elif k[-3:]=="_ge":
                    sp2l.append(k[:-3]+">="+s)
                elif k[-3:]=="_lt":
                    sp2l.append(k[:-3]+"<"+s)
                elif k[-3:]=="_le":
                    sp2l.append(k[:-3]+"<="+s)
                elif k[-3:]=="_ne":
                    sp2l.append(k[:-3]+"<>"+s) 
                elif k[-3:]=="_in":     #in 后面要跟列表list
                    sp2l.append(k[:-3]+"  in ("+",".join([s for _ in range(len(v))])+") ")
                    t=False
                elif k[-3:]=="_ot":
                    sp2l.append(k[-3:]+"="+v)
                    r=False
                else:
                    sp2l.append(k+"="+s)
                if t:
                    if r:
                        value=value+(v,)
                else:
                    for ii in range(len(v)):
                        value=value+(v[ii],)

            sp2=sp2+" and ".join(sp2l)
        sp3=["select ",sp1,"  from ",",".join(tablename),sp2]

        selectlist="".join(sp3)
        print(selectlist)
        cursor.execute(selectlist,value)
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        r = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
        #r=cursor.fetchall()
        cursor.close()
        return r




#if __name__ == "__main__":
   # sql=sql_server("192.168.1.8","sa","ldpjwy","gjgl_xh","1433")
    #result=sql.select("dbo.bdgl",{"xh_ge":7000},None)
    #df1=pd.DataFrame(result)
   # df1.set_index("xh",inplace=True)
    #exm=model_excel()
    #exm.xlwingcreate(df1,"e:\\r1.xlsx")