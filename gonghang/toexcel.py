from set import setline,setaes
import os
import xlwt
import time
import uuid
import socket
import json
import configparser
import math
import hashlib
import base64
from mssql import sql_server

shname="shapp.housepledge.xinheng"

def exlcelwrite(a, filename):
    book = xlwt.Workbook()            #创建excel对象
    sheet = book.add_sheet('sheet1')  #添加一个表
    c = 0  
    for d in a: #取出data中的每一个元组存到表格的每一行
        for index in range(len(d)):   #将每一个元组中的每一个单元存到每一列
            sheet.write(c,index,d[index])
        c += 1
    book.save(filename)

def zhuanshijianchuo(stri1):
    time1 = time.strptime(stri1,"%Y-%m-%d %H:%M:%S")
    timea=int(time.mktime(time1)*1000)
    print(timea)
    return timea

def getip():
    myname=socket.getfqdn(socket.gethostname())
    myaddr=socket.gethostbyname(myname)
    return myaddr+","+myname


def file_rtow(filenamep,chunkr):
    fsize=os.path.getsize(filenamep)
    chunkcount=math.ceil(fsize/chunkr)
    print(chunkcount)
    i=0
    filename=filenamep[0:filenamep.rfind(".")]+time.strftime("%Y%m%d%H%M%S")+filenamep[filenamep.rfind("."):]
    with open(filenamep,'rb') as fr:
        with open(filename,'wb') as fw:
            while i<chunkcount:
                fr.seek(i*chunkr)
                m=fr.read(chunkr)
                print(m)
                fw.write(m)
                i=i+1
             
         
def getMD5(path):
    with open(path, 'rb') as fp:
        data = fp.read()
    file_md5= hashlib.md5(data).hexdigest().upper()
    print(file_md5)     

def bianli(path,find):
    a=[]
    b=[]
    if os.path.exists(path):
        list1 = os.listdir(path) #列出文件夹下所有的目录与文件
        for i in range(0,len(list1)):
            path1 = os.path.join(path,list1[i])
            if os.path.isfile(path1) and path1.find(find)>0:
                    a.append(path1)
                    b.append(list1[i].replace('.pdf',''))

    return a,b



def upload(fpath,applyNo,empname): #applyNo 是List
    
    sql=sql_server("192.168.1.8","sa","ldpjwy","gjgl_xh","1433")
    
    mulupdata=[]
    result=sql.select("dbo.bdgl",{"zbgh_in":applyNo},['zgjs','zbgh','zl','jzmj','fdc_dj','fczjz','zcs','szc','fwlx','ybgxmbh'])
    if result:
        for r1 in result:
            if r1['zbgh'] and  r1['jzmj'] and r1['fdc_dj'] and r1['fczjz'] and r1['zcs'] and r1['szc'] and r1['fwlx'] and r1['ybgxmbh']:
                updata={}
                t=time.strftime("%Y%m%d%H%M%S",time.localtime())+'000000'
                fileuid=base64.b64encode(t.encode('utf-8'))
                updata["corpId"]="ASS00113"
                updata["emplName"]=empname
                updata["applyNo"]=r1['zbgh']
                updata['assessAddress']=r1['zl']
                updata['assessArea']=float(r1['jzmj'])
                updata['assessUnitPrice']=int(r1['fdc_dj'])
                updata['assessTotalPrice']=int(r1['fczjz'])
                updata['totalFloor']=int(r1['zcs'])
                updata['floor']=int(r1['szc'])
                updata['orientation']='朝南'
                updata['houseType']=r1['fwlx']
                updata['schoolHouse']=0
                updata['bronzeMedal']=0
                updata['assessStatus']=7
                updata['assessNo']=r1['ybgxmbh']
                updata['fileUnifiedNo']=fileuid
                updata['reportId']=r1['ybgxmbh']
                mulupdata.append(updata)

           

def muldup(updata,fpath):
    chunkr=512
    s=setline()
    s.seturl("/shlocal/housepledge/assessplate/save/assessment")#housepledge/assessplate/query/applylist
    s.setshappid(shname)
    s.setmsg(json.dumps(updata))
    getnameip = str(getip()).split(",")
    s.setip(getnameip[0])
    s.setname(getnameip[1])
    ss = setaes(s)
    uuid1=uuid.uuid1()
    result1=ss.dopost(uuid1)
    print(result1)
    if result1:
        if result1[0]=='0':
            fsize=os.path.getsize(fpath)
            chunkcount=math.ceil(fsize/chunkr)
            i=0
            with open(fpath,'rb') as fr: #读取文件开始上传报告
                while i<chunkcount:
                    fr.seek(i*chunkr)
                    m=base64.b64decode(fr.read(chunkr))
                    i=i+1
                    upl={}
                    upl['corpId']="ASS00113"
                    upl['empIName']= updata["emplName"]
                    upl['fileName']=fpath[fpath.rfind("\\")+1:]
                    upl['chunk']=i
                    upl['chunks']=chunkcount
                    upl['fileContent']=m
                    upl['fileUnifiedNo']=updata['fileUnifiedNo']
                    s.setmsg(json.dumps(upl))
                    uuid2=uuid.uuid1()
                    r2=ss.dopost(uuid2)
                    print(r2)

def to_excel(t1,t2,name):
    s =setline()
    s.seturl("/shlocal/housepledge/assessplate/query/applylist")#housepledge/assessplate/query/applylist
    s.setshappid("shapp.housepledge.xinheng")
   # tim=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
   # s.setmsg("{\"corpId\":\"ASS00113\",\"emplName\":\"王海琼\",\"settleStatus\":\"1\"}")
    s.setmsg("{\"corpId\":\"ASS00113\",\"emplName\":\""+name+"\",\"startDate\":\""+str(zhuanshijianchuo(t1))+"\",\"endDate\":\""+str(zhuanshijianchuo(t2))+"\",\"assessStatus\":\"7\"}")
    getnameip = str(getip()).split(",")
    s.setip(getnameip[0])
    s.setname(getnameip[1])
    ss = setaes(s)
    uuid1=uuid.uuid1()
    #print(json.loads((list(ss.dopost(uuid1))[1]))['rows'])
    result1=ss.dopost(uuid1)
    print(result1)
    laresult=[]
    if result1:
        if result1[0]=='0':
            result2=json.loads(result1[1])['rows']
            result3=[list(a.values()) for a in result2]
            result4=list(result2[0].keys())
            laresult.append(result4)
            for ff in result3:
                sf=ff[0]
                ff[0]=time.strftime("%Y-%m-%d", time.localtime(int(sf/1000)))
                laresult.append(ff)
            exlcelwrite(laresult, time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))+".xls")


if __name__=="__main__":
   f="E:\\436.pdf"
   r=512
   getMD5(f)
   #file_rtow(f,r)

            #print(laresult)
    #exlcelwrite(laresult, "xls//"+time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))+".xls")