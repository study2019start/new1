from mysqlconn import xiaoqu_mysql_lou
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import WebDriverException 
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from access import access_model
import configparser
import xlrd
import xlwings as xlw
import pandas as pd
import re
import os

re1=r"[\u4e00-\u9fa5]+(\d{4})[\u4e00-\u9fa5]*"

class base(object):
    def __init__(self,ur):
        self.url=ur



    def insert_access(self,nno,listno,tablename,dbname):
        self.logindd(nno)
        exit_model=access_model(dbname)
        resultln=self.tudisearch(listno)
        wheres=[]
        if resultln:
            for rsl in resultln:
                d={}
                d['dizhi']=rsl['dizhi']
                wheres.append(d)
            exit_model.inserttusql(resultln,tablename,wheres)
               


    def logindd(self,no):
        chrome_options = Options()
        __browser_url = r'C:\Users\thl\AppData\Local\Google\Chrome\Application\chrome.exe'
        chrome_options.binary_location = __browser_url
        chrome_options.add_argument('disable-infobars')
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
        driver = webdriver.Chrome(options = chrome_options)
        driver.maximize_window()
        driver.get(self.url)

        key=no

        self.get_elems(driver,('xpath','//input[@class=\'el-input__inner\']'),0).send_keys(key)#s收入账号
        if self.get_elem(driver,('xpath','//div[@id=\'tab-newhouse\']'),60):#等待60秒完成短信验证
            self.dr= driver
           
           
            return True
        else:
            return False

        

    def tudisearch(self,listno): #列表[开始时间，结束时间，交易状态，类型]
        first=self.get_elem(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li[3]') )#一级市场
        #second=self.get_elem(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li[4]') )#二级市场
        count=16
        listap=[]#存放数据
        sdd=False
        if first:
            ActionChains(self.dr).click(first).perform()
            tudi=self.visibilityy(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li/ul/li/span[text()=\'土地\']'))#土地项目点击进入

            if tudi:
                #print(tudi.location)
                ActionChains(self.dr).click(tudi).perform()
                while True:
                    if self.visibilityy(self.dr,('xpath','//input[@placeholder=\'开始日期\']')):
                        break
                    else:
                        tudi.click()
                #进入查询条件的form
                form1=self.get_elem(self.dr,("xpath","//form[@class=\'el-form res-table-search  el-form--label-right el-form--inline\']"))
                if form1:
                    #填入开始日期
                    self.get_eleminxpath(form1,".//input[@placeholder=\'开始日期\']").send_keys(listno[0])
                    self.get_eleminxpath(form1,".//input[@placeholder=\'结束日期\']").send_keys(listno[1])
                    #在溢价率点击 消除日期弹窗
                    yjl=self.get_elemsinxpath(form1,".//input[@class=\'el-input__inner\']")[15]
                    ActionChains(self.dr).click(yjl).perform()
                    #根据classsname 去除只读属性
                    #js="var s =document.getElementsByClassName(\"el-input__inner\");  for(i=0;i<s.length;i++){s[i].removeAttribute(\"readonly\")};"
                    #self.dr.execute_script(js)

                    #点击土地状态
                    while True:

                        self.get_elemsinxpath(form1,".//input[@class=\'el-input__inner\']")[2].click()
                        #time.sleep(1)
                        cj=self.visibilityy(self.dr,('xpath','//ul[@class=\'el-scrollbar__view el-select-dropdown__list\']/li/span[text()=\'成交\']')) #选择成交
                        ActionChains(self.dr).click(cj).perform()
                        d1=self.get_elems(self.dr,("xpath",'//div[@class=\'el-select res-search-input el-select--small\']'),0)
                        d2= self.get_elemsinxpath(d1,'.//span/span/span')
                        if d2:
                            for dd in d2:
                                if str(dd.text)==listno[2]:
                                    sdd=True
                        if sdd:
                            break
                    ActionChains(self.dr).click(yjl).perform()

                    

                    #点击规划用途
                    self.get_elemsinxpath(form1,".//input[@class=\'el-input__inner\']")[20].click()
                    time.sleep(1)
                    gui=self.visibilityy(self.dr,('xpath',"//ul[@class=\'el-scrollbar__view el-select-dropdown__list\']/li/span[text()=\'"+listno[3]+"\']"))
                    gui.click()
                    ActionChains(self.dr).click(yjl).perform() 
                    #查询按钮
                    self.get_elem(self.dr,("xpath","//button[@class=\'el-button el-button--primary el-button--small\']")).click()
                    time.sleep(1)
                    #if self.visibilityy(self.dr,('xpath',''))
                    #判断是否数据列表出现
                    while True:
                        if not self.visibilityy(self.dr,('class name','el-loading-mask'),3):
                            break
                    if not self.visibilityy(self.dr,('xpath','//div[@class=\'el-table__empty-block\']')):
                        loucjth=self.get_elem(self.dr,("xpath","//table[@class=\'el-table__header\']/thead/tr/th[13]"))
                        loucj=self.get_eleminxpath(loucjth,".//div")
                        #点击第一次成交楼板价 按成交楼板价降序排列
                        loucj.click()
                        #判断数据列表是否出现 出现再点击成交楼板价

                        while True:
                            if self.visibilityy(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr[1]'),5):
                                break

                        #点击第二次成交楼板价
                        
                        while True:
                            loucjth2=self.get_elem(self.dr,("xpath","//table[@class=\'el-table__header\']/thead/tr/th[13]"))
                            if self.tobeclick(loucjth2,('xpath',".//div")):
                            #self.dr.execute_script("arguments[0].click();", loucj2)
                                self.dr.execute_script("var cj=document.getElementsByClassName(\"cell\");cj[12].click();")
                                break
                        while True:
                            if self.visibilityy(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr[1]'),5):
                                break
                        for mlk in range(1,3):
                            listss=self.get_elemsa(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr'),15)
                            lop=0
                            if listss:  #遍历数据列表的tr
                                print(len(listss))
                                for tr in listss:
                                    #获取详情按钮 并点击
                                    #time.sleep(1)
                                    if lop==0:
                                        while True:
                                            if not self.visibilityy(self.dr,('class name','el-loading-mask'),3):
                                                break
                                    tdlist=self.get_elemsinxpath(tr,".//td/div") 
                                    if tdlist:
                                        tplist=tdlist[count]#第17个div
                                        
                                        buttonn=self.get_eleminxpath(tplist,'.//button')
                                        
                                        if buttonn:
                                            #self.dr.execute_script("arguments[0].scrollIntoView();", buttonn) # 滚动条到对应位置
                                            buttonn.click()  #点开详细页
                                            el_dialog=self.get_elem(self.dr,("class name","el-dialog"))
                                            if el_dialog:
                                                dicr={}
                                                if listno[3]== '工业':
                                                    dicr['wu']="五通一平"
                                                else:
                                                    dicr['wu']="七通一平"
                                                #记录内容的列
                                                zilist=self.get_elemsinxpath(el_dialog,".//table[@class=\'market-detail-table\']/tr/td")
                                                dicr['dizhi']=self.get_eleminxpath(zilist[4],'.//span').text
                                                dicr['sizhi']=self.get_eleminxpath(zilist[5],'.//span').text
                                                dicr['leix']=self.get_eleminxpath(zilist[6],'.//span').text
                                                dicr['rj']=str(self.get_eleminxpath(zilist[10],'.//span').text).replace('%','')
                                                dicr['ctime']=self.get_eleminxpath(zilist[20],'.//span').text
                                                dicr['dijia']=str(self.get_eleminxpath(zilist[17],'.//span').text).replace('(元/m²)','')
                                                #把字典数据放入listap列表
                                                if dicr['dizhi']!='' and dicr['sizhi']!='' and dicr['leix']!='' and  dicr['rj']!='' and dicr['ctime']!='' and dicr['dijia']!='':
                                                    dicr['lx']=dicr['leix']
                                                    listap.append(dicr)
                                                time.sleep(2)
                                                #关闭弹出框
                                                self.dr.execute_script("var i= document.getElementsByClassName(\"icon-close icon-location\"); i[0].click();")
                                                time.sleep(1)
                                        lop=lop+1
                                    else:
                                        break
                                    
                                
                            pagenext=self.get_elem(self.dr,('xpath',"//ul[@class=\'el-pager\']/li[text()=\'"+str(mlk+1) +"\']"),3)  #点击后页
                            if pagenext:
                                jss=" var f=document.getElementsByClassName('number'); for(var i=0;i<f.length;i++){ if(f[i].innerHTML=='"+str(mlk+1)+"'){f[i].click();} }"
                                self.dr.execute_script(jss)
                                #pagenext.click()
                            else:
                                break

        print(listap)
        return listap
        



    def firstfang(self,lists): 
        resslutlist=[]
        now=datetime.datetime.now().strftime("%Y-%m-%d")
        year=datetime.datetime.now().year-1
        fyear= datetime.datetime.strftime(datetime.datetime.now()+datetime.timedelta(days=-365),"%Y-%m-%d")
        chonglai=0
        #first=self.get_elem(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li[3]') )#一级市场
        second=self.get_elem(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li[4]') )#二级市场
        if second:
            
            ActionChains(self.dr).click(second).perform()
            while True:
                if not self.visibilityy(self.dr,('class name','el-loading-mask'),3):
                    break
            xin=self.visibilityy(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li/ul/li/span[text()=\'新房成交\']'))#新房点击进入
            if xin:
                #print(tudi.loaction)
                longs=len(lists)
                lix=0
                while lix < longs:

                    sff=True
                    s=[-1,-1,-1]
                    ActionChains(self.dr).click(xin).perform()
                    while True:
                        if self.visibilityy(self.dr,('xpath','//input[@placeholder=\'开始日期\']')):
                            break
                        else:
                            xin.click()
                    tt=time.time()
                    stfft=False
                    while True:
                        if time.time()-tt >40:
                            lix=lix-1
                            break
                        if not self.visibilityy(self.dr,('class name','el-loading-mask'),3):
                            stfft=True
                            break
                    #进入查询条件的form
                    #print(xin.location)
                    if stfft:
                        form1=self.get_elem(self.dr,("xpath","//form[@class=\'el-form res-table-search  el-form--label-right el-form--inline\']"))
                        if form1:
                            #填入开始日期
                            start=self.get_eleminxpath(form1,".//input[@placeholder=\'开始日期\']")
                            start.clear()
                            start.send_keys(fyear)
                            enddate=self.get_eleminxpath(form1,".//input[@placeholder=\'结束日期\']")
                            enddate.clear()
                            enddate.send_keys(now)
                            #在溢价率点击 消除日期弹窗
                            yjl=self.get_elemsinxpath(form1,".//input[@class=\'el-input__inner\']")[15]
                            ActionChains(self.dr).click(yjl).perform()
                            #根据classsname 去除只读属性
                            #js="var s =document.getElementsByClassName(\"el-input__inner\");  for(i=0;i<s.length;i++){s[i].removeAttribute(\"readonly\")};"
                            #self.dr.execute_script(js)
                            #点击土地状态
                            loup=self.get_eleminxpath(form1,".//input[@placeholder=\'请输入搜索内容\']") 
                            ActionChains(self.dr).click(loup).perform()  #鼠标点击搜索框

                            ActionChains(self.dr).send_keys(lists[lix][0]).perform() #模拟输入
    
                            time.sleep(2)
                            kuang=self.get_elem(self.dr,("xpath","//div[@class=\'el-popover el-popper popversearch-cot popversearch-xinz\']/div/div[@class=\'el-table__body-wrapper is-scrolling-none\']"))
                            while True:
                                kuang=self.visibilityy(self.dr,("xpath","//div[@class=\'el-popover el-popper popversearch-cot popversearch-xinz\']/div/div[@class=\'el-table__body-wrapper is-scrolling-none\']"))
                                if kuang:
                                    break
                            if str(kuang.text).find("暂无数据")>0:
                                resslutlist.append(s)
                                print(lists[lix][0]) 
                                lix=lix-1
                            else:
                                tempz=[]
                                trueindex=-1
                                tdli=self.get_eleminsxpath(kuang,'.//tr/td/div')
                                print(len(tdli))
                                lens=int(len(tdli)/4)
                                for iid in range(0,lens):
                                    tempi=iid*4+2
                                    nameiid=str(tdli[tempi].text)
                                    areaname=str(tdli[tempi-2].text)
                                    if areaname.find(lists[lix][2]) < 0 or ((nameiid.find('商业') > 0 or nameiid.find('办公') > 0 ) and nameiid.find(lists[lix][0])<0 ):
                                        pass
                                    elif nameiid.find(lists[lix][0]) >=0:
                                        trueindex = tempi
                                        print(nameiid)
                                        break
                                    else:
                                        tempz.append(tempi)
                                if trueindex==-1 and len(tempz)>0:
                                    for nam in tempz:
                                        name=str(tdli[nam].text)
                                        result=re.findall(re1,name)
                                        if result :
                                            if int(result[0]) < year :
                                                break
                                            else:
                                                trueindex=nam
                                                break
                                if trueindex > -1:
                                    tdli[trueindex].click()
                                    time.sleep(1)  
                                    self.get_elem(self.dr,('xpath','//span[@class=\'el-tag res-zhuzai el-tag--small\']')).click()
                                    #查询按钮
                                    self.get_elem(self.dr,("xpath","//button[@class=\'el-button el-button--primary el-button--small\']")).click()
                                     
                                    #if self.visibilityy(self.dr,('xpath',''))
                                    #判断是否数据列表出现
                                    timesc=time.time() #计时用 超过40秒重新查一次
                                    while True:
                                        if not self.visibilityy(self.dr,('class name','el-loading-mask'),2):
                                            break
                                        time1=time.time()
                                        if time1-timesc > 40:
                                            lix=lix-1
                                            sff=False
                                            break
                                    if sff:
                                        if not self.visibilityy(self.dr,('xpath','//div[@class=\'el-table__empty-block\']'),3):
                                            loucjth=self.get_elem(self.dr,("xpath","//table[@class=\'el-table__header\']/thead/tr/th[6]"))
                                            loucj=self.get_eleminxpath(loucjth,".//div")
                                            #点击第一次成交楼板价 按成交楼板价降序排列
                                            loucj.click()
                                            timesc=time.time()
                                            #判断数据列表是否出现 出现再点击成交楼板价
                                            while True:
                                                time1=time.time()         #计时判断
                                                if self.visibilityy(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr[1]'),15):
                                                    break
                                                if time1 -timesc>30:
                                                    sff=False
                                                    lix=lix-1
                                                    break
                                            if sff:
                                                tablebody=self.get_elemsa(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr'))
                                                pagetotal=self.get_elem(self.dr,('xpath','//span[@class=\'el-pagination__total\']'))
                                                inpagetotl=int(str(pagetotal.text).replace('共 ','').replace(' 条',''))
                                                print(inpagetotl)
                                                data1lit=[]
                                                #搜索第一页 降序排列后的 前后2个均价差值不查过30%
                                                trlen= len(tablebody)
                                                
                                                data1=self.get_elemsa(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr/td/div'))
                                                for i in range(0,trlen):
                                                    sf=5+12*i
                                                    data1lit.append(int(data1[sf].text))
                                                data1litlne=len(data1lit)
                                                s[0]=data1lit[0]
                                                if data1litlne>2:
                                                    for ii in range(0,data1litlne-1):
                                                        if (data1lit[ii+1]-data1lit[ii])/data1lit[ii] < 0.3:
                                                            s[1]=data1lit[ii]
                                                            break
                                                else:
                                                    s[1]=data1lit[0] 
                                                #点击第二次成交楼板价 升序排列
                                                while True:
                                                    loucjth2=self.get_elem(self.dr,("xpath","//table[@class=\'el-table__header\']/thead/tr/th[6]"))
                                                    if self.tobeclick(loucjth2,('xpath',".//div")):
                                                    #self.dr.execute_script("arguments[0].click();", loucj2)
                                                        self.dr.execute_script("var cj=document.getElementsByClassName(\"cell\");cj[5].click();")
                                                        break
                                                timesc=time.time()
                                                while True:
                                                    time1=time.time()
                                                    if self.visibilityy(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr[1]'),15):
                                                        break
                                                    if time1-timesc >30:
                                                        lix=lix-1
                                                        sff=False
                                                        break
                                                if sff:
                                                    data2=self.get_elems(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr/td/div'),5)
                                                    s[2]=int(data2.text)
                                                    resslutlist.append(s)

                                        else:
                                            resslutlist.append(s)
                                    else:
                                        resslutlist.append(s)
                                else:
                                    if chonglai<5:
                                        lix=lix-1
                                        chonglai=chonglai+1
                                    else:
                                        chonglai=0
                                
                        else:
                            resslutlist.append(s)
                    else:
                        lix=lix-1
                    lix +=1
                    print(s) 

        return  resslutlist
                                  

                                            


    @staticmethod
    def get_elem(brow,aa,time=15):
        try:
            element = WebDriverWait(brow,time).until(lambda x:x.find_element(*aa))
            return element
        except WebDriverException:
            print(WebDriverException)
            return None
    @staticmethod        
    def get_elems(brow,aa,x,time=15):
        try:
            elements = WebDriverWait(brow,time).until(lambda x:x.find_elements(*aa))
            return elements[x]
        except WebDriverException:
            print(WebDriverException)
            return None
    @staticmethod
    def get_elemsa(brow,aa,time=15):
        try:
            elements = WebDriverWait(brow,time).until(lambda x:x.find_elements(*aa))
            return elements
        except WebDriverException:
            print(WebDriverException)
            return None
    @staticmethod
    def get_eleminxpath(brow,aa):
        try:
            element = brow.find_element_by_xpath(aa)
            return element
        except WebDriverException:
            print(WebDriverException)
            return None
    @staticmethod
    def get_eleminsxpath(brow,aa):
        try:
            elements = brow.find_elements_by_xpath(aa)
            return elements
        except WebDriverException:
            print(WebDriverException)
            return None            
    @staticmethod
    def get_eleminclass(brow,aa):
        try:
            elements = brow.find_element_by_class_name(aa)
            return elements
        except WebDriverException:
            print(WebDriverException)
            return None
    @staticmethod
    def get_elemsinxpath(brow,aa):
        try:
            elements = brow.find_elements_by_xpath(aa)
            return elements
        except WebDriverException:
            print(WebDriverException)
            return None
    @staticmethod
    def visibilityy(brow,aa,time=15):
        try:
            isv=WebDriverWait(brow,time).until(EC.visibility_of_element_located(aa))
            return isv
        except WebDriverException:
            print(WebDriverException)
            return False
    @staticmethod
    def tobeclick(brow,aa,time=10):
        try:
            isv=WebDriverWait(brow,time).until(EC.element_to_be_clickable(aa))
            return isv
        except WebDriverException:
            print(WebDriverException)
            return False
    @staticmethod
    def searchac(databserul,tablen,where):
        search=access_model(databserul)
        reasult=search.muselect(where,tablen)
        return reasult

   

def read_excel(filename,sheetname,ncol,ncol2):
        dataa = []
        book = xlrd.open_workbook(filename)
        sheet = book.sheet_by_name(sheetname) #book.sheet_by_name('sheet1')
        ra = sheet.nrows
        #na= sheet.ncols 
        #for aa in range(0,na):
           # self.lie.append(sheet.cell_value(0,aa))
        for i in range(1,ra):
            s=[]
            v = sheet.cell_value(i,ncol)
            v1=sheet.cell_value(i,ncol2)
            s.append(v)
            s.append(i) #序号
            s.append(v1)
            dataa.append(s)
        return dataa

def exlcelwrite(df, filename,sheetname,rangestart='Q2'):
    if os.path.exists(filename):
        pass
    else:
        excelApp = xlw.App(False, False)
        excelFile = excelApp.books.add()
        excelFile.sheets.add(sheetname)
        excelFile.save(filename)

    app=xlw.App(visible=True,add_book=False)    
    wb=app.books.open(filename,update_links=False)
    sh=wb.sheets[sheetname]
    sh.range(rangestart).value=df.values
    wb.save()
    wb.close()
    app.quit()
    # writebook = xlwt.Workbook() 
    # sheet= writebook.sheet_by_name(sheetname)  
    # c=0
    # for d in a: #取出data中的每一个元组存到表格的每一行
    #     for index in range(0,len(d)):   #将每一个元组中的每一个单元存到每一列
    #         sheet.write(c,index,d[index])
    #     c += 1
    # writebook.save(filename)

if __name__ == "__main__":

    mi=configparser.ConfigParser()
    mi.readfp(open('./ressearch/in.ini'))
    no1=mi.get('key','no')
    url=mi.get('key','res')
    search=base(url)
    
    databaur=r"F:\地价\test\test\conn\Database1.accdb"
    
    ls=['2020-05-01','2020-08-20','成交','住宅']#列表[开始时间，结束时间，交易状态，类型] #土地成交导入access
    search.insert_access(no1,ls,'bj_table',databaur)
    
    #################################################################

    # repath=r"e:\一手典型楼盘.xlsx"
    # readexcl=read_excel(repath,'Sheet1',3,0)
    # login1=search.logindd(no1)
    # if login1:
    #     times=time.time()
    #     resresponse=search.firstfang(readexcl)
    #     dff=pd.DataFrame(resresponse,columns={"最高","中","最低"})
    #     print(dff)
    #     exlcelwrite(dff,repath,"Sheet1")
    #     t=(time.time()-times)/60
    #     print(t)
    
        
    
    # tname="bj_table"
    # tatol=[]
    # dd={}

    # f=list(search.searchac(databaur,tname,dd))
    # for sf in f :
    #     ls=[]
    #     x= sf[7].strftime("%Y-%m-%d") #datetime.datetime.strptime(sf[7],'%Y-%m-%d %H-%M-%S')
    #     for i in range(0,7):
    #         ls.append(sf[i])
    #     ls.append(x)
    #     for i in range(8,len(sf)):
    #         ls.append(sf[i])
    #     tatol.append(ls)
    # print(tatol)
    
    