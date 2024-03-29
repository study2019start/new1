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
from multiprocessing import Process,Queue,Lock,Pool,Manager
import re
shname="shapp.housepledge.xinheng"

def exlcelwrite(a, filename,c=0):
    book = xlwt.Workbook()            #创建excel对象
    sheet = book.add_sheet('sheet1')  #添加一个表
     
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
    filename=filenamep[:filenamep.rfind(".")]+time.strftime("%Y%m%d%H%M%S")+filenamep[filenamep.rfind("."):]
    with open(filenamep,'rb') as fr:
        with open(filename,'wb') as fw:
            while i<chunkcount:
                fr.seek(i*chunkr)
                m=base64.b64encode(fr.read(chunkr)).decode()
                print(m)
                fw.write(base64.b64decode(m))
                i=i+1
             
         
def getMD5(path):
    with open(path, 'rb') as fp:
        data = fp.read()
    file_md5= hashlib.md5(data).hexdigest().upper()
    print(file_md5)     

def bianli(path,find):
    #a=[]
    b=[]
    if os.path.exists(path):
        list1 = os.listdir(path) #列出文件夹下所有的目录与文件
        for i in range(0,len(list1)):
            path1 = os.path.join(path,list1[i])
            if os.path.isfile(path1) and path1.find(find)>0:
                    #a.append(path1)
                    b.append(list1[i].replace('.pdf',''))

    return b



def upload(fpath,applyNon,applyno_file_path,lose_file=[]): #applyNo 是List
    sql=sql_server("192.168.1.8","sa","ldpjwy","gjgl_xh","1433")
    sql2=sql_server("192.168.1.8","sa","ldpjwy","icbc_api","1433")
    for ia,applyNo in enumerate(applyNon):
        result2=sql2.select(["dbo.icbcapi_assessment"],{"reportId":applyNo},None) #先去上传的查看是否上传过
        result=sql.select(["dbo.bdgl"],{"ybgxmbh":applyNo},['zgjs','zbgh','zl','jzmj','fdc_dj','fczjz','zcs','szc','fwlx','ybgxmbh'])

        mulupdata=[]
        fp=[]

        inset=[]  #insert1 表示要插入 update1表示更新
        if  result:
            insertt=True
            if result2:
                if result['zgjs'] and result['zbgh'] and  result['jzmj'] and result['fdc_dj'] and result['fczjz']   and result['fwlx'] and result['ybgxmbh']:
                    result2["emplName"]=result["zgjs"]
                    mulupdata.append(result2)
                    fp.append(applyno_file_path[ia])
                    inset.append("update1")
                    insertt=False
                else:
                    insertt=False
                    lose_file.append(applyno_file_path[ia])
              
        #del sql
        #del sql2
                if insertt:
                        if result['zgjs'] and result['zbgh'] and  result['jzmj'] and result['fdc_dj'] and result['fczjz']   and result['fwlx'] and result['ybgxmbh'] :
                            updata={}
                            updata["corpId"]="ASS00113"
                            updata["emplName"]=result['zgjs']
                            updata["applyNo"]=result['zbgh']
                            updata['assessAddress']=result['zl']
                            updata['assessArea']=float(result['jzmj'])
                            updata['assessUnitPrice']=int(result['fdc_dj'])
                            updata['assessTotalPrice']=int(result['fczjz'])*10000
                            updata['totalFloor']=int(result['zcs']) if result['zcs']  else 0
                            updata['floor']=int(result['szc']) if result['szc']  else 0
                            updata['orientation']='朝南'
                            updata['houseType']=result['fwlx']
                            updata['schoolHouse']="0"
                            updata['bronzeMedal']="0"
                            updata['assessStatus']="6"
                            updata['assessNo']=result['ybgxmbh']
                            #updata['fileUnifiedNo']=fileuid
                            updata['remarks']=""
                            mulupdata.append(updata)
                            #ups=updata.copy()
                            #ups.pop('emplName')
                            #ups.pop('remarks')
                            #ups['fileUnifiedNo']=fileuid
                            fp.append(applyno_file_path[ia])
                            inset.append("insert1")
                        else:
                            
                            lose_file.append(applyno_file_path[ia])
                else:
                    lose_file.append(applyno_file_path[ia])
        print(mulupdata)
        print(fp)
        print(inset)
        if mulupdata:

            for ii,lsd in enumerate(mulupdata):
          
                muldup(lsd,fp[ii],inset[ii])

           

            
             

    print("---------------完成-------------")


def muldup(updata,fpath,insertup,):
    if 'reportId' in list(updata.keys()):
        updata.pop("reportId")
    
    if 'flag' in list(updata.keys()):
        updata.pop("flag")
    
 
    s=setline()
    chunkr=512
    s.setshappid("shapp.housepledge.xinheng")
    getnameip = str(getip()).split(",")
    s.setip(getnameip[0])
    s.setname(getnameip[1])
    ss = setaes(s)
    fsize=os.path.getsize(fpath)
    chunkcount=math.ceil(fsize/chunkr)
    i=0
    s.seturl("/shlocal/might/magic/encrypt/upload/manual/")
    with open(fpath,'rb') as fr: #读取文件开始上传报告
        upl={}
        upl['corpId']="ASS00113"
        upl['empIName']= updata["emplName"]
        upl['fileName']=fpath[fpath.rfind("\\")+1:]
        upl['chunks']=chunkcount
        while i<chunkcount:
            fr.seek(i*chunkr)
            m=base64.b64encode(fr.read(chunkr))    
            upl['chunk']=i
            upl['fileContent']=m.decode()
            s.setmsg(json.dumps(upl,ensure_ascii=False))
            uuid2=uuid.uuid1()
            r2=ss.dopost(uuid2)
            print(r2)
            if r2[0]=='0' :
                if i==0:
                    updata['fileUnifiedNo']=json.loads(r2[1])['rows'][0]["fileUnifiedNo"]
                    print(updata['fileUnifiedNo'])
                    upl['fileUnifiedNo']=updata['fileUnifiedNo']
                print("正在上传"+fpath+"------"+str(i/chunkcount*100)+"%")
            else:
                print("----上传"+fpath+"失败-----")
                raise Exception
            i=i+1 
   
    
    s.seturl("/shlocal/housepledge/assessplate/save/assessment")#housepledge/assessplate/query/applylist
    
    jsonupd=json.dumps(updata,ensure_ascii=False)
 
    s.setmsg(jsonupd)
   
    uuid1=uuid.uuid1()
    result1=ss.dopost(uuid1)
    print(result1)
    if result1:
        if result1[0]=='0':
            updata['reportId']=updata["assessNo"]
            updata['flag']="1"
            updata['assessStatus']="7"
            sql2=sql_server("192.168.1.8","sa","ldpjwy","icbc_api","1433")
            sql2.updateorinsert("icbcapi_assessment",{"applyNo":updata["applyNo"]},updata,['applyNo'],insertup)
            

                    
        else:
            raise Exception
    
    #except:
        #que.put(updata)
        #que2.put(insertup)


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
   #f=r"E:\applyno"
   #fl=bianli(f,"AID")
   #upload(f,fl)
    applyNo=["AID0000037741"]
    sql2=sql_server("192.168.1.8","sa","ldpjwy","icbc_api","1433")
    result2=sql2.select(["dbo.icbcapi_assessment"],{"applyNo":applyNo},None) #先去上传的查
    print(result2)
    # f="E:\\436.pdf"
    # r=512
    # file_rtow(f,r)
   #getMD5(f)
   

            #print(laresult)
    #exlcelwrite(laresult, "xls//"+time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))+".xls")