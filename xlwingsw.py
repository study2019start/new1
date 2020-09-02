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
        app2=xw.App(visible=False,add_book=False)
        app2.display_alerts=False
        app2.screen_updating=False
        i1=i*30+3
        i2=(i+1)*30+2
        if i2 > rows:
            i2=rows
        na1=''.join([sht.range(namel+str(i1)).value,"-",sht.range(namel+str(i2)).value,".xlsx"])   #保存文件名
        
        tpath2=os.path.join(tpath,na1)#保存路径
        if os.path.isfile(tpath):
            fpp=tpath2
        else:
            fpp=target
        wbf=app2.books.open(fpp)
        shtp=wbf.sheets[sname]
      
        for li,ll in enumerate(targetlist):
            npl=sht.range(''.join([zonglist[li],str(i1),":",zonglist[li],str(i2)])).value
            shtp.range(ll+str(i1)).options(transpose=True).value=npl
        
        wbf.save(tpath2)
        wbf.close()
        app2.kill()
       
    wb.close()
    app.quit()




if __name__ == "__main__":
    y=r'E:\金陵东路\金陵东路64号地块给评估公司清册.xlsx'
    t=r'E:\金陵东路\模板.xlsx'
    yuanlist=['C','D','E','F','G']
    tarlist=['B','C','D','F','G']
    namel='C'
    mun='评估汇总'
    fen(y,t,yuanlist,tarlist,namel,mun,30)

  