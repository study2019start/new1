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


class base(object):
    def __init__(self,ur):
        self.url=ur

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

        

    def tudisearch(self): #列表[开始时间，结束时间，交易状态，类型，多少页]
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
                    self.get_eleminxpath(form1,".//input[@placeholder=\'开始日期\']").send_keys("2020-01-01")
                    self.get_eleminxpath(form1,".//input[@placeholder=\'结束日期\']").send_keys("2020-03-25")
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
                                if str(dd.text)=="成交":
                                    sdd=True
                        if sdd:
                            break
                    ActionChains(self.dr).click(yjl).perform()

                    

                    #点击规划用途
                    self.get_elemsinxpath(form1,".//input[@class=\'el-input__inner\']")[20].click()
                    time.sleep(1)
                    gui=self.visibilityy(self.dr,('xpath','//ul[@class=\'el-scrollbar__view el-select-dropdown__list\']/li/span[text()=\'住宅\']'))
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
                    loucjth=self.get_elem(self.dr,("xpath","//table[@class=\'el-table__header\']/thead/tr/th[13]"))
                    loucj=self.get_eleminxpath(loucjth,".//div")
                    #点击第一次成交楼板价 按成交楼板价降序排列
                    loucj.click()
                    #判断数据列表是否出现 出现再点击成交楼板价
                    while True:
                        if self.visibilityy(self.dr,('xpath','//table[@class=\'el-table__body\']/tbody/tr[1]'),15):
                            break

                    #点击第二次成交楼板价
                    
                    while True:
                        loucjth2=self.get_elem(self.dr,("xpath","//table[@class=\'el-table__header\']/thead/tr/th[13]"))
                        if self.tobeclick(loucjth2,('xpath',".//div")):
                        #self.dr.execute_script("arguments[0].click();", loucj2)
                            self.dr.execute_script("var cj=document.getElementsByClassName(\"cell\");cj[12].click();")
                            break
                    while True:
                        if self.visibilityy(self.dr,('xpath','//table[@class=\'el-table__body\']/tbody/tr[1]'),15):
                            break

                    listss=self.get_elemsa(self.dr,('xpath','//table[@class=\'el-table__body\']/tbody/tr'),30)

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
            elements = brow.find_element_by_xpath(aa)
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


if __name__ == "__main__":

    mi=configparser.ConfigParser()
    mi.readfp(open('in.ini'))
    no1=mi.get('key','no')
    url=mi.get('key','res')
    search=base(url)
    print(search)
    login1=search.logindd(no1)
    if login1:
        search.tudisearch()
        
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
    
    pass