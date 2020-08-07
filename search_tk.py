import tkinter as tk
from  tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from stdframe import firstsou
import re
import multiprocessing
re1=r"\d{1,2}"
def choose():
    
    filename=askopenfilename(filetypes=[("Excel","*.xls?")])
    #path.set(filename)
    path.set(filename)


def update1():
    filename=path.get().replace("/","\\")
    sname=sheetname.get()
    ncl=ncol.get()
    if filename!="" and sname!="" and  re.match(re1,ncl):
        try:
            
            up=firstsou(filename,int(ncl),sname)
            up.run()
            showinfo(title="提示", message="成功")
        except Exception as e:
            showinfo(title="提示", message="出错")
    else:
        showinfo(title="提示", message="出错")


if __name__ == "__main__":
    root = tk.Tk()
    multiprocessing.freeze_support()
    root.title('My Window')
    
    # 第3步，设定窗口的大小(长 * 宽)
    root.geometry('550x260') 

    path=tk.StringVar()
    sheetname=tk.StringVar()
    ncol=tk.StringVar()
    tk.Label(root, text='选择文件:', font=('宋体', 15), width=10, height=2).grid(row=0,column=0)
    en=tk.Entry(root,width=30,textvariable=path)
    en.grid(row=0,column=1)
    tk.Label(root, text='', font=('宋体', 2), width=5, height=2).grid(row=0,column=2)
    en['state'] = 'readonly'

    tk.Label(root, text='表名:', font=('宋体', 15), width=10, height=2).grid(row=1,column=0)
    tk.Entry(root,width=15,textvariable=sheetname).grid(row=1,column=1)

    tk.Label(root, text='所在列（数字）:', font=('宋体', 15), width=18, height=2).grid(row=2,column=0)
    tk.Entry(root,width=15,textvariable=ncol).grid(row=2,column=1)
    tk.Button(root,text="选择",command=choose,font=('宋体', 13,'bold')).grid(row=0,column=3)
    tk.Button(root,text="确定",command=update1,font=('宋体', 18)).grid(row=3,column=1)

    root.mainloop()

    