from mysqlconn import xiaoqu_mysql_lou
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
import datetime
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from access import access_model
import configparser


class base(object):
    def __init__(self,ur):
        self.url=ur

    def logindd(self):
        chrome_options = Options()
        __browser_url = r'C:\Users\thl\AppData\Local\Google\Chrome\Application\chrome.exe'
        chrome_options.binary_location = __browser_url
        chrome_options.add_argument('disable-infobars')
        driver = webdriver.Chrome(options = chrome_options)
        driver.get(self.url)
        mi=configparser.ConfigParser()
        mi.readfp(open('in.ini'))
        key=mi.get('key','no')
        self.get_elems(driver,('xpath','//input[@class=\'el-input__inner\']'),0).send_keys(key)#s收入账号
        if self.get_elem(driver,('xpath','//div[@id=\'tab-newhouse\']'),30):#等待30秒完成短信验证
            self.dr= driver
           
           
            return True
        else:
            return False

        

    def tudisearch(self):
        first=self.get_elem(self.dr,('xpath','//ul[@class=\'el-menu-vertical menu-ul-l el-menu\']/li[3]') )#一级市场
        print(first)
        count=0
        if first:
            ActionChains(self.dr).click(first).perform()
            tudi=self.get_eleminxpath(first,'.//span[text()=\'土地\']')#土地项目点击进入
            if tudi:
                tudi.click()
                #进入查询条件的form
                form1=self.get_elem(self.dr,("xpath","//form[@class=\'el-form res-table-search  el-form--label-right el-form--inline\']"))
                if form1:
                    #填入开始日期
                    self.get_eleminxpath(form1,"input[@placeholder=\'开始日期\']").send_keys("2020-01-01")
                    self.get_eleminxpath(form1,"input[@placeholder=\'结束日期\']").send_keys("2020-03-25")
                    #根据classsname 去除只读属性
                    js="var s =document.getElementsByClassName(\"el-input__inner\");  for(i=0;i<s.length;i++){s[i].removeAttribute(\"readonly\")};"
                    self.dr.execute_script(js)
                    self.get_eleminxpath(form1,"input[@class=\'el-input__inner\']")(2).send_keys("成交")
                    self.get_eleminxpath(form1,"input[@class=\'el-input__inner\']")(20).send_keys("住宅")
                    self.get_elem(self.dr,("xpath","//button[@class=\'el-button el-button--primary el-button--small\']")).click()
                    #if self.visibilityy(self.dr,('xpath','毕'))
                    while True:
                        if not EC.visibility_of_element_located(self.dr,('class name','el-loading-mask')
                        break
                    listss=self.get_elems(self.dr,('xpath','//table[@class=\'el-table__body\']/tr'))
                    if listss:  #数据列表的tr
                        for tr in listss:   
                            tdlist=self.get_elemsinxpath(tr,"//td/div")
                            if tdlist:
                                for tddiv in tdlist:
                                    print(tddiv.text())
                                    count=count+1
                                    if count=51:
                                        xi=self.get_eleminxpath





        time.sleep(5000)
        

    @staticmethod
    def get_elem(brow,aa,time=15):
        try:
            element = WebDriverWait(brow,time).until(lambda x:x.find_element(*aa))
            return element
        except BaseException:
            print(BaseException)
            return None
    @staticmethod        
    def get_elems(brow,aa,x,time=15):
        try:
            elements = WebDriverWait(brow,time).until(lambda x:x.find_elements(*aa))
            return elements[x]
        except BaseException:
            print(BaseException)
            return None
    @staticmethod
    def get_elemsa(brow,aa,time=15):
        try:
            elements = WebDriverWait(brow,time).until(lambda x:x.find_elements(*aa))
            return elements
        except BaseException:
            print(BaseException)
            return None
    @staticmethod
    def get_eleminxpath(brow,aa):
        try:
            elements = brow.find_element_by_xpath(aa)
            return elements
        except BaseException:
            print(BaseException)
            return None
    @staticmethod
    def get_eleminclass(brow,aa):
        try:
            elements = brow.find_element_by_class_name()
            return elements
        except BaseException:
            print(BaseException)
            return None
    @staticmethod
    def get_elemsinxpath(brow,aa):
        try:
            elements = brow.find_elements_by_xpath(aa)
            return elements
        except BaseException:
            print(BaseException)
            return None
    @staticmethod
    def visibilityy(brow,aa):
        try:
            isv=WebDriverWait(brow,15).until(EC.visibility_of_element_located(aa))
            return isv
        except BaseException:
            print(BaseException)
            return False

    @staticmethod
    def searchac(databserul,tablen,where):
        search=access_model(databserul)
        reasult=search.muselect(where,tablen)
        return reasult


if __name__ == "__main__":
    search=base('https://res.realtynavi.com/login')
    login1=search.logindd()
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