from access import access_model as ac
from keyboard import *
from pymouse import *
import time
from mysqlmodel import Model,IntegerField,StringField,DoubleField,mysql_model
import pyautogui as pag
from PIL import Image
import os
import numpy as np
import pandas as pd
from excel import  model_excel
from mssql import sql_server
import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

class A:

    def __init__(self, name, age):
        self.name =name
        self.age = age

    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            obj = object.__new__(cls)
            cls.__instance = obj
        return cls.__instance

 
 



    

def gb(lis):

    le=len(lis)
    if le <=1:
        return lis
    f=int(le/2)
    a1=gb(lis[:f])
    a2=gb(lis[f:])
    print(a1)
    print(a2)
    result= merge(a1)+merge(a2)
    return merge(result)
def merge(ls):
    f=len(ls)
    mid=int(f/2)
    i=0
    j=mid
    b=[]
    while i< mid and j<f:
        if ls[i]>ls[j]:
            b.append(ls[j])
            j=j+1
        else:
            b.append(ls[i])
            i=i+1
    while i<mid:
        b.append(ls[i])
        i=i+1
    while j<f:
        b.append(ls[j])
        j=j+1
     
    return b

class SomeClass(object):
    some_var = 15
    some_list = [3]
    another_list = [5]
    def __init__(self,x):
        self.some_var = x + 1
        self.some_list = self.some_list + [x]
        self.another_list += [x]


class spp(SomeClass):
    some_var1 = 15
    spp2=16
    some_list = [5]
    #another_list = [6]
    def __init__(self,x):
        super(spp,self).__init__(x)
        self.some_var1 =x
        

def st1(i=2,ii=4,iii=6):
    print(i,"\n",ii,"\n",iii)

class mm(Model):
    __table__="reports"
    fd1=StringField("fd1",True,0)
    fd20=DoubleField("fd20",False)
    fd3=StringField("fd3",False)
    fd26=StringField("fd26",False)
    fd36=DoubleField("fd36",False)

def compress_image(infile, outfile='', mb=1536, step=1, quality=85):
    """不改变图片尺寸压缩到指定大小
    :param infile: 压缩源文件
    :param outfile: 压缩文件保存地址
    :param mb: 压缩目标，KB
    :param step: 每次调整的压缩比率
    :param quality: 初始压缩比率
    :return: 压缩文件地址，压缩文件大小
    """
    i=20
    o_size = get_size(infile)
    if o_size <= mb:
        return infile
    if outfile:
        pass
    else:
        outfile = infile
    try:
        while o_size > mb:
            im = Image.open(infile)
            im.save(outfile, quality=quality)
            if i - step < 0:
                break
            i=i-1
            quality -= step
            o_size = get_size(outfile)
            print(o_size)
    except:
        print("--------图片已经损坏------------")
        print(outfile)
        print("-------------------------------")
    return outfile, get_size(outfile)


def get_size(file):
    # 获取文件大小:KB
    size = os.path.getsize(file)
     
    return size / 1024
    
a=[]
def bianli(path,find):
    global a
    if os.path.exists(path):
        list1 = os.listdir(path) #列出文件夹下所有的目录与文件
        for i in range(0,len(list1)):
            path1 = os.path.join(path,list1[i])
            if os.path.isfile(path1):
                for f in find:
                    if path1.find(f)>0:
                        a.append(path1)
            else:
                bianli(path1,find)

def bianli2(path,dir_list):
    if os.path.exists(path):
        list1 = os.listdir(path) #列出文件夹下所有的目录与文件
        for i in range(0,len(list1)):
            path1 = os.path.join(path,list1[i])
            if os.path.isfile(path1):
                pass
            else:
                dir_list.append(path1)
                bianli2(path1,dir_list)


def find1(path1,bianhao): # 动迁系统查询 是否认领完毕  path1动迁照片路径  bianhao系统内总报告编号
    df_m=model_excel()
    mm2=sql_server("192.168.1.8","sa","ldpjwy","gjgl_xh","1433")
    r2=mm2.select("dbo.cq1",{'gdbh':13431,'zl_ne':'','zgjs':'王昱鹏'},['bcqrxm'])
    df11=[ x['bcqrxm'].replace("（亡）","").replace("(亡）","") for x in r2 ]
    # df1=df_m.readexcel("E:\\21.xlsx",0,None,1,"H")
    # df1.dropna(axis=0,inplace=True)
    # df1[7]=df1[7].apply(lambda  x: x.replace("（亡）","").replace("(亡）",""))
    # df11=df1.iloc[:,0].tolist()
    ls1=[]
    bianli2(path1,ls1)
    #print(ls1)
    t=True
    for name in ls1:
        for pp in df11:
            if name.find(pp)>-1:
                t=False
                break
        if t:
            print(name)
        else:
            t=True

def mysql_shen_qian(n1,n2,lst):
    t=mysql_model("im2006",'user',pwd="7940",host1="192.168.1.3",ch="utf8")
    #t=mysql_model("im2006")
    f=["fd1"]
    #fd1=[["X2021-00300","X2021-00601"]]
    fd1=lst
    select_list=['id','fd1','fd29','fd41','fd27','fd28','auditlevel','fd10','fd25','signature','fd37']
    result=t.selectmul(f,"reports",fd1,select_list,True)
    g_ls=[]
    where_ls=[]
    print(result)

    for r1 in result:
        where_1={}
        if not r1['auditlevel']:

            r1['auditlevel']='B'
        if r1["fd41"]=='待归档':
            pass
        else:
            r1["fd41"]='待归档'
            if r1["fd28"]:
                pass
            else:
                r1["fd28"]=r1["fd10"].strftime("%Y-%m-%d")
            if r1['fd29']:
                pass
            else:
                if r1['fd37']:
                    if r1['fd37'].find("银行")>-1:
                         r1['fd29']='陈伟林'
                    else:
                         r1['fd29']='齐刚'
                else:
                    r1['fd29']='陈伟林'
            if r1["fd27"]:
                pass
            else:
                if r1['fd25']==n1 or r1['fd25']==n2:
                    r1['fd27']=r1['fd25']
                elif r1['signature']==n1 or r1['signature']==n2:
                    r1['fd27']=r1['signature']
                else:
                    if r1['fd1'][0:1]=="G":
                        r1['fd27']='齐刚' 
                    else:
                        r1['fd27']='陈伟林'
        r1.pop("signature")
        r1.pop("fd25")
        r1.pop("fd10")
        r1.pop("fd37")
        where_1["id"]=r1.pop("id")
        g_ls.append(r1)
        where_ls.append(where_1)
    print(g_ls)
    t.update(g_ls,where_ls,"reports")
    # result=t.selectmul(f,"reports",fd1,select_list,True)
    # print(result)
        
                
        
def beian_read_test(url,cookie_1):
    header={}
    header["User-Agent"]="Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; Media Center PC 6.0)"
    header["Accept"]="application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*"
    header["Accept-Encoding"]="gzip, deflate"
    header["Accept-Language"]="zh-CN"
    re1=r"沪信衡估报字（(\d{4})）第([A-Za-z])(\d{5})号$"
    re2=r"[\s\S]*共(\d{1,7})页[\s\S]*"
    result_1=requests.get(url,headers=header,cookies=cookie_1) 
    result_1.encoding=result_1.apparent_encoding
    ii=1
    s=result_1.text
    soup = BeautifulSoup(s, 'lxml')
    td=soup.select("td[class='trlight']")
    
    
    if s.find("无记录")>-1:
        pass
    else:
        if re.match(re2,s):
            iil=re.search(re2,s).group(1)

            ii=int(iil)

    print(ii)
    

    lp=[]
    report_id_fd1=""
    i=1
    if td:
        for t1 in td:
            if i%12==4:
                s=t1.string
                if s.find("沪信衡估报字第")>-1:
                    report_id_fd1=s.replace("沪信衡估报字第","").replace("号","")
                    if len(report_id_fd1)==11:
                        lp.append(report_id_fd1)

                elif s.find("沪信衡估报字（")>-1:
                    if(re.match(re1,s)):
                        re_1=re.search(re1,s)
                        report_id_fd1="".join([re_1.group(2),re_1.group(1),"-",re_1.group(3)])
                        lp.append(report_id_fd1)

                
            i=i+1
    if ii>1 :
        for iii in range(2,ii+1):
            url1=url.replace("page=1","page="+str(iii))
            print(url1)
            result_1=requests.get(url1,headers=header,cookies=cookie_1) 
            result_1.encoding=result_1.apparent_encoding
            s=result_1.text
            soup = BeautifulSoup(s, 'lxml')
            td=soup.select("td[class='trlight']")
            lp1=[]
            report_id_fd1=""
            i=1
            if td:
                for t1 in td:

                    if i%12==4:
                        s=t1.string
                        if s.find("沪信衡估报字第")>-1:
                            report_id_fd1=s.replace("沪信衡估报字第","").replace("号","")
                            if len(report_id_fd1)==11:
                                lp1.append(report_id_fd1)

                        elif s.find("沪信衡估报字（")>-1:
                            if(re.match(re1,s)):
                                re_1=re.search(re1,s)
                                report_id_fd1="".join([re_1.group(2),re_1.group(1),"-",re_1.group(3)])
                                lp1.append(report_id_fd1)
                    i=i+1
                print(lp1)
                lp=lp+lp1
    print(lp)
    return lp


def beian_read(url,cookie_1,re1):
    header={}
    header["User-Agent"]="Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; Media Center PC 6.0)"
    header["Accept"]="application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*"
    header["Accept-Encoding"]="gzip, deflate"
    header["Accept-Language"]="zh-CN"
    #re1=r"沪信衡估报字（(\d{4})）第([A-Za-z])(\d{5})号$"
    re2=r"[\s\S]*共(\d{1,7})页[\s\S]*"
    result_1=requests.get(url,headers=header,cookies=cookie_1) 
    result_1.encoding=result_1.apparent_encoding
    ii=1
    s=result_1.text
    soup = BeautifulSoup(s, 'lxml')
    td=soup.select("td[class='trlight']")
    
    
    if s.find("无记录")>-1:
        pass
    else:
        if re.match(re2,s):
            iil=re.search(re2,s).group(1)

            ii=int(iil)

    print(ii)
    

    lp=[]
     
    i=1
    if td:
        for t1 in td:
            if i%12==4:
                s=t1.string
                if(re.match(re1,s)):
                    re_1=re.search(re1,s)
                    #report_id_fd1="".join([re_1.group(2),re_1.group(1),"-",re_1.group(3)])
                    lp.append(re_1.group(1))

                
            i=i+1
    if ii>1 :
        for iii in range(2,ii+1):
            url1=url.replace("page=1","page="+str(iii))
            print(url1)
            result_1=requests.get(url1,headers=header,cookies=cookie_1) 
            result_1.encoding=result_1.apparent_encoding
            s=result_1.text
            soup = BeautifulSoup(s, 'lxml')
            td=soup.select("td[class='trlight']")
            lp1=[]
            
            i=1
            if td:
                for t1 in td:

                    if i%12==4:
                        s=t1.string

                        if(re.match(re1,s)):
                            re_1=re.search(re1,s)
                            #report_id_fd1="".join([re_1.group(2),re_1.group(1),"-",re_1.group(3)])
                            lp1.append(re_1.group(1))
                    i=i+1
                
                lp=lp+lp1
    print(lp)
    xls2=pd.DataFrame(lp)
    xls2['nn']=1
    return xls2

def select(t={'gdbh':13431,'hnbh':1},list1=['bgbh','qz','fh']):
    mm2=sql_server("192.168.1.8","sa","ldpjwy","gjgl_xh","1433")
    r2=mm2.select("dbo.cq1",t,list1)
    xls1=pd.DataFrame(r2)
    
    return xls1

def bijiao_excel(x1,x2):
    r=pd.merge(x1,x2,how='left')
    r.fillna(value=-99)
    r.sort_values(by="nn")
    f_excel=model_excel()
    n_t=time.strftime("%Y%m%d%H%M%S",time.time())
    f_excel.xlwingcreate(r,r"e:\bj_sl"+n_t+r".xlsx")


def read_beian_url(num,modifytime=''):

    url="http://183.194.243.149:7001/WebRoot/gjba/gjbgba/list/auditedList.jsp?projectName=&client=&modifyTimeStart="+modifytime+"&modifyTimeEnd=&assessAimMain=&reportNum=&reportNO=2021&addTimeStart=&addTimeEnd=&estimator=&instName=&household=&reportDateStart=&reportDateEnd=&location=&page=1&rows="+str(num)+"&okey=&order="
    return url

def shenhe_test(reportid,cookie_1):
    header={}
    header["User-Agent"]="Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 6.1; WOW64; Trident/7.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; .NET4.0C; .NET4.0E; Media Center PC 6.0)"
    header["Accept"]="application/x-ms-application, image/jpeg, application/xaml+xml, image/gif, image/pjpeg, application/x-ms-xbap, */*"
    header["Accept-Encoding"]="gzip, deflate"
    header["Accept-Language"]="zh-CN"
    url_1="http://183.194.243.149:7001/WebRoot/gjba/gjbgba/list/auditList.jsp?projectName=&client=&assessAimMain=&reportNO=&estimator=&addTimeStart=&addTimeEnd=&instName=&household=&reportDateStart=&reportDateEnd=&location="
    url="http://183.194.243.149:7001/WebRoot/gjba/gjbgba/list/auditList.jsp?projectName=&client=&assessAimMain=&reportNO="+reportid+"&estimator=&addTimeStart=&addTimeEnd=&instName=&household=&reportDateStart=&reportDateEnd=&location=&page=1&rows=3200&okey=&order="
    result_1=requests.get(url,headers=header,cookies=cookie_1) 
    result_1.encoding=result_1.apparent_encoding
    s=result_1.text
    soup = BeautifulSoup(s, 'lxml')
    td=soup.select("input[name='check_box']")
    
    if td:
        for t1 in td:
            print(t1["value"])

            url1="http://183.194.243.149:7001/WebRoot/gjba/gjbgba/list/reportAudit.do?editReportID="+str(t1["value"])
            result_2=requests.get(url1,headers=header,cookies=cookie_1) 
            result_2.encoding=result_2.apparent_encoding
            s=result_2.text
            soup = BeautifulSoup(s, 'lxml')
            td=soup.select("input[id='diagID']")
            search=td[0]["value"]
            if search !=None and search != "":
                url2="http://183.194.243.149:7001/WebRoot/gjba/gjbgba/list/searchDiagnostic.do"
                d={}
                d["diagID"]=search
                print(search)
                result_3=requests.post(url2,headers=header,cookies=cookie_1,data=d) 
                print(result_3.text)
            if t1["value"]!="" and t1["value"]!=None :
                url3="http://183.194.243.149:7001/WebRoot/gjba/gjbgba/list/submitReport.do"
                d1={}
                d["reportID"]=t1["value"]
                d["status"]=2
                d["opinion"]=r"%E5%90%8C%E6%84%8F%EF%BC%81"
                result_3=requests.post(url3,headers=header,cookies=cookie_1,data=d1) 
                if result_3.text:
                    print(result_3.text)
                    requests.get(url_1,headers=header,cookies=cookie_1)



                
def dui_bi():
    mm2=sql_server("192.168.1.8","sa","ldpjwy","gjgl_xh","1433")
    r2=mm2.select("dbo.cq1",{'gdbh':13431,'zl_ne':'','zgjs':''},['bcqrxm','zl'])
    df11=[ x['bcqrxm'].replace("（亡）","").replace("(亡）","").replace("等","") for x in r2 ]
    b2=[]
    bianli2(r"\\192.168.1.5\动迁资料\黄浦征收项目\2021黄浦区厦门路地块（110、111、133、134街坊）旧城区改建项目\照片\110、111、134（四所）照片",b2)
    print(df11)
    for ls in df11:
        for ddf11 in b2:
            if ddf11.find(ls)>-1:
                print(ddf11)
                break

if __name__ == "__main__":
    # mm1=mm()
    # mm1.fd1="F2020-00100"
    # mm1.fd20=299
    # mm1.fd3=None
    
    #mm1.connection() mm1.save_self()


    co={'JSESSIONID':'jg5DgptTxCMmtf1hKnTGQzdwYMq8GSYSJtX2pbvYG0hqWHkdXzN3!1176869032'}
    
    
    # reportid=r"%BB%A6%D0%C5%BA%E2%B9%C0%B1%A8%D7%D6%B5%DAF2020-00366%BA%C5-J-954"
 
    

    url=read_beian_url(3600)
    # ls=beian_read_test(url,co)
    # ##shenhe_test(reportid,co)
    # mysql_shen_qian("童定祥","张爱军",[ls])
    



    # mm2=sql_server("192.168.1.8","sa","ldpjwy","gjgl_xh","1433")
    # r2=mm2.select("dbo.cq1",{'gdbh':13431,'zl_ne':'','zgjs':'王昱鹏'},[])
    # f_excel=model_excel()
    # df=pd.DataFrame(r2)
    # f_excel.xlwingcreate(df,r"e:\sl.xlsx")
    # print(df)

    #find1(r"F:\BaiduYunDownload\厦门路地块")  #查询动迁 匹配文件夹中被征收人和系统中的被征收人
    #zgjs 认领人
    #zl 坐落
    #bcqrxm 被征收人姓名
    #pgsd 价值时点
    #gdbh 总编号id
    #hybw 部位
    #cqr 委托方
    #mjxz 房屋类型
    #qsxz  公有或私有
    #jqdj  加权单价
    #qz 签字估价师1  qzzs 签字估价师2
    #fwfssb 问题列表


#################缩小图片###############
    # ls=r"F:\地价\厦门路装修"
    # bianli(ls,["jpg","JPG"])
    # for aa in a :
    #     f=aa[aa.rfind("\\")+1:]
    #     print(f)
    #     compress_image(aa)
#################缩小图片###############   
    

    #r1=mm1.select_mysql(like={"fd1":"G"},between={"fd10":["2021-01-04","2021-01-05"]})
    #print(r1.result)
    
    
    re1=r"沪信衡估报字第F2021-00252号-([A-Z]{1,3}-\d{1,4})"
    x1=beian_read(url,co,re1)
    x2=select()
    print(x1)
    print(x2)
    #bijiao_excel(x2,x1)



    # t=PyMouse()
    # x,y=pag.position() 
    # ft=time.time()
    # while True:
    #     t.click(x,y,1)
    #     time.sleep(3)
    #     t.click(x,y,1)
    #     time.sleep(9*60)
    #     if time.time()-ft> 60*60*3.3:
    #         break





    # ret1 = A("小明", 20)
    # ret2 = A("小花", 28)
    # ret3 = A("小白", 34)
    # print(ret1.__dict__)
    # sp=[2,1]
    # st1(i=5,iii=33)
    # a=1
    # b=a
    # a=b+1
    # print(a,b)
    # sp1=spp(7)
    # sp2=spp(77)
    # print(sp1.another_list)
    # print(sp1.some_list)
    # print(SomeClass.another_list)
    # print(sp2.another_list)
    # spp.spp2=17
    # sp1.spp2=[2,3,6]
    # print(sp1.spp2)
    # print(sp2.spp2)
    # print(spp.spp2)
    #m=ac(r"F:\地价\test\test\conn\Database1.accdb")
    #p=m.muselect({'dizhi':"青浦区华新镇蒋家巷路东侧44-02地块"},'bj_table')
    #