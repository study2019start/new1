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
import xlwt

class base(object):
    def __init__(self,ur):
        self.url=ur



    def insert_access(self,nno,listno,tablename,dbname):
        self.logindd(nno)
        exit_model=access_model(dbname)
        resultln=self.tudisearch(listno)
        if resultln:
            for resul in resultln:
                wherelist={}
                wherelist['dizhi']=resul['dizhi']
                result_nol=exit_model.muselect(wherelist,tablename)
                if not len(result_nol)>1:
                    exit_model.insert(resul,tablename)
               


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

        

    def tudisearch(self,listno): #列表[开始时间，结束时间，交易状态，类型，多少页]
        first=self.get_elem(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li[3]') )#一级市场
        second=self.get_elem(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li[4]') )#二级市场
        count=16
        listap=[]#存放数据
        sdd=False
        if first:
            print(first.location)
            ActionChains(self.dr).click(first).perform()
            print(second.location)
            time.sleep
            tudi=self.visibilityy(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li/ul/li/span[text()=\'土地\']'))#土地项目点击进入

            if tudi:
                #print(tudi.loaction)
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
                        time.sleep(1)
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
                            if self.visibilityy(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr[1]'),15):
                                break

                        #点击第二次成交楼板价
                        
                        while True:
                            loucjth2=self.get_elem(self.dr,("xpath","//table[@class=\'el-table__header\']/thead/tr/th[13]"))
                            if self.tobeclick(loucjth2,('xpath',".//div")):
                            #self.dr.execute_script("arguments[0].click();", loucj2)
                                self.dr.execute_script("var cj=document.getElementsByClassName(\"cell\");cj[12].click();")
                                break
                        while True:
                            if self.visibilityy(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr[1]'),15):
                                break

                        listss=self.get_elemsa(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr'),30)

                        if listss:  #遍历数据列表的tr
                            for tr in listss:
                                #获取详情按钮 并点击
                                time.sleep(2)
                                tdlist=self.get_elemsinxpath(tr,".//td/div")[count] #第17个div
                                self.get_eleminxpath(tdlist,'.//button').click()  #点开详细页
                                el_dialog=self.get_elem(self.dr,("class name","el-dialog"))
                                if el_dialog:
                                    dicr={}
                                    
                                    #记录内容的列
                                    zilist=self.get_elemsinxpath(el_dialog,".//table[@class=\'market-detail-table\']/tr/td")
                                    dicr['dizhi']=self.get_eleminxpath(zilist[4],'.//span').text
                                    dicr['sizhi']=self.get_eleminxpath(zilist[5],'.//span').text
                                    dicr['leix']=self.get_eleminxpath(zilist[6],'.//span').text
                                    dicr['rj']=str(self.get_eleminxpath(zilist[10],'.//span').text).replace('%','')
                                    dicr['time']=self.get_eleminxpath(zilist[20],'.//span').text
                                    dicr['dijia']=str(self.get_eleminxpath(zilist[17],'.//span').text).replace('(元/m²)','')
                                    dicr['lx']=dicr['leix']
                                    #把字典数据放入listap列表
                                    listap.append(dicr)
                                    time.sleep(2)
                                    #关闭弹出框
                                    self.dr.execute_script("var i= document.getElementsByClassName(\"icon-close icon-location\"); i[0].click();")

                                
                            print(listap)
                        pagenext=self.get_elem(self.dr,('xpath','//ul[@class=\'el-pager\']/li[text()=\''+str(2) +'\']'))  #点击第二页
                        if pagenext:
                            pagenext.click()
        time.sleep(5000)
        return listap
        



    def firstfang(self,lists): #列表[开始时间，结束时间，交易状态，类型，多少页]
        resslutlist=[]
        now=datetime.datetime.now().strftime("%Y-%m-%d")
        fyear= datetime.datetime.strftime(datetime.datetime.now()+datetime.timedelta(days=-365),"%Y-%m-%d")
        print(now)
        print(fyear)
        first=self.get_elem(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li[3]') )#一级市场
        second=self.get_elem(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li[4]') )#二级市场
        if second:
            print(first.location)
            ActionChains(self.dr).click(second).perform()
            print(second.location)
            time.sleep
            while True:
                if not self.visibilityy(self.dr,('class name','el-loading-mask'),3):
                    break
            xin=self.visibilityy(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li/ul/li/span[text()=\'新房成交\']'))#新房点击进入
            if xin:
                #print(tudi.loaction)
                for lststr in lists:
                    s=[-1,-1,-1]
                    ActionChains(self.dr).click(xin).perform()
                    while True:
                        if self.visibilityy(self.dr,('xpath','//input[@placeholder=\'开始日期\']')):
                            break
                        else:
                            xin.click()
                    #进入查询条件的form
                    print(xin.location)
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
                        ActionChains(self.dr).click_and_hold(loup).release().perform()  #鼠标点击搜索框
                        time.sleep(2)
                        ActionChains(self.dr).send_keys(lststr[0]).perform() #模拟输入
                        time.sleep(3)
                        
                        kuang=self.get_elem(self.dr,("xpath","//div[@class=\'el-popover el-popper popversearch-cot popversearch-xinz\']/div/div[@class=\'el-table__body-wrapper is-scrolling-none\']"))
                        if str(kuang.text).find("暂无数据")>0:
                            resslutlist.append(s)
                            print(s) 
                            break

                        else:
                            trueindex=-1
                            tdli=self.get_eleminsxpath(kuang,'.//tr/td/div')
                            lens=len(tdli)
                            for iid in range(0,lens):
                                tempi=iid*4+2
                                nameiid=str(tdli[tempi].text)
                                print(nameiid)
                                if nameiid.find('商业') > 0 or nameiid.find('办公') > 0:
                                    pass
                                else:
                                    trueindex=tempi
                                    break
                            if trueindex>-1:
                                tdli[trueindex].click()
                                time.sleep(2)  
                                self.get_elem(self.dr,('xpath','//span[@class=\'el-tag res-zhuzai el-tag--small\']')).click()
                                #查询按钮
                                self.get_elem(self.dr,("xpath","//button[@class=\'el-button el-button--primary el-button--small\']")).click()
                                time.sleep(1)
                                #if self.visibilityy(self.dr,('xpath',''))
                                #判断是否数据列表出现
                                while True:
                                    if not self.visibilityy(self.dr,('class name','el-loading-mask'),2):
                                        break

                                if not self.visibilityy(self.dr,('xpath','//div[@class=\'el-table__empty-block\']'),3):
                                    loucjth=self.get_elem(self.dr,("xpath","//table[@class=\'el-table__header\']/thead/tr/th[6]"))
                                    loucj=self.get_eleminxpath(loucjth,".//div")
                                    #点击第一次成交楼板价 按成交楼板价降序排列
                                    loucj.click()
                                    #判断数据列表是否出现 出现再点击成交楼板价
                                    while True:
                                        if self.visibilityy(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr[1]'),15):
                                            break
                                    tablebody=self.get_elemsa(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr'))
                                    pagetotal=self.get_elem(self.dr,('xpath','//span[@class=\'el-pagination__total\']'))
                                    inpagetotl=int(str(pagetotal.text).replace('共 ','').replace(' 条',''))
                                    print(inpagetotl)
                                    data1lit=[]
                                    #搜索第一页 降序排列后的 前后2个均价差值不查过30%
                                    trlen= len(tablebody)
                                    print(trlen)
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
                                    while True:
                                        if self.visibilityy(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr[1]'),15):
                                            break
                                    data2=self.get_elems(self.dr,('xpath','//div[@class=\'res-table-search\']//table[@class=\'el-table__body\']/tbody/tr/td/div'),5)
                                    s[2]=int(data2.text)
                                    resslutlist.append(s)

                                else:
                                    resslutlist.append(s)
                            else:
                                resslutlist.append(s)
                    else:
                        resslutlist.append(s)
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

    @staticmethod
    def insert1(databserul,tablen,where):
        inser=access_model(databserul)
        reasult=inser.insert(where,tablen)
        return reasult

def read_excel(filename,sheetname,ncol):
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

if __name__ == "__main__":

    mi=configparser.ConfigParser()
    mi.readfp(open('in.ini'))
    no1=mi.get('key','no')
    url=mi.get('key','res')
    search=base(url)
    #print(search)
    repath=r"e:\一手典型楼盘.xlsx"
    readexcl=read_excel(repath,'Sheet1',3)
    login1=search.logindd(no1)
    fname2="E:\\"+str(time.strftime("%H%M%S",time.localtime()))+".xls"
    if login1:
        resresponse=search.firstfang(readexcl)
        print(resresponse)
        exlcelwrite(resresponse,fname2)
        #search.tudisearch()
        
    databaur=r"F:\地价\test\test\conn\Database1.accdb"
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
    
    