import pymssql
import pandas as pd
from excel import model_excel
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

    def select(self,tablename,where,selectlist=None):  #表名   where的字典条件  要搜索的字段
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
                value=value+(v,)
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
                    sp2l.append(k[:-3]+"in ("+",".join([s for _ in range(len(v))])+")")
                else:
                    sp2l.append(k+"="+s)
            sp2=sp2+"and".join(sp2l)
        sp3=["select ",sp1,"  from ",tablename,sp2]

        selectlist="".join(sp3)
        
        cursor.execute(selectlist,value)
        desc = cursor.description  # 获取字段的描述，默认获取数据库字段名称，重新定义时通过AS关键重新命名即可
        r = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()]  # 列表表达式把数据组装起来
        #r=cursor.fetchall()
        cursor.close()
        return r




if __name__ == "__main__":
    sql=sql_server("192.168.1.8","sa","ldpjwy","gjgl_xh","1433")
    result=sql.select("dbo.bdgl",{"xh_ge":7000},None)
    df1=pd.DataFrame(result)
    df1.set_index("xh",inplace=True)
    exm=model_excel()
    exm.xlwingcreate(df1,"e:\\r1.xlsx")