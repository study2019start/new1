from mysqlconn import xiaoqu_mysql_lou
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from mysqlzongtable import xiaoqu_mysql_zong
import json
from xls import xlsread
import configparser

def get_elem(brow,aa,time=15):
    try:
        element = WebDriverWait(brow,time).until(lambda x:x.find_element(*aa))
        return element
    except BaseException:
        print(BaseException)
        return None
    


def get_elems(brow,aa,x,time=15):
    elements = WebDriverWait(brow,time).until(lambda x:x.find_elements(*aa))
    return elements[x]


def get_elemsa(brow,aa,time=15):
    elements = WebDriverWait(brow,time).until(lambda x:x.find_elements(*aa))
    return elements

def op1(v):
    __browser_url = r'C:\Users\thl\AppData\Local\Google\Chrome\Application\chrome.exe'  #浏览器的地址
    chrome_options = Options()
    chrome_options.binary_location = __browser_url
    chrome_options.add_argument('disable-infobars')
    driver = webdriver.Chrome(options = chrome_options)
    driver.get("http://218.242.60.234:8080/wsjcj/api/index.html")
    mi=configparser.ConfigParser()
    mi.readfp(open('in.ini'))
    key=mi.get('key','no')
    get_elem(driver,('name','j_username')).send_keys(key)
    get_elem(driver,('name','j_password')).send_keys("111111")
    get_elem(driver,('xpath','//input[@value=\'登 录\']')).click()
    get_elems(driver,('xpath','//li[@class=\'menunotice\']'),4).click()
    
    lxl = ("花园住宅","联列住宅","公寓","其他")
    ss=xiaoqu_mysql_lou()
    s=int(str(ss.select('pdlou',None,'id','desc',1)[0][0]))+1
    print(s)
    for vv in v:
        iframe =  get_elem(driver,('id','mainframe'))
        driver.switch_to.frame(iframe)
        ele = get_elem(driver,('id','COMMUNITY_NAME'))
        ele.clear()
        #driver.execute_script("arguments[0].value=''",ele)
        ele.send_keys(vv[1])
        Select(get_elem(driver,('id','CURRENT_STEP_ID'))).select_by_value("22")
        get_elem(driver,('xpath','//a[@class=\'mlinkbutton searchbtn\']')).click()
        time.sleep(2)
        if get_elem(driver,('xpath','//div[@class=\'datagrid-cell datagrid-cell-c1-COMMUNITY_NAME\']')).get_attribute('innerHTML'):
            time.sleep(2)  
            get_elem(driver,('xpath','//div[@class=\'datagrid-cell datagrid-cell-c1-COMMUNITY_NAME\']/a')).click()
            driver.switch_to.default_content()    
            ff = get_elem(driver,('xpath','//iframe[@frameborder=\'0\']'))
            driver.switch_to.frame(ff)
            ff2 = get_elem(driver,('id','formurl'))
            driver.switch_to.frame(ff2)
            
            #if vv[11] == "" and   EC.presence_of_all_elements_located((By.NAME,'FINISHED_YEAR'))(driver):
            yy = get_elemsa(driver,('xpath','//table[@class=\'formtable\']//td[@class=\"content\"]'))
            y = {}
            y['id']=str(vv[0])
            y['name'] =yy[0].get_attribute('innerHTML')
            y['year'] =yy[1].get_attribute('innerHTML')
            y['dis']=yy[3].get_attribute('innerHTML')
            y['xiaoqushux']=yy[5].get_attribute('innerHTML')
            y['bankuai']=yy[7].get_attribute('innerHTML')
            y['jiedao']=yy[8].get_attribute('innerHTML')
            y['juwei']=yy[9].get_attribute('innerHTML')
            y['lischool']=yy[11].get_attribute('innerHTML')
            y['huanxian']=yy[10].get_attribute('innerHTML')
            y['east']=yy[14].get_attribute('innerHTML')
            y['west']=yy[15].get_attribute('innerHTML')
            y['south']=yy[16].get_attribute('innerHTML')
            y['north']=yy[17].get_attribute('innerHTML')
            y['lx']="公寓"
            print(y)
            my = xiaoqu_mysql_zong()
            my.insert('pdzongtable',y)
            get_elems(driver,('xpath','//a[@class=\'tabs-inner\']'),3).click()
              
            if EC.presence_of_all_elements_located((By.XPATH,'//input[@name=\'BUILDING_LOCATION\']'))(driver):
                lou = iter(get_elemsa(driver,('xpath','//input[@name=\'BUILDING_LOCATION\']')))
                lx = iter(get_elemsa(driver,('xpath','//select[@name=\'TYPE_ID\']')))
                next(lou)
                next(lx)
                lls=[]
                for ou,x in zip(lou,lx):
                    use1 = int(x.get_attribute('oldval'))-1
                    use2 = ou.get_attribute('value')
                    mys = xiaoqu_mysql_lou()
                    m = (s,use2,lxl[use1],"","",str(vv[0]))
                    ll = {}
                    l = ("id","louname","lx","loucen","jiegou","z_id")
                    ll = dict(zip(l,m))
                    s= s+1
                    print(str(s)+ou.get_attribute('value')+"-----"+str(lxl[use1]))
                    lls.append(ll)
                mys.manyinsert("pdlou",lls)
            elif EC.presence_of_all_elements_located((By.CLASS_NAME,'trChangeColor'))(driver):   
                lou1 = get_elemsa(driver,('xpath','//tr[@class=\'trChangeColor\']//td[1]'))
                lou2 = get_elemsa(driver,('xpath','//tr[@class=\'trChangeColor\']//td[4]'))
                a = 0  
                lls=[]
                for lo in lou1:
                    ld = lo.get_attribute('innerHTML')
                    lx2 = lou2[a].get_attribute('innerHTML')  
                    a += 1
                    mys1 = xiaoqu_mysql_lou()
                    m = (s,ld,lx2,"","",str(vv[0]))
                    ll = {}
                    l = ("id","louname","lx","loucen","jiegou","z_id")
                    ll = dict(zip(l,m))
                    print(str(s)+"-----"+str(lx2)+"-----"+str(vv[0]))
                    lls.append(ll)
                    s=s+1
                mys1.manyinsert("pdlou",lls)
            lls=[]
            driver.switch_to.default_content()
            time.sleep(1)
            ff = get_elem(driver,('xpath','//iframe[@frameborder=\'0\']'))
            driver.switch_to.frame(ff)
            time.sleep(1)
            glclose=get_elem(driver,('class name','icon-close'))
            if glclose:
                try:
                    glclose.click()
                    driver.switch_to.default_content()
                except:
                    driver.refresh()
            else:
                driver.refresh()
            #driver.find_element_by_css_selector("[class='mlinkbutton closebtn']").click()
            #get_elem(driver,('xpath','//a[@class=\'mlinkbutton closebtn\']')).click()
        print(1)
        driver.switch_to.default_content()
        


    time.sleep(30)



def op2(v):
    __browser_url = r'C:\Users\thl\AppData\Local\Google\Chrome\Application\chrome.exe'  #360浏览器的地址
    chrome_options = Options()
    chrome_options.binary_location = __browser_url
    chrome_options.add_argument('disable-infobars')
    driver = webdriver.Chrome(options = chrome_options)
    driver.get("http://218.242.60.234:8080/wsjcj/api/index.html")
    get_elem(driver,('name','j_username')).send_keys("15692157086")
    get_elem(driver,('name','j_password')).send_keys("111111")
    get_elem(driver,('xpath','//input[@value=\'登 录\']')).click()
    

    for vv in v:
        
        get_elems(driver,('xpath','//li[@class=\'menunotice\']'),0).click()
        driver.switch_to.default_content()
        ff = get_elem(driver,('xpath','//iframe[@frameborder=\'0\']'))
        driver.switch_to.frame(ff)
        iframe =  get_elem(driver,('id','formurl'))
        driver.switch_to.frame(iframe)

        ele = get_elem(driver,('name','COMMUNITY_LOCATION'))
        driver.execute_script("arguments[0].removeAttribute('readonly')",ele)
        ele.clear()
        ele.send_keys(vv[1])
        Select(get_elem(driver,('name','DISTRICT'))).select_by_value("10")
        
        
        get_elems(driver,('xpath','//a[@class=\'tabs-inner\']'),3).click()
        sss = get_elemsa(driver,('xpath','//a[@class=\'mlinkbutton\']'))
        for ss in sss:
            if str(ss.get_attribute('innerHTML')).find(u"批量")>0:
                ss.click()
                break
        driver.switch_to.default_content()
        iframe1 =  get_elemsa(driver,('xpath','//iframe[contains(@src,\'selectBuild.html?type=2\')]'))
        for ifra in iframe1:
    
            driver.switch_to.frame(ifra)
            
            if EC.visibility_of_all_elements_located((By.CLASS_NAME,"mlinkbutton searchbtn")):
                sss = get_elems(driver,('xpath','//a[@class=\'mlinkbutton searchbtn\']'),0)
                sss.click()
                break
       
        Select(get_elem(driver,('xpath','//select[@class=\'pagination-page-list\']'))).select_by_index(8)
        
        
        o = 0
        ye =  get_elems(driver,('xpath','//div[@class=\'datagrid-pager pagination\']//td'),7)
        ye1 = str(ye.get_attribute('innerHTML')).replace("<span style=\"padding-right:6px;\">共","").replace("页</span>","")
        print(ye1)
        p = 1
        while p <= int(ye1):
            if p>1:
                get_elems(driver,('xpath','//a[@class=\'l-btn l-btn-small l-btn-plain\']'),0).click()
            time.sleep(3)
            aa = get_elemsa(driver,('xpath','//table[@class=\'datagrid-btable\']//div[@class=\'datagrid-cell datagrid-cell-c2-NAME\']'))
            bb = get_elemsa(driver,('xpath','//table[@class=\'datagrid-btable\']//div[@class=\'datagrid-cell datagrid-cell-c2-FLOOR\']'))
            cc = get_elemsa(driver,('xpath','//table[@class=\'datagrid-btable\']//div[@class=\'datagrid-cell datagrid-cell-c2-FINISHED\']'))
            for aaaa in aa:
                d={}
                d['name']= aaaa.get_attribute('innerHTML')
                d['loucen'] = bb[o].get_attribute('innerHTML')
                d['riqi'] =cc[o].get_attribute('innerHTML')
                xzz = xiaoqu_mysql_zong()
                xzz.insertloucen(d)
                print(str(vv[0])+"----"+aaaa.get_attribute('innerHTML')+"-----"+bb[o].get_attribute('innerHTML'))
                o=o+1

            
            
                #get_elem(driver,('xpath','//a[@class=\'mlinkbutton closebtn\']')).click()
            
            print(1)
            
            p=p+1
        driver.switch_to.default_content()
        time.sleep(3)  
        driver.refresh()
        time.sleep(2)
        
        
       
        
    time.sleep(300)


def op3(v):
    __browser_url = r'C:\Users\thl\AppData\Local\Google\Chrome\Application\chrome.exe'  #360浏览器的地址
    chrome_options = Options()
    chrome_options.binary_location = __browser_url
    chrome_options.add_argument('disable-infobars')
    driver = webdriver.Chrome(options = chrome_options)
    driver.get("http://218.242.60.234:8080/wsjcj/api/index.html")
    get_elem(driver,('name','j_username')).send_keys("15692157086")
    get_elem(driver,('name','j_password')).send_keys("111111")
    get_elem(driver,('xpath','//input[@value=\'登 录\']')).click()

    sid=""
    for vv in v:
        
        get_elems(driver,('xpath','//li[@class=\'menunotice\']'),0).click()
        driver.switch_to.default_content()
        ff = get_elem(driver,('xpath','//iframe[@frameborder=\'0\']'))
        sid = ff.get_attribute("name")
        print(sid)
        driver.switch_to.frame(ff)
        iframe =  get_elem(driver,('id','formurl'))
        driver.switch_to.frame(iframe)
        get_elem(driver,('name','COMMUNITY_NAME')).send_keys(vv[0])
        ele = get_elem(driver,('name','COMMUNITY_LOCATION'))
        driver.execute_script("arguments[0].removeAttribute('readonly')",ele)
        ele.send_keys(str(vv[3]).replace("、",";"))
        get_elem(driver,('name','FINISHED_YEAR')).send_keys(vv[10])
        Select(get_elem(driver,('name','DISTRICT'))).select_by_value("10")
        Select(get_elem(driver,('name','COMMUNITY_PROPERTY'))).select_by_value(str(shux(vv[9])))
        bank = int(bankuai(vv[1]))+1000
        Select(get_elem(driver,('name','PLATE'))).select_by_value(str(bank))
        Select(get_elem(driver,('name','CIRCLELINE'))).select_by_value(str(huanx(str(vv[2]).replace("间",""))))
        jiedao1 = int(jiedao(vv[11]))+1000
        Select(get_elem(driver,('name','STREET'))).select_by_value(str(jiedao1))
        get_elem(driver,('xpath','//a[@title=\'所在居委\']')).click()
        #get_elems(driver,('xpath','//li[@class=\'menunotice\']'),0).click()
        driver.switch_to.default_content()
        f1 = get_elem(driver,('xpath','//table[@class=\'ui_border ui_state_visible ui_state_focus ui_state_lock\']//iframe[@frameborder=\'0\']'))
        driver.switch_to.frame(f1)
        get_elem(driver,('xpath','//a[@class=\'mlinkbutton searchbtn\']')).click()
        check = get_elemsa(driver,('name','CODE'))
        tname = get_elemsa(driver,('xpath','//table[@class=\'datagrid-btable\']//div[@class=\'datagrid-cell datagrid-cell-c2-NAME\']'))
        jishu =0
        for tt in tname:
            print(tt.get_attribute('innerHTML'))
            if str(tt.get_attribute('innerHTML')).find(vv[12]) >=0:
                check[jishu].click()
                break
            jishu +=1
        get_elem(driver,('id','save')).click()
        driver.switch_to.default_content()
        f2 = get_elem(driver,('name',sid))
        driver.switch_to.frame(f2)
        iframe =  get_elem(driver,('id','formurl'))
        driver.switch_to.frame(iframe)
        get_elem(driver,('xpath','//a[@title=\'对口小学选择\']')).click()
        driver.switch_to.default_content()
        f1 = get_elem(driver,('xpath','//table[@class=\'ui_border ui_state_visible ui_state_focus ui_state_lock\']//iframe[@frameborder=\'0\']'))
        driver.switch_to.frame(f1)
        get_elem(driver,('id','NAME')).send_keys(str(vv[13]).replace("上海市","").replace("杨浦区","").replace("上海",""))
        get_elem(driver,('xpath','//a[@class=\'mlinkbutton searchbtn\']')).click()
        time.sleep(3)
        if EC.visibility_of_all_elements_located((By.XPATH,'//div[@class=\'datagrid-cell-check\']//input[@name=\'CODE\']'))(driver):
            time.sleep(3)
            get_elems(driver,('name','CODE'),0).click()
            get_elem(driver,('xpath','//div[@id=\'query\']//a[@class=\'mlinkbutton\']')).click()

        else:
            get_elem(driver,('xpath','//a[@class=\'mlinkbutton resetbtn\']')).click()
            get_elems(driver,('name','CODE'),0).click()
            get_elem(driver,('xpath','//div[@id=\'query\']//a[@class=\'mlinkbutton\']')).click()
            driver.switch_to.default_content()
            f2 = get_elem(driver,('name',sid))
            driver.switch_to.frame(f2)
            iframe =  get_elem(driver,('id','formurl'))
            driver.switch_to.frame(iframe)
            ele = get_elem(driver,('name','COUNTERPART_SCHOOL_TEXT'))
            driver.execute_script("arguments[0].removeAttribute('readonly')",ele)
            ele.clear()
            ele.send_keys(str(vv[13])) 
                   

        driver.switch_to.default_content()
        f2 = get_elem(driver,('name',sid))
        driver.switch_to.frame(f2)
        iframe =  get_elem(driver,('id','formurl'))
        driver.switch_to.frame(iframe)
        get_elem(driver,('name','EAST')).send_keys(vv[3])
        get_elem(driver,('name','WEST')).send_keys(vv[4])
        get_elem(driver,('name','SOUTH')).send_keys(vv[5])
        get_elem(driver,('name','NORTH')).send_keys(vv[6])        
        get_elem(driver,('xpath','//div[@class=\'nkform-tools-contain\']//a[@class=\'mlinkbutton\']')).click() 
        get_elems(driver,('xpath','//a[@class=\'tabs-inner\']'),3).click()
  
        
        sss = get_elemsa(driver,('xpath','//a[@class=\'mlinkbutton\']'))
        for ss in sss:
            if str(ss.get_attribute('innerHTML')).find(u"批量")>0:
                ss.click()
                break
        driver.switch_to.default_content()
        iframe1 =  get_elemsa(driver,('xpath','//iframe[contains(@src,\'selectBuild.html?type=2\')]'))
        for ifra in iframe1:
    
            driver.switch_to.frame(ifra)
            
            if EC.visibility_of_all_elements_located((By.XPATH,"//a[@class=\'mlinkbutton searchbtn\']"))(driver):
                sss = get_elems(driver,('xpath','//a[@class=\'mlinkbutton searchbtn\']'),0)
                sss.click()
                break
       
        Select(get_elem(driver,('xpath','//select[@class=\'pagination-page-list\']'))).select_by_index(8)
        
        
        o = 0
        ye =  get_elems(driver,('xpath','//div[@class=\'datagrid-pager pagination\']//td'),7)
        ye1 = str(ye.get_attribute('innerHTML')).replace("<span style=\"padding-right:6px;\">共","").replace("页</span>","")
        print(ye1)
        p = 1
        while p <= int(ye1):
            if p>1:
                get_elems(driver,('xpath','//a[@class=\'l-btn l-btn-small l-btn-plain\']'),0).click()
            time.sleep(3)
            aa = get_elemsa(driver,('xpath','//div[@class=\'datagrid-body\']//table[@class=\'datagrid-btable\']//div[@class=\'datagrid-cell datagrid-cell-c2-NAME\']'))
            bb = get_elemsa(driver,('xpath','//input[@name=\'CODE\']'))    
            lis=[]
            ji=0
            for aaa in aa:
                s={}
                s['name']=str(aaa.get_attribute('innerHTML'))
                s['code']=str(ji)
                print(s)
                lis.append(s)
                ji+=1
                #get_elem(driver,('xpath','//a[@class=\'mlinkbutton closebtn\']')).click()
            ji=0
            print(lis)
            lis2=[]
            for de in dedupe(lis, key=lambda s: s['name']):
                lis2.append(de)

            print(lis2)
            for lis1 in lis2:
                lisji = int(lis1['code'])
                bb[lisji].click()

            
            print(1)
            
            p=p+1
        get_elem(driver,('id','save')).click()
        time.sleep(5000)
        driver.switch_to.default_content()
        time.sleep(3)  
        driver.refresh()
        time.sleep(2)
        
        
       
        
    time.sleep(300)
def shux(s):
    shuxin=("商品房","售后公房","动迁安置房","商场","办公","店铺")
    i=0
    for a in shuxin:
        i=i+1
        if a==s:
            return i

def bankuai(s):
    ban=("东外滩","中原","五角场","新江湾城","鞍山","黄兴")
    i=0
    for a in ban:
        i=i+1
        if a==s:
            return i

def huanx(s):
    ban=("内环内","内中环","中外环","外交环","交环外")
    i=0
    for a in ban:
        i=i+1
        if a==s:
            return i

def dedupe(items, key=None):
    seen = []
    for item in items:
        val = item if key is None else key(item)
        print(val)
        if val not in seen:
            yield item
            seen.append(val)

def jiedao(s):
    ban=("长白新村街道","定海路街道","延吉新村街道","五角场镇","四平路街道","大桥街道","五角场街道","控江路街道","新江湾城街道","平凉路街道","殷行路街道","浦江路街道")
    i=0
    for a in ban:
        i=i+1
        if a==s:
            return i

if __name__=="__main__":
    #xzz = xiaoqu_mysql_zong()
    zz=xlsread('E://小区//南汇小区名.xls')
    ff=zz.readx()
    print(ff)
    op1(ff)
   # a = "order by  id  limit 559,300 "
   # b = xzz.selectdizhi(a)

    #print(b)
   # c =(('上和园','新江湾城','内中环间','国安路355弄、国安路259弄','国安路','清流环一路，政云路','三门路北侧绿地，三门路','清流环一路，民府小区','公寓','商品房','2015','新江湾城街道','政立路第二居委会','上海市杨浦区复旦科技园小学'),)
  #  op3(c)
    #op1(b)