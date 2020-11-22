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

                    if ms_l['pgmd']=='房地产抵押估价':
                        whe_dict['fd11']='抵押价值评估'
                    
                    

                    whe_dict['category']=ms_l['ybgxmbh'][0]
                    
                    search["fd1"]=whe_dict['fd1']
                    if str(ms_l['xq']).find("崇明")>-1:
                        whe_dict['district']="崇明县"
                    else:
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
                    if ms_l['bgnr']=='居住' or ms_l['bgnr']=='住宅':
                        whe_dict['fd13']='住宅'
                        whe_dict['fd14']='住宅'
                        whe_dict['fd15']='住宅'
                    if ms_l['qsxz'].find("集体")>-1:
                        whe_dict['landfeature']="集体"
                    else:
                        whe_dict['landfeature']="国有"
                    whe_dict['fd16']=ms_l['tdqbfs']
                    if ms_l['jzmj']: #建筑面积
                        whe_dict['fd18']=ms_l['jzmj']
                    if ms_l['fczjz']:#总价
                        whe_dict['fd20']=int(ms_l['fczjz'])
                    if ms_l['fdc_dj']: #单价
                        whe_dict['fd21']=int(ms_l['fdc_dj'])
                    if ms_l['qzgjs']: #签字估价师
                        ls2=str(ms_l['qzgjs']).split(',')
                        whe_dict['fd25']=ls2[0]
                        whe_dict['signature']=ls2[-1:][0]
                    whe_dict['fd26']=ms_l['zgjs']
                    if ms_l['wtr']:         #来源
                        if ms_l['wtr'].find('工商'):
                            whe_dict['fd37']="中国工商银行"
                    if ms_l['xmly']:         #支行
                        sp=ms_l['xmly'].replace("支行","")
                        if sp=="漕河泾开发区":
                            whe_dict["fd38"]="漕河泾"
                        elif sp=="浦东开发区":
                            whe_dict["fd38"]="浦开发"
                        else:
                            whe_dict["fd38"]=sp
                    whe_dict['fd39']=ms_l['lxry']
                    whe_dict['fd41']="待审核"
                    fd31=0.5
                    if  whe_dict["district"]=="崇明县" or  whe_dict["district"]=="外省市":
                        fd31+=2
                    elif whe_dict["district"]=="金山区":

                        fd31+=1
                    elif whe_dict["district"]=="南汇区" or whe_dict["district"]=="奉贤区" or whe_dict["district"]=="嘉定区" or whe_dict["district"]=="松江区" or whe_dict["district"]=="青浦区" :
                        fd31+=0.5
                        

                    whe_dict['fd31']=fd31
                    fd31b=0.5
                    if whe_dict['category'] =="F" or whe_dict['category'] =="X":
                        if whe_dict['fd11'] !="财产鉴证" and whe_dict['fd11'] !="赠与、继承" and whe_dict['fd11'] !='房地产课税评估':
                            fd31b+=1

                    elif whe_dict['category'] =="T":
                        fd31b+=2
                    if whe_dict['fd37']=='法院':
                        fd31b+=2
                    elif whe_dict['fd37']!="中国工商银行":
                        fd31b+=0.5
                    if whe_dict['category'] =="F" or whe_dict['category'] =="X" or whe_dict['category'] =="T":
                        if whe_dict['fd20']>10000:
                            fd31b+=1
                        elif whe_dict['fd20']>1000:
                            fd31b+=0.5
                    whe_dict['fd31b']=fd31b
                    searchwhere.append(search)
                    whe.append(whe_dict)
        if whe:
            mysql.updateorinsertmany(whe,searchwhere,tablename)
                





if __name__ == "__main__":
    d1=datetime.datetime.now()
    ddt1=datetime.timedelta(minutes=5410)
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
    selectlist=['ybgxmbh','xq','xmmc','lpmc','lxry','qprq','pgsd','jsrq','pgff','jzmj','fczjz','fdc_dj','qzgjs','zgjs','wtr','xmly','zdkr','bgnr','qsxz','tdqbfs','pgmd']

    mysql_datname="im2006"
    mysql_us="root"
    mysql_pwd="111"
    mysql_host="localhost"
    mstomysql=Run(m_h,m_user,m_pwd,m_d,m_port,ms_table,selectlist,mslist,mysql_datname,mysql_us,mysql_pwd,mysql_host)
    ms_result_list=mstomysql.mssql_select()
     
    mysql_table="reports"
    mstomysql.inser_or_update_mysql(ms_result_list,mysql_table)


    