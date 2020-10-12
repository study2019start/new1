import pandas as pd
import xlwings as xlw
import time
import os
import shutil
import datetime
class model_excel(object):
    def xlwingcreate(self,df,filename,rangestart='A1'):
        if os.path.exists(filename):
            fid1=filename.rfind(".")
            filename_ex=filename[fid1:]  #后缀名
            filename_newname=filename[:fid1]   #去除后缀名的路径
            filename_t=filename_newname+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+filename_ex
        else:
            filename_t=filename
        app=xlw.App(visible=False,add_book=False)
        book=app.books.add()
        book.sheets.add("1")
        book.sheets["1"].range(rangestart).value=df
        book.save(filename_t)
        book.close()
        app.quit()

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
        if os.path.exists(svpath):
            wb=app.books.open(svpath,update_links=False)
        else:
            wb=app.books.add()
        if sheetnameexit(wb,sheetname):
            sh=wb.sheets[sheetname]
        else:
            sh=wb.sheets.add(sheetname)
        
        sh.range(rangestart).value=df.values
        if st2.find('信衡') > -1:
            hang=df.shape[0]+4
            sh.range('L5:L'+str(hang)).NumberFormatLocal = "@"
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