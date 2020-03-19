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
        self.get_elems(driver,('xpath','//input[@class=\'el-input__inner\']'),0).send_keys('15692157086')
        if self.get_elem(driver,('xpath','//div[@id=\'tab-newhouse\']'),20):
            return driver
        else:
            return None

        
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


if __name__ == "__main__":
    search=base('https://res.realtynavi.com/login')
    login1=search.logindd()
    print(login1)
    pass