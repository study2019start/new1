import time
import datetime
import xlwings as xw
import math
import os

def fen(zong,target,zonglist,targetlist,namel,sname,fens=30): #两清表，模板，两清需要复制的列集合，模板列集合，命名列，模板sheets名字，一表多少行
    app=xw.App(visible=False,add_book=False)
    app.display_alerts=False
    app.screen_updating=False
    wb=app.books.open(zong)
    sht=wb.sheets['Sheet1']
    gindex=target.rfind("\\")
    tpath=target[0:gindex] #模板所在目录
    rows=sht.api.UsedRange.Rows.count #总行数 
    fen1=math.ceil((rows+2)/fens) #需要分多少个表 数据从第三行开始
    for i in range(0,fen1):
        i1=i*30+3
        i2=(i+1)*30+2
        if i2 > rows:
            i2=rows
        wbf=app.books.open(target)
        shtp=wbf.sheets[sname]
        na1=''.join([sht.range(namel+str(i1)).value,"-",sht.range(namel+str(i2)).value,".xlsx"])   #保存文件名
        for ll,li in enumerate(targetlist):

            npl=sht.range(''.join([zong[li],str(i1),":",zong[li],str(i2)])).value
            shtp.range(ll+str(i1)).optins(transpose=True).value=npl
        tpath=os.path.join(tpath,na1)#保存路径
        
        wbf.save(tpath)
        wbf.close()
    wb.close()





if __name__ == "__main__":
    pass