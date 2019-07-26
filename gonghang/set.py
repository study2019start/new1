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


class setline(object):
    def __init__(self):
        self.__baseurl="http://corp.sh.icbc.com.cn/shapi"
        self.__key=""
        self.__shappid=""
        self.__url=""
        self.__msg=""
        self.__ip=""
        self.__name=""
    def setkey(self,k):
        self.__key=k
    def setip(self,ip):
        self.__ip=ip
    def setname(self,name):
        self.__name=name
    def seturl(self,u):
        self.__url=u
    def setmsg(self,m):
        self.__msg=m
    def setshappid(self,shappid):
        self.__shappid=shappid
    def getkey(self):
        return self.__key
    def geturl(self):
        return self.__url
    def getshappid(self):
        return self.__shappid
    def getbaseurl(self):
        return self.__baseurl
    def getmsg(self):
        return self.__msg
    def getip(self):
        return self.__ip
    def getname(self):
        return self.__name
    def baseurl(self):
        return self.__baseurl        

class setaes():
    def __init__(self,setl):
        self.s=setl


    def dopost(self,uuid):
        head= "<?xml version=\"1.0\" encoding=\"UTF-8\"?><HEADER><SHAPPID>%s</SHAPPID>" %self.s.getshappid() + "<ICBCHQAPPID>%s</ICBCHQAPPID>" %"0"+ "<REQUESTURI>%s</REQUESTURI>" %self.s.geturl()+ "<CLIENTIP>%s</CLIENTIP>" %self.s.getip()+ "<CLIENTHOSTNAME>%s</CLIENTHOSTNAME>" %self.s.getname()+ "<CLIENTUUID>%s</CLIENTUUID>"  %uuid+ "<PREV_UUID>%s</PREV_UUID>"  %""+ "<CLIENTTIMESTAMP>%s</CLIENTTIMESTAMP>"  %gettime()+ "<RETURNCODE>-1</RETURNCODE><RETURNMSG>UNKNOW</RETURNMSG></HEADER>"
        iv = "1111111111111111"
       
        key11= to16(self.s.getkey())

        read = setaes.aes1encode(key11,head,iv)
        read2 = setaes.aes1encode(key11,self.s.getmsg(),iv)
        enhead=read.decode()
        encmsg = read2.decode()
        digest = sha(self.s.getmsg())
        readyxml = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"+"<Trade><PUBLIC><SHAPPID>"+str(self.s.getshappid())+"</SHAPPID>" + "<REQUEST_ID>"+str(uuid)+"</REQUEST_ID>"  + "<PREV_UUID></PREV_UUID></PUBLIC>" + "<SHAPI><HEADER>"+str(enhead)+"</HEADER><REQUEST>"+str(encmsg)+"</REQUEST>" + "<RESPONSE></RESPONSE><DIGEST>"+str(digest)+"</DIGEST></SHAPI></Trade>" 

        cospurl = self.s.getbaseurl()+self.s.geturl()
        way="SHAPI"
        version="00001"
        
        return enhead

    @classmethod
    def aes1encode(cls,key,something,IV):
        index = urandom(7)
        index2= urandom(14)
        s=b""
        ss=b""
        for iii in index:
            s=s+base64.b64encode(int.to_bytes(iii,1,byteorder='big'))
      
        for ii in index2:
            ss=ss+base64.b64encode(int.to_bytes(ii,1,byteorder='big'))
        s1=str(s.decode()).replace("=","")[0:7]
        s2=str(ss.decode()).replace("=","")[0:14]
        something=s1+something+s2
        cryp = AES.new(key,AES.MODE_CBC,IV.encode("utf8"))
        bs=len(key) 
        pad = lambda s: s + ((bs - len(s) % bs) * chr(bs - len(s) % bs)).encode('utf-8')
        so=something.encode("utf8")
        chiphertext = cryp.encrypt(pad(so))
        return base64.b64encode(chiphertext)



def docospPost(appcde,trxcode,msg,cospurl):
    headers = {
    "Content-Type":"application/x-www-form-urlencoded"
}
    sb="cosp="+urllib.parse.quote(msg, safe='/', encoding="utf-8", errors=None)+"&appcode="+str(appcde)+"&trxcode="+str(trxcode)
    r = requests.post(cospurl,data=sb.encode(),headers=headers)
    return r
def baidu():
    r=requests.get("http://baidu.com")
    return r


def decrypt1(key, text,IV):
        decode = base64.b64decode(text)
        cryptor = AES.new(key, AES.MODE_CBC, IV.encode("utf8"))
        plain_text = cryptor.decrypt(decode)
        unpad = lambda s: s[0:-ord(s[-1:])]
        return unpad(plain_text)


def sha(str2):
    s1=sha1()
    s1.update(str2.encode())
    return s1.hexdigest()

def to16(str2):
    lis=list(str2)
    i=0
    count=len(lis)/2
    result=b''
    while i < count:
        intt=int(lis[i*2]+lis[i*2+1],16)
        ss=int.to_bytes(intt,1,byteorder='big')  
        result += ss
        i = i+1
    
    return result


def getip():
    myname=socket.getfqdn(socket.gethostname())
    myaddr=socket.gethostbyname(myname)
    return myaddr+","+myname
def gettime():
    st = time.strftime("%Y%m%d-%H%M%S", time.localtime())
    time2 = str(time.time())
    ti =  "".join([time2[time2.find(".")+x]  for x in range(1,4)])
    return str(st)+"-"+str(ti)

if __name__=="__main__":
    s =setline()
    s.setkey("48400552514989144C739E3221728BB9E6F346A3Ac37E6DC7DBD668D6FB6BAB3")
    s.seturl("shlocal/housepledge/commplate/qurey/dict")
    s.setshappid("shapp.housepledge.xinheng")
    s.setmsg("{\"corpId\":\"ASS00113\",\"emplName\":\"王海琼\"}")
    getnameip = str(getip()).split(",")
    s.setip(getnameip[0])
    s.setname(getnameip[1])
    ss = setaes(s)
