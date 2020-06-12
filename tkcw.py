from tkinter import *
from  tkinter.filedialog import *
from tkinter.messagebox import *
from caiwu import update
root = Tk()

root.title('My Window')
 
# 第3步，设定窗口的大小(长 * 宽)
root.geometry('450x160') 

path=StringVar()
Label(root, text='选择文件:', font=('宋体', 15), width=10, height=4).grid(row=0,column=0)
en=Entry(root,width=30,textvariable=path)
en.grid(row=0,column=1)
Label(root, text='', font=('宋体', 2), width=5, height=4).grid(row=0,column=2)
en['state'] = 'readonly'


def choose():
    print(path.get())
    filename=askopenfilename(filetypes=[("Excel","*.xls?")])
    #path.set(filename)
    path.set(filename)

def update1():
    fileurl=path.get()
    try:
        dan="im2006"
        whl=['fd1','fd33','fd34','checkno','fd35','fd36']
        up=update(dan,fileurl,whl)
        up.conn()
        showinfo(title="提示", message="成功")
    except Exception as e:
        showinfo(title="提示", message="出错")


Button(root,text="选择",command=choose,font=('宋体', 13,'bold')).grid(row=0,column=3)
Button(root,text="确定",command=update1,font=('宋体', 18)).grid(row=1,column=1)

root.mainloop()