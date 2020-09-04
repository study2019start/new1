import requests
from bs4 import BeautifulSoup
import random
import re
import xlrd
import xlwt
import time
from multiprocessing import Process,Queue,Lock,Pool,Manager
import xlwings as xlw
import pandas as pd
import os
from excel import model_excel
 
he={'user-agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36','content-encoding':'gzip'}
head={'content-type': 'application/x-www-form-urlencoded; charset=UTF-8','user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'}
re1=r"[\u4e00-\u9fa5]+"
re2=r"(\d{4})年(\d{1,2})月(\d{1,2})日"
re3=r".*([^\d{4}-]\d{2,3}-\d{1,4})+.*"
re4=r".*[\u4e00-\u9fa5](\d{2,3}-\d{1,4})[㎡|平].*"
re5=r".*面(\d{2,4}㎡)+.*"
re6=r"<em>+[^1-9]*(\d{3,8})[\w\W]+</em>"
re7=r"<span+.*>(.*)</span>"
re8=r'href=\"(.*\.fang\.com|.*\.fang\.com\/\d{1,5})\/\"'
re9=r'<a.*>(.*)</a>'
re10=r"(\d{4})-(\d{1,2})-(\d{1,2})"
re11=r'>(\w\W)<'
re12=r'.*([\u4e00-\u9fa5]\d+\.*\d*.*[\u4e00-\u9fa5]*\/*[\u4e00-\u9fa5]*).*'

class firstsou(object):
    def __init__(self,path,ncol,shname):
        self.fp=path
        self.nc=ncol
        self.sheetname=shname

    def run(self):
        lists1=read_excel(self.fp,self.sheetname,self.nc)
        sflist=[]
        mul=Pool(6)
        qq=Manager().Queue()
        for lsd in lists1:
            mul.apply_async(runss,(lsd,qq))
        mul.close()
        mul.join()
        while not qq.empty():
            sflist.append(qq.get())
        sflist.sort(key=lambda x: x[6])
        
        xlww=model_excel()
        df=pd.DataFrame(sflist,columns=['售价','开盘时间','主力面积','信息','信息2','名称','序号'])
        
        xlww.xlwingwirte(df,self.fp,self.sheetname,True)


def runss(lo,qp): 
    
    tss=searchbegin(lo)
    Lock().acquire()
    print(tss)
    qp.put(tss)
    Lock().release()
        #for resf in resultlist:
        #    print(resf)
        

def searchbegin(lo):
     
    dd={}
    dd['city']='上海'
    url='https://sh.newhouse.fang.com/house/ajaxrequest/search_keyword_submit.php?t='+rand()
    ls=['','','','','','',-1]
    slo=[]
    ls[6] = lo[1]
    if str(lo[0]).find(",") > 0:
        slo = [x for x in lo[0].split(',')]
    else:
        slo.append(lo[0])
    for sslo in slo:
        dd['keyword'] = sslo
        result=requests.post(url,data=dd,headers=head)
        
        sp=result.text.split("^")
        if sp[0]=='100':
            url1='https:'+sp[1]+ '?xf_source='+sslo
            
            result2=requests.get(url1,headers=he)
            ls=readhtml(result2.text.encode('ISO-8859-1').decode('gb18030'))
            ls.append(lo[1])
            return ls
        else:
            d2={}
            d2['type']='urlencode'
            d2['data']=sslo
            d2['city']='上海'
            ress=requests.post("https://sh.newhouse.fang.com/house/ajaxrequest/arealist.php?t="+str(rand()),data=d2,headers=he)
            if len(ress.text)>0:
                ress2=requests.get("https://sh.newhouse.fang.com/house/s/a9"+ress.text+"/?xl_source="+sslo)
                html1=ress2.text.encode('ISO-8859-1').decode('gb18030','ignore')
                so2=BeautifulSoup(html1,"html.parser")
                ww3=so2.select('div[class="nl_con clearfix"] > ul >li>div>div>div>div[class="nlcd_name"]')
                so33=so2.select('div[class="house_value clearfix"]>div[class="fl mr10"]')
                for ww in ww3:
                    sw=str(ww)
                    #if sslo.find(sw) >=0 or sw.find(sslo)>=0:
                    swref=re.findall(re8,sw)
                    if swref:
                        if swref[0].find("http")>-1:
                            ts=swref[0]
                        else:
                            ts="https:"+swref[0]
                        result22=requests.get(ts,headers=he)
                        ls=readhtml(result22.text.encode('ISO-8859-1').decode('gb18030','ignore'))
                        ls.append(lo[1])
                        return ls 
                    elif re.search(re9,str(ww)):
                        if so33:
                            if str(so33[0]).find('二手')>=0:
                                ls[0]='二手房'
                                ls[5]=sslo
                                return ls
                        sw=re.search(re9,str(ww)).group(1)
                        if sslo.find(sw) >=0 or sw.find(sslo)>=0:
                            swref=re.findall(re8,str(ww))
                            if swref:
                                if swref[0].find("http")>-1:
                                    ts=swref[0]
                                else:
                                    ts="https:"+swref[0]
                                
                                result22 = requests.get(ts,headers=he)
                                ls=readhtml(result22.text.encode(result22.encoding,'ignore').decode('gb18030','ignore'))
                                ls.append(lo[1])
                                return ls
    return ls


def  readhtml(html1):
    
    ls=['','','','','','']
    sw=[]
    tt=True
    soup=BeautifulSoup(html1,"html.parser")
    ifers=soup.select('div[class="laybox clearfix"] > div[class="bread"] ')
    if ifers:
        if str(ifers[0]).find("二手")>0:
            ls[0]='二手'
            return ls
    w33=soup.select('div[id="orginalNaviBox"] >a')
    if w33:
        w3=w33[1]['href']
        w2=soup.select('div[class="fl zlhx"] >a')
        for ww2 in w2:
            stw=ww2.string
            if stw:
                stwre=re.search(re5,stw)
                if stwre:
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
            #stf1=re.search(re6,str(so1[0])).group(1)
            
            res=re.search(re12,str(so1[0]))
            if res:
                ls[0]=res.group(1)
            else:
                stf1=str(so1[0]).replace("<p>","").replace("</p>","").replace("em","").replace("</em>","").replace(r'<div class="pricetd">','').replace("</div>","").replace("<b>","").replace("</b>","").replace("<>","").replace(r"</>","").replace("\r\n","").replace(r"\n","")
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
               
                #replace('	','').replace('		',''))
            elif str(soupr.string).find("开盘时间：")>-1:
                str2=''
                str1= str(so[i+1])
                if str1.find('预计') >-1 and  str1.find("加推")==-1:
                    str2=str1
                else:
                    res1=re.findall(re2,str1)
                    if  res1:
                        if len(res1[0])>2:
                            if str1.find("加推")>-1:
                                str2=res1[0][0]+"-"+res1[0][1]+"-"+res1[0][2]+"加推"
                            else:
                                str2=res1[0][0]+"-"+res1[0][1]+"-"+res1[0][2]
                    else:
                        res222=re.findall(re10,str1)
                        if res222:
                            if str1.find("加推")>-1:
                                str2=res222[0][0]+"-"+res222[0][1]+"-"+res222[0][2]+"加推"
                            else:
                                str2=res222[0][0]+"-"+res222[0][1]+"-"+res222[0][2]
                        elif str1.find("加推")>-1:
                            str2=str1
                ls[1]=str2
        so=soup.select('div[class="main-item"] > div[class="main-table"] > div[class="table-part"] > table >tr >td')
        for sof in so:
            re41=re.search(re4,str(sof))
            if re41:
                rs4=re41.group(1)
              
                ls[2]=ls[2]+rs4+'㎡'
                ls[3]=str(sof)
            
                tt=False
                break
        if tt:
            if ls[4]!='':
                ls[2]=ls[2]+gb(ls[4])
                
    return ls

def maopao(lid):
    maolist=lid.replace('㎡','').split(',')
    ml=[]
  
    for mm in maolist:
        if str(mm).isdigit():
            ml.append(int(mm))
        else:
            return ''
 
    if len(ml)==1:
        return str(ml[0])+"㎡"
    i=len(ml)-1
    ml.sort()
    return str(ml[0])+"-"+str(ml[i])+"㎡"

def gb(lid):
    maolist=lid.replace('㎡','').split(',')
    ml=[]
 
    for mm in maolist:
        if str(mm).isdigit():
            ml.append(int(mm))
    if len(ml)==1:
        return str(ml[0])+"㎡"
    elif len(ml) ==0:
        return ''
    i=len(ml)-1
    ml.sort()
    # for ia in range(0,i):
    #     mtf=True
    #     for ib in range(0,i-ia):
    #         if ml[ib]>ml[ib+1]:
    #             temp=ml[ib]
    #             ml[ib]=ml[ib+1]
    #             ml[ib+1]=temp
    #             mtf=False
    #     if mtf:
    #         return str(ml[0])+"-"+str(ml[i])+"㎡"
    return str(ml[0])+"-"+str(ml[i])+"㎡"
        

    

def read_excel(filename,sheetname,ncol):
        dataa = []
        book = xlrd.open_workbook(filename)
        sheet = book.sheet_by_name(sheetname) #book.sheet_by_name('sheet1')
        ra = sheet.nrows
        print(ra)
        #na= sheet.ncols 
        #for aa in range(0,na):
           # self.lie.append(sheet.cell_value(0,aa))
        for i in range(1,ra):
            s=[]
            v = sheet.cell_value(i,ncol)
            s.append(v)
            s.append(i) #序号
            dataa.append(s)
        return dataa

def exlcelwrite(a, filename):
    writebook = xlwt.Workbook() 
    sheet= writebook.add_sheet('test')  
    c=0
    for d in a: #取出data中的每一个元组存到表格的每一行
        for index in range(0,len(d)):   #将每一个元组中的每一个单元存到每一列
            sheet.write(c,index,d[index])
        c += 1
    writebook.save(filename)


def xlwingwirte(a,filename,sheetname,rangestart='H2'):
    df=pd.DataFrame(a,columns=['售价','开盘时间','主力面积','信息','信息2','名称','序号'])
    #print(df)
    findd=filename.rfind('.')
    findd1=filename.rfind('\\')
    st1=filename[findd:len(filename)] #后缀名
    st2=filename[findd1:findd] #文件名
    st3=filename[0:findd1] #文件所在目录
    newfn=st2+str(time.strftime("%H%M%S",time.localtime()))+st1  #文件名加入时间
    svpath=os.path.join(st3,newfn)
    os.system("copy "+filename+"  " +svpath)
    app=xlw.App(visible=True,add_book=False)    
    wb=app.books.open(svpath,update_links=False)
    sh=wb.sheets[sheetname]
    sh.range(rangestart).value=df.values
    wb.save()
    wb.close()
    app.quit()


def rand():
    return str(random.randint(1000000000000000,9999999999999999)/10000000000000000)

if __name__ == "__main__":
    t=time.time()
    #print(time.strftime("%H:%M:%S",time.localtime()))
    #lists=["恒文星尚湾","昱龙家园"]
    fname=r"E:\二季度一手楼盘.xlsx"
    #fname2="E:\\"+str(time.strftime("%H%M%S",time.localtime()))+".xls"
    lists1=read_excel(fname,'Sheet1',3)
    #lists1=[["禹洲雍锦府",1]]
   # print(lists1)
    longlis=[]
    mul=Pool(6)
    qq=Manager().Queue()
    for lsd in lists1:
        mul.apply_async(runss,(lsd,qq))

    mul.close()
    mul.join()
        
   
    sflist=[]
    while not qq.empty():
        sflist.append(qq.get())
    #print(sflist)
    sflist.sort(key=lambda x: x[6])
    xlww=model_excel()
    df=pd.DataFrame(sflist,columns=['售价','开盘时间','主力面积','信息','信息2','名称','序号'])
     
    xlww.xlwingwirte(df,fname,'Sheet1',True)
    #exlcelwrite(sflist,fname2)
    #print(time.strftime("%H:%M:%S",time.localtime()))
    print(time.time()-t)