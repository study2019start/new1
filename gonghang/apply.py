import uuid
import socket
import time,datetime
from Crypto.Cipher  import AES
import base64
import random
from os import urandom
from hashlib import sha1
import requests
import urllib 
import re
import json
from set import setline,setaes

class app(object):
    def __init__(self):
        self.sit=setline()
        self.sit.setkey("48400552514989144C739E3221728BB9E6F346A3AC37E6DC7DBD668D6FB6BAB3")
        self.sit.setshappid("shapp.housepledge.xinheng")
        getnameip = str(getip()).split(",")
        self.sit.setname(getnameip[1])
        self.sit.setip(getnameip[0])

    def applylist(self,idq,name,tim1,tim2,status):
        self.sit.seturl("/shlocal/housepledge/assessplate/query/applylist")
        m="{\"corpId\":\""+str(idq)+"\",\"emplName\":\""+str(name)+"\",\"startDate\":\""+str(tim1)+"\",\"endDate\":\""+str(tim2)+"\",\"assessStatus\":\""+str(status)+"\"}"
        
        self.sit.setmsg(m)
        ss=setaes(self.sit)
        uuid1=uuid.uuid1()
        ls=ss.dopost(uuid1)
        
        if int(ls[0])==0:
            msg=json.loads(ls[1])
            
            print(msg['total'])
            for item in msg['rows']:
                at=int(int(item["applyTime"])/1000)
                tat=time.strftime("%Y-%m-%d",time.localtime(at))
                item["applyTime"]=tat
                for k,t in item.items():
                    print(str(k)+":"+str(t))
                print("-----------------")
    




def getip():
    myname=socket.getfqdn(socket.gethostname())
    myaddr=socket.gethostbyname(myname)
    return myaddr+","+myname

def zhuanshijianchuo(time1):
    return int(time.mktime(time.strptime(time1,"%Y-%m-%d %H:%M:%S")))*1000

if __name__=="__main__":
    ap=app()
    idq="ASS00113"
    ap.applylist(idq,"赵晓芸",zhuanshijianchuo("2019-01-01 00:00:00"),int(time.time()*1000),"6")
