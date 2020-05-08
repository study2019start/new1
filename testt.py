import re
import pandas as pd
import numpy
import os
import xlwings as xlw

re1=r"[\u4e00-\u9fa5]+(\d{4})[\u4e00-\u9fa5]*"

def res(listt):
    for lis in listt:
        result=re.findall(re1,lis)
        if result:
            print(result[0])

def wirte(df,mpath):
    svpath= "E:\\我的文档\\vba\\新建文件夹\\"  +"01.xlsx"
    if os.path.exists(svpath):
        pass
    else:
        os.system(" copy "+mpath + "  "+svpath)
   # with    pd.ExcelWriter(svpath) as wirter: # pylint: disable=abstract-class-instantiated
       # df.to_excel(wirter,sheet_name="评估汇总",startrow=2,startcol=0,header=False,index=False)
    app=xlw.App(visible=True,add_book=False)
    wb=app.books.open(svpath,update_links=False)
    sht=wb.sheets["评估汇总"]
    sht.range("A3").value= df.values
    wb.save()
    wb.close()
    app.quit()
    
def pandasr(path):
    df=pd.read_excel(path,sheet_name="Sheet1",header=[1],usecols=[0,1,2,3,4,5])
    return df
if  __name__ == "__main__":
   # lisd=["绿地外滩中心2018","绿地外滩2013中心","绿地2015"]
    #res(lisd)
    d=pandasr(r"E:\我的文档\vba\金陵东路64号地块给评估公司清册.xlsm")
    print(int(d.shape[0]/30+0.5))
    print(d)
   #df1=d.loc[d['序号']>10,['件袋号']].apply(lambda x: x+"-xs")
   #print(df1[1:20])
   #ef=d.loc[(d['序号']>0) & (d['序号']<31),['件袋号']]
   #print(ef.loc[[0],:].values[0])
    #wirte(d[2:32],r"E:\我的文档\vba\J-0001-J-0030-s.xlsx")
    