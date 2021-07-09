import pandas as pd
import xlwings as xlw
import time
import os
import shutil
import datetime
import configparser

class model_excel(object):
    @classmethod
    def xlwingcreate(self,df,filename,rangestart='A1'):
        if os.path.exists(filename):
            fid1=filename.rfind(".")
            filename_ex=filename[fid1:]  #后缀名
            filename_newname=filename[:fid1]   #去除后缀名的路径
            filename_t=filename_newname+datetime.datetime.now().strftime("%Y%m%d%H%M%S")+filename_ex
        else:
            filename_t=filename
        app=xlw.App(visible=False,add_book=False)
        new_i=1
        book=app.books.add()
        for ii in  range(1,100):
            if sheetnameexit(book,str(ii)):
                pass
            else:
                new_i=ii
                break
        book.sheets.add(str(new_i))
        book.sheets[str(new_i)].range(rangestart).value=df
        book.save(filename_t)
        book.close()
        app.quit()

    @classmethod
    def readexcel(self,file_path,sheet_name=0,hearder=None,skiprows=None,usecols=None):

        ddf=pd.read_excel(file_path,sheet_name = sheet_name,header=hearder,skiprows=skiprows,usecols=usecols)
        #ddf=ddf.drop(ddf.index[0])
        #ddf.rename(columns={0:'fd1',1:'fd33',2:'fd34',3:'checkno',4:'fd35',5:'fd36'}, inplace=True)

        return ddf



    def xlwingwirte(self,df,filename,sheetname,copy,rangestart='H2'):
        
        #print(df)
        findd=filename.rfind('.')
        findd1=filename.rfind('\\')
        
        st1=filename[findd:len(filename)] #后缀名
        st2=filename[findd1:findd] #文件名
        st3=filename[0:findd1] #文件所在目录
        
        if copy:
           
            newfn=st2+str(time.strftime("%H%M%S",time.localtime()))+st1  #文件名加入时间
            svpath=os.path.join(st3,newfn)
            shutil.copy(filename,svpath)
        else:
            svpath=filename
        app=xlw.App(visible=False,add_book=False) 
        if os.path.exists(svpath):
            wb=app.books.open(svpath,update_links=False)
        else:
            wb=app.books.add()
        if sheetname:
            if sheetnameexit(wb,sheetname):
                sh=wb.sheets[sheetname]
            else:
                sh=wb.sheets.add(sheetname)
        else:
            sh=wb.sheets[0]
        
        sh.range(rangestart).value=df.values
        mi=configparser.ConfigParser()
        mi.readfp(open(r'in.ini'))
        key1=mi.get('key','name')
        if st2.find(key1) > -1:
            hang=df.shape[0]+4
            sh.range('L5:L'+str(hang)).NumberFormatLocal = "@"
        wb.save(svpath)
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