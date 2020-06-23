import pandas as pd
import xlwings as xlw
import time
import os
import shutil
class model_excel(object):

    def xlwingwirte(self,df,filename,sheetname,copy,rangestart='H2'):

        #print(df)
        if copy:
            findd=filename.rfind('.')
            findd1=filename.rfind('\\')
            st1=filename[findd:len(filename)] #后缀名
            st2=filename[findd1:findd] #文件名
            st3=filename[0:findd1] #文件所在目录
            newfn=st2+str(time.strftime("%H%M%S",time.localtime()))+st1  #文件名加入时间
            svpath=os.path.join(st3,newfn)
            shutil.copy( filename,svpath)
        else:
            svpath=filename
        app=xlw.App(visible=False,add_book=False)    
        wb=app.books.open(svpath,update_links=False)
        if sheetnameexit(wb,sheetname):
            sh=wb.sheets[sheetname]
        else:
            sh=wb.sheets.add(sheetname)
        
        sh.range(rangestart).value=df.values
        wb.save()
        wb.close()
        app.quit()

def sheetnameexit(wb,shn):
    nsheet = wb.sheets
    tfexit=False
    for shtt in nsheet:
         
        if shtt.name==shn:
            tfexit=True
            break
    return tfexit