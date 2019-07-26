from selenium import webdriver
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select

t1 = False

def resh(brow,i1):
    global t1
    handle = brow.current_window_handle
    i1= i1+1
    try:
        if not EC.title_is(u"房地产估价报告网上备案管理系统")(brow):
            if i1>0:
                act = ActionChains(brow)
                act.send_keys(Keys.F5).perform()
            else:
                brow.get("http://218.242.60.234:7001/fangdi/system/USBLogin.jsp")
                handle = brow.current_window_handle
            
            input_loc = ("name","keypwd")
            WebDriverWait(brow,10).until(lambda x:x.find_element(*input_loc)).send_keys("bdf5cfbc")
            brow.find_element_by_name("Submit2").click()
            handles = brow.window_handles
            for newhandle in handles:
        # 筛选新打开的窗口B
                if newhandle != handle :
    # 切换到新打开的窗口B
                    brow.switch_to.window(newhandle)
                    if WebDriverWait(brow,30).until(EC.title_is(u"房地产估价报告网上备案管理系统")):
                        #print(EC.title_is(u"房地产估价报告网上备案管理系统")(brow))
                        t1 = True
                        return brow
        else:
            t1 = True
            return brow
    except Exception as e:
        print(e)
        brow.switch_to.window(handle)
        return resh(brow,i1)
    else:
        while i1 < 5:
                brow.switch_to.window(handle)
                resh(brow,i1)
            
        brow.switch_to.window(handle)
        return brow
def connect(data):
    global t1 
    t1= False
    browser = webdriver.Ie()
    browser = resh(browser,0)
    
    if t1:
        WebDriverWait(browser,15).until(EC.visibility_of_element_located((By.NAME,'headFrm')))
        iframe = browser.find_element_by_name("headFrm")
        browser.switch_to.frame(iframe)
        b1 = browser.find_elements_by_xpath("//td[@class='menu_unact']")
        for b in b1:
            if b.text == "报告备案":
                browser.execute_script("arguments[0].id='b1';", b)
        aa = browser.find_elements_by_xpath("//td[@id='b1']/div")
    #ActionChains(browser).move_to_element(target).perform()
    #print(browser.page_source)
        for u in aa:
            browser.execute_script("arguments[0].style.display='inline';", u)
        aa1 = browser.find_elements_by_xpath("//td[@id='b1']/div//li[@class='list1']")
        for a in aa1:
            InnerElement = a.get_attribute('innerHTML')
            if str(InnerElement) == "起草":
                a.click()
        browser.switch_to.default_content()
        #进入新增页面
       
        iframe = browser.find_element_by_name("mainFrm")
        browser.switch_to.frame(iframe)       
        iframe = browser.find_element_by_name("list")
        browser.switch_to.frame(iframe)
        iframe = browser.find_element_by_name("reportFormAction")
        browser.switch_to.frame(iframe)
        #browser.find_element_by_xpath("//input[@value='新增']").click()
        browser.execute_script("var aEle=document.getElementsByTagName('input');  for(var i=0;i<aEle.length;i++){ if(aEle[i].getAttribute('value')=='新增') { aEle[i].click(); break;}  } ")
        time.sleep(1)
        browser.switch_to.default_content()
        iframe = browser.find_element_by_name("mainFrm")
        browser.switch_to.frame(iframe)       
        iframe = browser.find_element_by_name("list")
        browser.switch_to.frame(iframe) 
        time.sleep(1)
    #开始填表
    #是否分户 是分户选择地址
        if data['isfenhu']: 
            browser.execute_script( "var aEle=document.getElementById('householdYes');aEle.click(); ")
            browser.execute_script( "var aEle=document.getElementsByTagName('*');  for(var i=0;i<aEle.length;i++){ if(aEle[i].getAttribute('name')=='assessAim')  {if(aEle[i].getAttribute('value')=="+data['assessAim']+") { aEle[i].click(); break;}  } } ")
            browser.execute_script( "var aEle=document.getElementById('getObject');aEle.click(); ")
            browser.execute_script("document.getElementById('proLocation').value = '"+data['location']+"'; ")
            time.sleep(3)
            browser.find_element_by_xpath("//div[@id='objDiv']//table[@class='table_all']//input[@value='查询']").click()
            time.sleep(5)
            #browser.execute_script("getObj();" )
            browser.execute_script("var ii=2; var t=0;var aEle=document.getElementsByTagName('*');var su=[];var su1=[];for(var i=0;i<aEle.length;i++){ if(aEle[i].className=='trlight' )  { su.push(aEle[i]);  } if(aEle[i].getAttribute('name')=='pcheckbox') {su1.push(aEle[i]); } }  while(ii<su.length){ if(su[ii].innerHTML=='"+data['buildingArea']+"') { su1[(ii-2)/7].click(); t=1; break;} ii=ii+7; }if(t==1)addObj(); else hiddenObjDiv();")
            #b2 = browser.find_elements_by_xpath("//td[@class='trlight']")[0]
            #print(b2.get_attribute('innerHTML'))
            #browser.execute_script("arguments[0].click();", b2)
            time.sleep(2)
            if browser.find_element_by_xpath("//input[@name='buildingArea']").get_attribute("value") == "":
                browser.find_element_by_xpath("//input[@name='buildingArea']").send_keys(data['buildingArea'])
                browser.find_element_by_id("location").send_keys(data['location'])
            #browser.execute_script("hiddenObjDiv()" )#关闭
           # browser.find_element_by_id("householdYes").click()
        else:
            browser.execute_script( "var aEle=document.getElementsByTagName('*');  for(var i=0;i<aEle.length;i++){ if(aEle[i].getAttribute('name')=='assessAim')  {if(aEle[i].getAttribute('value')=="+data['assessAim']+") { aEle[i].click(); break;}  } } ")
            browser.execute_script( "var aEle=document.getElementById('householdNo');aEle.click(); ")
            #browser.find_element_by_id("householdNo").click()
        #项目名称
        browser.find_element_by_id("projectName").send_keys(data['projectName'])
        #总报告编号
        browser.find_element_by_id("fatherReportNO").send_keys(data['fatherReportNO'])
        #报告编号
        browser.find_element_by_id("reportNO").send_keys(data['reportNO'])
        #委托方
        browser.find_element_by_id("client").send_keys(data['client'])
        #签字估价师2
        browser.find_element_by_id("estimatorTwo").send_keys(data['estimatorTwo'])
         #主要审核人
        browser.find_element_by_id("auditMan").send_keys(data['auditMan'])
        #估价目的
        

        #browser.find_elements_by_xpath("//table[@id='aimname1']//#tr//td//input[@id='assessAim']")[2].click()
        #房屋分类
        browser.execute_script( "var aEle=document.getElementsByTagName('input');  for(var i=0;i<aEle.length;i++){ if(aEle[i].getAttribute('name')=='houseUse')  {if(aEle[i].getAttribute('value')=="+data['houseUse']+") { aEle[i].click(); break;}  } } ")
         #居住或非居分类
        if int(data['houseReside'])>0:
            browser.execute_script( "var aEle=document.getElementsByTagName('*');  for(var i=0;i<aEle.length;i++){ if(aEle[i].getAttribute('name')=='houseReside')  {if(aEle[i].getAttribute('value')=="+data['houseReside']+") { aEle[i].click(); break;}  } } ")
        elif int(data['houseResideNo'])>0:
              browser.execute_script( "var aEle=document.getElementsByTagName('*');  for(var i=0;i<aEle.length;i++){ if(aEle[i].getAttribute('name')=='houseResideNo')  {if(aEle[i].getAttribute('value')=="+data['houseResideNo']+") { aEle[i].click(); break;}  } } ")
        #完成日期以及价值时点
        timu = browser.find_element_by_id("reportDate")
        browser.execute_script("arguments[0].style.onclick='';", timu)
        timu.send_keys(data['reportDate'])
        timu2 = browser.find_element_by_id("valueDate") 
        browser.execute_script("arguments[0].style.onclick='';", timu2)
        timu2.send_keys(data['valueDate'])
        #单价
        browser.find_element_by_id("assessOneValue").send_keys(data['assessOneValue'])   
        #选择区
        Select(browser.find_element_by_id("district")).select_by_value(data['district'])
        #内外环
        Select(browser.find_element_by_id("position")).select_by_value(data['position'])
        time.sleep(2)
        browser.find_element_by_xpath("//input[@value='暂存']").click()
         
        WebDriverWait(browser,10).until(lambda x:x.find_element("id","yesBtn")).click()
        WebDriverWait(browser,10).until(lambda x:x.find_element("Xpath","//input[@value='提交']")).click()
        alert = browser.switch_to_alert()
        alert.accept()

#print(browser.find_elements_by_xpath("//li[@class='list1']")[4].text)
#for b1 in b:
#print(b1.text())
#if b1.text() == "起草":
#b1.click()
#client委托方,rFileName项目名称,reportDate出具报告时间
#humanIDTwo签字估价师2 auditManId主要审核人 assessAim估价目的
#district区,position内中外环,location地址,buildingArea建筑面积
#houseResideNo 居住类型,valueDate价值时点,assessTotleValue,评估总价
#assessOneValue单价  houseUse 公房16 私房15  其他14
#proLocation 征收查询时的坐落
#//table[@id='objTab']//td[@class-'trlight'] [6]是姓名 [7]是点击选项
#//div[@id='objDiv']//table[@class-'table_all']//tr[@class='sub_window_head']//td/a
if __name__=="__main__":
    data2 = {'isfenhu':'householdYes','fatherReportNO':'F2019-00666','reportNO':'F2019-01222','projectName':'浦东新区XXXX','client':'XXX银行','reportDate':'2019-06-21','estimatorTwo':'齐刚','auditMan':'齐刚','assessAim':'3','district':'2','position':'1','location':'梧桐路36弄1号','buildingArea':'12.79','houseUse':'16','houseReside':'13','houseResideNo':'0','valueDate':'2019-06-06','assessTotleValue':'0','assessOneValue':'12345'}
    connect(data2)