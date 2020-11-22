from yugu import yugum
import os
from tkinter import *
from  tkinter.filedialog import *
from tkinter.messagebox import *

root = Tk()

root.title('Baojia')
 
# 第3步，设定窗口的大小(长 * 宽)
root.geometry('450x160') 
def do1():
    pp=os.path.join(os.path.abspath('.'),r"xlsx\预估报告编号.xlsx")
    p2=os.path.abspath('.')
    data_n="im2006"
    us="user"#"user"
    pwd="7940"#"7940"
    host="192.168.1.3"#"192.168.1.3"
    ch="utf8"
    mu=["fd1"]
    tablename="reports"
    searchlist=["district","fd3","fd1","buildingname","fdzq","fd4","fd18","fd15","fd20","fd21","fd10","fd37","fd38","fd16", "landfeature","credentialsno"]
    mm=yugum()
    mm.do(pp,p2,data_n,us,pwd,host,ch,mu,tablename,searchlist)


Label(root, text='', font=('宋体', 2), width=5, height=15).grid(row=0,column=2)
Label(root, text='', font=('宋体', 2), width=95, height=4).grid(row=1,column=0)
Button(root,text="确定",command=do1,font=('宋体', 18)).grid(row=1,column=1)
Label(root, text='', font=('宋体', 2), width=5, height=4).grid(row=1,column=2)
Label(root, text='', font=('宋体', 2), width=5, height=4).grid(row=0,column=3)
root.mainloop()