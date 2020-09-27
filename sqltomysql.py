from mysqlmodel import mysql_model
from mssql import sql_server
import time
import datetime

class Run():
    def __init__(self,mshost,msuser,mspwd,msdataname,msport,ms_tablename,ms_lists,selectwhere,mysql_datname,mysql_us,mysql_pwd,mysql_host):
        self.ms_host=mshost
        self.ms_user=msuser
        self.ms_pwd=mspwd
        self.ms_dataname=msdataname
        self.ms_port=msport
        self.ms_table=ms_tablename
        self.selectwhere=selectwhere
        self.ms_list=ms_lists


        self.mysql_d=mysql_datname
        self.mysql_u=mysql_us
        self.mysql_p=mysql_pwd
        self.mysql_h=mysql_host


    def mssql_select(self):
        ms_sqll=sql_server(self.ms_host,self.ms_user,self.ms_pwd,self.ms_dataname,self.ms_port)
        return ms_sqll.select(self.ms_table,self.selectwhere,self.ms_list)
    
    def inser_or_update_mysql(self,list_ms,tablename):
        mysql=mysql_model(self.mysql_d,self.mysql_u,self.mysql_p,self.mysql_h)
        whe=[]
        searchwhere=[]
        for ms_l in list_ms:
            whe_dict={}
            search={}
            if ms_l['ybgxmbh'] : #有报告编号
                if ms_l['ybgxmbh'].find("XX") <0:
                    if ms_l['ybgxmbh'].find("G")>-1:#是个贷报告
                        whe_dict['fd1']=ms_l['ybgxmbh'][7:18]
                        whe_dict['person']="柴书钦"
                        whe_dict['depperson']="朱留青"
                        whe_dict['distrperson']="朱留青"
                    search["fd1"]=whe_dict['fd1']
                    whe_dict['district']=ms_l['xq']
                    whe_dict['fd3']=ms_l['xmmc']
                    whe_dict['buildingname']=ms_l['lpmc']
                    whe_dict['fd4']=ms_l['wtr']
                    whe_dict['fd7']=ms_l['zdkr']
                    whe_dict['startdate']=ms_l['qprq']
                    whe_dict['carryondate']=ms_l['qprq']
                    whe_dict['distrdate']=ms_l['qprq']
                    whe_dict['fd9']=ms_l['pgsd']
                    whe_dict['fd10']=ms_l['jsrq']
                    ls=str(ms_l['pgff']).split(',')
                    whe_dict['fd12']=" ".join(ls)
                    whe_dict['fd13']=ms_l['tdyt']
                    whe_dict['fd14']=ms_l['tdyt']
                    if ms_l['tdqbfs']:
                        whe_dict['landfeature']=ms_l['qsxz']
                    else:
                        whe_dict['landfeature']="国有"
                    whe_dict['fd16']=ms_l['tdqbfs']
                    if ms_l['jzmj']:
                        whe_dict['fd18']=ms_l['jzmj']
                    if ms_l['fczjz']:
                        whe_dict['fd20']=int(ms_l['fczjz'])
                    if ms_l['fdc_dj']:
                        whe_dict['fd21']=int(ms_l['fdc_dj'])
                    if ms_l['qzgjs']:
                        ls2=str(ms_l['qzgjs']).split(',')
                        whe_dict['fd25']=ls2[0]
                        whe_dict['signature']=ls2[-1:][0]
                    whe_dict['fd26']=ms_l['zgjs']
                    if ms_l['wtr']:
                        if ms_l['wtr'].find('工商'):
                            whe_dict['fd37']="中国工商银行"
                    if ms_l['xmly']:
                        sp=ms_l['xmly'].replace("支行","")
                        if sp=="漕河泾开发区":
                            whe_dict["fd38"]="漕河泾"
                        elif sp=="浦东开发区":
                            whe_dict["fd38"]="浦开发"
                        else:
                            whe_dict["fd38"]=sp
                    whe_dict['fd39']=ms_l['lxry']
                    whe_dict['fd41']="待审核"
                    searchwhere.append(search)
                    whe.append(whe_dict)
        if whe:
            mysql.updateorinsertmany(whe,searchwhere,tablename)
                





if __name__ == "__main__":
    d1=datetime.datetime.now()
    ddt1=datetime.timedelta(minutes=110)
    ddt2=datetime.timedelta(minutes=20)
    d2=d1-ddt1
    d3=d1+ddt2
    m_h="192.168.1.8"
    m_user="sa"
    m_pwd="ldpjwy"
    m_d="gjgl_xh"
    m_port=1433
    dd1=d2.strftime("%Y-%m-%d %H:%M:%S")
    dd2=d3.strftime("%Y-%m-%d %H:%M:%S")
    ms_table=["bdgl"]
    
    mslist={'wcsj_ge':dd1,'wcsj_le':dd2}
    selectlist=['ybgxmbh','xq','xmmc','lpmc','lxry','qprq','pgsd','jsrq','pgff','jzmj','fczjz','fdc_dj','qzgjs','zgjs','wtr','xmly','zdkr','tdyt','qsxz','tdqbfs']

    mysql_datname="im2006"
    mysql_us="root"
    mysql_pwd="111"
    mysql_host="localhost"
    mstomysql=Run(m_h,m_user,m_pwd,m_d,m_port,ms_table,selectlist,mslist,mysql_datname,mysql_us,mysql_pwd,mysql_host)
    ms_result_list=mstomysql.mssql_select()
     
    mysql_table="reports"
    mstomysql.inser_or_update_mysql(ms_result_list,mysql_table)


    