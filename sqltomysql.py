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
        ms_sqll.select(self.ms_table,self.selectwhere,self.ms_list)
    




if __name__ == "__main__":
    d1=datetime.datetime.now()
    ddt1=datetime.timedelta(minutes=60)
    ddt2=datetime.timedelta(minutes=20)
    d2=d1-ddt1
    d3=d1+dd2
    m_h="192.168.1.8"
    m_user="sa"
    m_pwd="ldpjwy"
    m_d="gjgl_xh"
    m_p=1433
    dd1=d1.strftime("%Y-%m-%d %H:%M:%S")
    dd2=d3.strftime("%Y-%m-%d %H:%M:%S")
    mslist={'wcsj_ge':dd1,'wscj_le':dd2}
    selectlist=['ybgxmbh','xq','xmmc','lxry','qprq','pgsd','jsrq','pgff','jzmj','fczjz','fdc_dj','qzgjs','zgjs','wtr','xmly','zdkr','tdyt','qsxz','tdqbfs']


    