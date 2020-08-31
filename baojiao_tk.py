from tkinter import *
from  tkinter.filedialog import *
from tkinter.messagebox import *
from baojia import model
root = Tk()

root.title('Baojia')
 
# 第3步，设定窗口的大小(长 * 宽)
root.geometry('450x160') 

path=StringVar()
Label(root, text='选择文件:', font=('宋体', 15), width=10, height=4).grid(row=0,column=0)
en=Entry(root,width=30,textvariable=path)
en.grid(row=0,column=1)
Label(root, text='', font=('宋体', 2), width=5, height=4).grid(row=0,column=2)
en['state'] = 'readonly'

a=0
def choose():
    print(path.get())
    filename=askopenfilename(filetypes=[("Excel","*.xls?")])
    #path.set(filename)
    path.set(filename)

def update1():
    global a
    if a==0:
        a=1
        fileurl=path.get()
        try:
            inlist=["district","fd3","quoteprice","fd37","fd38","fd39","quotedate","quotedate_b","person"]
            d_n="im2006"
            table_n="price"
            h="192.168.1.3"
            u="user"
            pwd="7940"
            m=model(fileurl,"顾李青",inlist,d_n,table_n,h,u,pwd)
            m.msqlinset()
            a=0
    
            showinfo(title="提示", message="成功")
        except Exception as e:
            showinfo(title="提示", message="出错")


Button(root,text="选择",command=choose,font=('宋体', 13,'bold')).grid(row=0,column=3)
Button(root,text="确定",command=update1,font=('宋体', 18)).grid(row=1,column=1)

root.mainloop()