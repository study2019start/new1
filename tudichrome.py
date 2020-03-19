from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys 
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.select import Select
from mysqlqk import qk_mysql_tu


def get_elem(brow,aa,time=30):
    element = WebDriverWait(brow,time).until(lambda x:x.find_element(*aa))
    return element


def get_elems(brow,aa,x,time=30):
    elements = WebDriverWait(brow,time).until(lambda x:x.find_elements(*aa))
    return elements[x]


def get_elemsa(brow,aa,time=30): #返回多个节点
    elements = WebDriverWait(brow,time).until(lambda x:x.find_elements(*aa))
    return elements

def op1(v):
    __browser_url = r'C:\Users\thl\AppData\Local\Google\Chrome\Application\chrome.exe'  #360浏览器的地址
    chrome_options = Options()
    chrome_options.binary_location = __browser_url
    chrome_options.add_argument('disable-infobars')
    driver = webdriver.Chrome(options = chrome_options)
    ii = 1
    
    vv2 =""
    tf = True
    driver.get("https://land.3fang.com/market/310100___2_____3_0_1.html")
    vv =time.mktime(time.strptime(v,'%Y-%m-%d'))
    print(vv)
    while tf:
        a1 = get_elemsa(driver,('xpath','//div[@class=\'list28_text fl\']//h3//a[@target=\'_blank\']'))
        for a in a1:
            b = str(a.get_attribute('innerHTML'))
            s = b.find("(")
            if  s>0:
                b = b[0:int(s-1)]
            print(b)
            a.click()
            handle = driver.current_window_handle
            handles = driver.window_handles
            for newhandle in handles:
            # 筛选新打开的窗口B
                if newhandle != handle :
        # 切换到新打开的窗口B
                    driver.switch_to.window(newhandle)
                    time.sleep(2)
            while True:
                if EC.presence_of_all_elements_located((By.ID,'printData1'))(driver):
                    break
                else:
                    driver.refresh()

            title = get_elem(driver,('xpath','//div[@class=\'tit_box01\']')).get_attribute('innerHTML')
            title =str(title).replace("<span class=\"state_box business_pass\"></span>","")
            print(title)
            tudjy = get_elemsa(driver,('xpath','//table[@class=\'tablebox02 mt10\']//td'))
            use1 = str(tudjy[1].get_attribute('innerHTML')).replace("<span class=\"gray2\">所在地：</span>","")
            ind = use1.find(u">")
            use1 = use1[int(ind+1):int(len(use1))]
            use1 = use1.replace("</a>","")
            use2 = str(tudjy[4].get_attribute('innerHTML')).replace("<span class=\"gray2\">规划建筑面积：</span>","").replace("<em class=\"red01\">","").replace("</em>","")
            use3 = str(tudjy[15].get_attribute('innerHTML'))
            use3 = use3.replace("<span class=\"gray2\">规划用途：</span>","")
            ind = use3.find(u">")
            use3 = use3[int(ind+1):int(len(use3))]
            use3 = use3.replace("</a>","")
            use4 = str(tudjy[20].get_attribute('innerHTML'))
            ind = use4.find(u"：")
            use4 = use4[int(ind+1):int(len(use4))]
            use4 = use4.replace("</span>","")
            vv2 =time.mktime(time.strptime(use4,'%Y-%m-%d'))
            if vv2 <vv:
                return 0
            use5 = str(tudjy[23].get_attribute('innerHTML'))
            ind = use5.find(u"：")
            use5 = use5[int(ind+1):int(len(use5))]
            use5 = use5.replace("</span>","")
            use6 = str(tudjy[24].get_attribute('innerHTML'))
            ind = use6.find(u"：")
            use6 = use6[int(ind+1):int(len(use6))]
            use6 = use6.replace("</span>","")
            mysqlins = {}
            mysqlins["t_name"] = title
            mysqlins["arear"] = use1
            mysqlins["zzmj"] = use2
            mysqlins["yt"] = use3
            mysqlins["cjrq"] = use4
            mysqlins["cjj"] = use5
            mysqlins["lmdj"] = use6
            qkm = qk_mysql_tu()
            qkm.insert(mysqlins)
            print(mysqlins) 
            print(vv2)
            time.sleep(1)
                        


                        
            driver.close()
            driver.switch_to_window(handles[0]) 
            time.sleep(1)
        ii = ii+1
        sss = get_elemsa(driver,('xpath','//div[@id=\'landlb_B04_23\']//div[@id=\'divAspNetPager\']//a'))
        for ss in sss:
            if ss.get_attribute("innerHTML") == str(ii):
                ss.click()
                break
    time.sleep(555)
    return 0
    


                
            

    
if __name__=="__main__":
    s = op1("2019-03-31")