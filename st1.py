import time
import sys
import keyboard
from PIL import ImageGrab
from baiduapi1 import BaiduApi
from setclopboard import Sc


def screenshot():
    if keyboard.wait('ctrl+1') == None:
        
            time.sleep(0.01)

            im = ImageGrab.grabclipboard()
            im.save('iamgGrab.png')


if __name__ == '__main__': 
    x = 1
    while x < 10:
        screenshot()

        baidu = BaiduApi()
        sc =Sc()
        text = baidu.picture('iamgGrab.png')
        print(text)
        sc.set_text(text)

