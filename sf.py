import requests
from bs4 import *
import random
import re
import xlrd
import xlwt
from xlutils.copy import copy 
class Soufang(object):
    def __init__(self,loulist):
        self.lou=loulist
        self.re1=r"[\u4e00-\u9fa5]+"
        self.re2=r"(\d{4})年(\d{1,2})月(\d{1,2})日"
        self.re3=r".*([^\d{4}-]\d{2,3}-\d{1,4})+.*"
        self.re4=r".*(\d{2,3}-\d{1,4})+.*"
        self.re5=r".*(\d{2,4}㎡)+.*"
        self.re6=r"([\u4e00-\u9fa5]*\d{3,5}[\u4e00-\u9fa5]*?)"
    def souf(self):
        dd={}
        dd['city']='上海'
        resultlist=[]
        ls=['','','','','','']
        he={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','content-encoding':'gzip'}
        head={'content-type': 'application/x-www-form-urlencoded; charset=UTF-8','user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
        url='https://sh.newhouse.fang.com/house/ajaxrequest/search_keyword_submit.php?t='+rand()
        for lo in self.lou:
            dd['keyword'] = lo
            result=requests.post(url,data=dd,headers=head)
            print(result.text)
            sp=result.text.split("^")
            if sp[0]=='100':
                url1='https:'+sp[1]+ '?xf_source='+lo
                print(url1)
                result2=requests.get(url1,headers=he)
                ls=readhtml(result2.text.encode('ISO-8859-1').decode('gbk'),self.re1,self.re2,self.re3,self.re4,self.re5,self.re6)
                resultlist.append(ls)
                ls=['','','','','','']
            elif sp[0] =='102':
                d2={}
                d2['type']='urlencode'
                d2['data']=lo
                d2['city']='上海'
                ress=requests.post("https://sh.newhouse.fang.com/house/ajaxrequest/arealist.php?t="+str(rand()),data=d2,headers=he)
                if len(ress.text)>0:
                    ress2=requests.get("https://sh.newhouse.fang.com/house/s/a9"+ress.text+"/?xl_source="+lo)
                    html1=ress2.text.encode('ISO-8859-1').decode('gbk')
                    so2=BeautifulSoup(html1,"html.parser")
                    ww3=so2.select('div[class="nl_con clearfix"] > ul >li>div>div>div>div[class="nlcd_name"]')
                    print(ww3)
                    for ww in ww3:
                        print(ww.string)
        print(resultlist)

def  readhtml(html1,re1,re2,re3,re4,re5,re6):
    ls=['','','','','','']
    sw=[]
    he={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','content-encoding':'gzip'}
    soup=BeautifulSoup(html1,"html.parser")
    w3=soup.select('div[id="orginalNaviBox"] >a')[1]['href']
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
    print(rs3.encoding)
    html=rs3.text.encode('ISO-8859-1').decode('gbk')
    soup=BeautifulSoup(html,"html.parser")
    so1 = soup.select('div[class="main-info-price"] > em')
    if so1:
        print(str(so1[0]))
        stf1=re.search(re6,str(so1[0])).groups()
        print(stf1)
        stf=stf1[len(stf1)-1]
        print(stf)
        if stf.find("约")>=0:
            stf=stf[stf.find("约")+1:len(stf)].replace('元/平方米','')
        ls[0]=stf.replace(' ','')
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
            ls[1]=str2
            print(str2)
    so=soup.select('div[class="main-item"] > div[class="main-table"] > div[class="table-part"] > table >tr >td')
    for sof in so:
        res3=re.search(re3, str(sof))
        if res3:
            ree=res3.group(1)
            print(ree)
            re4=re.search(re4,str(ree))
            if re4:
                rs4=re4.group(1)
                ls[2]=ls[2]+rs4+'㎡'
                ls[3]=str(sof)
                print(rs4+"  "+str(sof))
                break
    return ls
                    
def read_excel(self,filename,sheetname,ncol):
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

def exlcelwrite(a, filename,sheetname):
    book1 = xlrd.open_workbook(filename)            #创建excel对象
    book  =copy(book1)
    sheet = book.sheet_by_name(sheetname)  #添加一个表
    na= sheet.ncols 
    c=1
    for d in a: #取出data中的每一个元组存到表格的每一行
        for index in range(na,len(d)+na):   #将每一个元组中的每一个单元存到每一列
            sheet.write(c,index,d[index])
        c += 1
    book.save(filename)
            


    
def rand():
    return str(random.randint(1000000000000000,9999999999999999)/10000000000000000)

if __name__ == "__main__":
    lists=["招商虹桥公馆","大华公园城市"]
    sf=Soufang(lists)
    sf.souf()
    pass
