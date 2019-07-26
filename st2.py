from baiduapi1 import BaiduApi
from pathlib import Path
import os
import imghdr


def shibie(filepath):
    baidu = BaiduApi()
    alltxt = ''
    pp = Path('write.txt')
    if os.path.exists(filepath):
        for dirp, dirnames, filenames in os.walk(filepath):
            for file in filenames:
                path = os.path.join(dirp, file)
                print(str(path))
                if imghdr.what(path):
                    alltxt = alltxt + baidu.picture(path).replace(' ', '')+'\n'              
                    wr = open(pp, "w+")
                    wr.write(alltxt)
                    wr.close()


if __name__ == '__main__': 
    
    shibie('./image')