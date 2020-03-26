from set import setline,setaes
import os
import xlwt
import time
import uuid
import socket
import json
import configparser

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


if __name__=="__main__":
    s =setline()
    s.seturl("/shlocal/housepledge/assessplate/query/applylist")#housepledge/assessplate/query/applylist
    s.setshappid("shapp.housepledge.xinheng")
    tim=time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()))
   # s.setmsg("{\"corpId\":\"ASS00113\",\"emplName\":\"王海琼\",\"settleStatus\":\"1\"}")
    s.setmsg("{\"corpId\":\"ASS00113\",\"emplName\":\"王海琼\",\"startDate\":\""+str(zhuanshijianchuo('2019-09-01 00:00:00'))+"\",\"endDate\":\""+str(zhuanshijianchuo(tim))+"\",\"assessStatus\":\"7\"}")
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
            #print(laresult)
    #exlcelwrite(laresult, "xls//"+time.strftime("%Y%m%d%H%M%S", time.localtime(time.time()))+".xls")