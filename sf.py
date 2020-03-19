import requests
from bs4 import *
import random
import re
import xlrd
import xlwt
import time

he={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','content-encoding':'gzip'}
head={'content-type': 'application/x-www-form-urlencoded; charset=UTF-8','user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
re1=r"[\u4e00-\u9fa5]+"
re2=r"(\d{4})年(\d{1,2})月(\d{1,2})日"
re3=r".*([^\d{4}-]\d{2,3}-\d{1,4})+.*"
re4=r".*[\u4e00-\u9fa5](\d{2,3}-\d{1,4})[㎡|平].*"
re5=r".*面(\d{2,4}㎡)+.*"
re6=r"<em>+[^1-9]*(\d{3,8})[\w\W]+</em>"
re7=r"<span+.*>(.*)</span>"
re8=r'href=\"(.*)\/\"'
re9=r'<a.*>(.*)</a>'
re10=r"(\d{4})-(\d{1,2})-(\d{1,2})"

class Soufang(object):
    def __init__(self,loulist):
        self.lou=loulist

    def souf(self):
        resultlist=[]
       
        for lo in self.lou:
            resultlist.append(searchbegin(lo))
        #for resf in resultlist:
        #    print(resf)
        return resultlist

def searchbegin(lo):
    time.sleep(1)
    dd={}
    dd['city']='上海'
    url='https://sh.newhouse.fang.com/house/ajaxrequest/search_keyword_submit.php?t='+rand()
    ls=['','','','','','']
    slo =lo.split(',')
    for i,sslo in enumerate(slo):
        dd['keyword'] = sslo
        result=requests.post(url,data=dd,headers=head)
        print(result.text)
        sp=result.text.split("^")
        if sp[0]=='100':
            url1='https:'+sp[1]+ '?xf_source='+lo
            print(url1)
            result2=requests.get(url1,headers=he)
            ls=readhtml(result2.text.encode('ISO-8859-1').decode('gb18030'))
            return ls
        elif sp[0] =='102':
            d2={}
            d2['type']='urlencode'
            d2['data']=sslo
            d2['city']='上海'
            ress=requests.post("https://sh.newhouse.fang.com/house/ajaxrequest/arealist.php?t="+str(rand()),data=d2,headers=he)
            if len(ress.text)>0:
                ress2=requests.get("https://sh.newhouse.fang.com/house/s/a9"+ress.text+"/?xl_source="+lo)
                html1=ress2.text.encode('ISO-8859-1').decode('gb18030','ignore')
                so2=BeautifulSoup(html1,"html.parser")
                ww3=so2.select('div[class="nl_con clearfix"] > ul >li>div>div>div>div[class="nlcd_name"]')
                so33=so2.select('div[class="house_value clearfix"]>div[class="fl mr10"]')
                print(ww3)
                for ww in ww3:
                    sww33=re.search(re7,str(ww))
                    if sww33:
                        sw=sww33.group(1)
                        print(sw)
                        if sslo.find(sw) >=0 or sw.find(sslo)>=0:
                            swref=re.findall(re8,str(ww))
                            result22=requests.get('https:'+swref[0],headers=he)
                            ls=readhtml(result22.text.encode('ISO-8859-1').decode('gb18030','ignore'))
                            return ls
                    elif re.search(re9,str(ww)):
                        if so33:
                            print(so33[0])
                            if str(so33[0]).find('二手')>=0:
                                ls[0]='二手房'
                                ls[5]=sslo
                                return ls
                        sw=re.search(re9,str(ww)).group(1)
                        print(sw)
                        if sslo.find(sw) >=0 or sw.find(sslo)>=0:
                            swref=re.findall(re8,str(ww))
                            result22=requests.get('https:'+swref[0],headers=he)
                            ls=readhtml(result22.text.encode(result22.encoding,'ignore').decode('gb18030','ignore'))
                            return ls
    return ls


def  readhtml(html1):
    time.sleep(1)
    ls=['','','','','','']
    sw=[]
    tt=True
    soup=BeautifulSoup(html1,"html.parser")
    w33=soup.select('div[id="orginalNaviBox"] >a')
    if w33:
        w3=w33[1]['href']
        w2=soup.select('div[class="fl zlhx"] >a')
        for ww2 in w2:
            stw=ww2.string
            if stw:
                stwre=re.search(re5,stw)
                if stwre:
                    print(stwre.group(1))
                    sw.append(stwre.group(1))
        if sw:
            ls[4]=','.join(sw)
        soo=  soup.select('div[class="tit"]>h1')
        if soo:
            ls[5]=str(soo[0]).replace('<strong>','').replace('</strong>','').replace('</h1>','').replace('<h1>','')
        rs3=requests.get('https:'+w3,headers=he)
      
        html=rs3.text.encode('ISO-8859-1').decode('gb18030','ignore')
        soup=BeautifulSoup(html,"html.parser")
        so1 = soup.select('div[class="main-item"] > div[class="main-info clearfix"] > div[class="main-info-price"] > div[class="pricetd"] ')
        if so1:
            print(so1[0])
            #stf1=re.search(re6,str(so1[0])).group(1)
            stf1=str(so1[0]).replace("<p>","").replace("</p>","").replace("em","").replace("</em>","").replace(r'<div class="pricetd">','').replace("</div>","").replace("<b>","").replace("</b>","").replace("<>","")
            print(stf1)
           
           
            ls[0]=stf1
        so=soup.select('div[class="main-item"] > ul[class="list clearfix"] > li >div')
        for i,soupr in enumerate(so):
            if str(soupr.string).find("装修状况")>-1:
                str1 = so[i+1].string
                str2=''
                res1 = re.findall(re1,str(str1))
                if res1:
                    str2=res1[0]
                ls[2]=str2
                print(str2)
                #replace('	','').replace('		',''))
            elif str(soupr.string).find("开盘时间：")>-1:
                str2=''
                str1= str(so[i+1])
                res1=re.findall(re2,str1)
                if  res1:
                    if len(res1[0])>2:
                        str2=res1[0][0]+"-"+res1[0][1]+"-"+res1[0][2]
                else:
                    res222=re.findall(re10,str1)
                    if res222:
                        str2=res222[0][0]+"-"+res222[0][1]+"-"+res222[0][2]
                ls[1]=str2
                print(str2)
        so=soup.select('div[class="main-item"] > div[class="main-table"] > div[class="table-part"] > table >tr >td')
        for sof in so:
            re41=re.search(re4,str(sof))
            if re41:
                rs4=re41.group(1)
                print(rs4)
                ls[2]=ls[2]+rs4+'㎡'
                ls[3]=str(sof)
                print(rs4+"  "+str(sof))
                tt=False
                break
        if tt:
            if ls[4]!='':
                ls[2]=ls[2]+maopao(ls[4])
                
    return ls

def maopao(lid):
    maolist=lid.replace('㎡','').split(',')
    ml=[]
    print(maolist)
    for mm in maolist:
        if str(mm).isdigit():
            ml.append(int(mm))
        else:
            return ''
    print(ml)
    if len(ml)==1:
        return str(ml[0])+"㎡"
    i=len(ml)-1
    for ia in range(0,i):
        mtf=True
        for ib in range(0,i-ia):
            if ml[ib]>ml[ib+1]:
                temp=ml[ib]
                ml[ib]=ml[ib+1]
                ml[ib+1]=temp
                mtf=False
        if mtf:
            return str(ml[0])+"-"+str(ml[i])+"㎡"
    return str(ml[0])+"-"+str(ml[i])+"㎡"


        

    

def read_excel(filename,sheetname,ncol):
        dataa = []
        book = xlrd.open_workbook(filename)
        sheet = book.sheet_by_name(sheetname) #book.sheet_by_name('sheet1')
        ra = sheet.nrows
        #na= sheet.ncols 
        #for aa in range(0,na):
           # self.lie.append(sheet.cell_value(0,aa))
        for i in range(1,ra):
            v = sheet.cell_value(i,ncol)
            dataa.append(v)
        return dataa

def exlcelwrite(a, filename):
    writebook = xlwt.Workbook() 
    sheet= writebook.add_sheet('test')  
    c=1
    for d in a: #取出data中的每一个元组存到表格的每一行
        for index in range(0,len(d)):   #将每一个元组中的每一个单元存到每一列
            sheet.write(c,index,d[index])
        c += 1
    writebook.save(filename)
            
    
def rand():
    return str(random.randint(1000000000000000,9999999999999999)/10000000000000000)

if __name__ == "__main__":
    t=time.time()
    lists=["恒文星尚湾","昱龙家园"]
    fname=r"E:\S1一手房楼盘典型楼盘(1)(1).xls"
    fname2="E:\\"+str(time.strftime("%H%M%S",time.localtime()))+".xls"
    lists1=read_excel(fname,'19S4',3)
   # print(lists1)
    sf=Soufang(lists1)
    sflist=sf.souf()
    print(sflist)
    exlcelwrite(sflist,fname2)
    print(time.strftime("%H:%M:%S",time.localtime()))
    print(time.time()-t)
    pass
