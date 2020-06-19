from tkinter import *
from  tkinter.filedialog import *
from tkinter.messagebox import *
from whq import he
root = Tk()

root.title('王海琼')
 
# 第3步，设定窗口的大小(长 * 宽)
root.geometry('450x450') 

path=StringVar()
v = StringVar()
Label(root, text='选择文件:', font=('宋体', 15), width=10, height=4).grid(row=0,column=0)
en=Entry(root,width=30,textvariable=path)
en.grid(row=0,column=1)
Label(root, text='', font=('宋体', 2), width=5, height=4).grid(row=0,column=2)
en['state'] = 'readonly'
Label(root, text='未找出个数:', font=('宋体', 13), width=10, height=4).grid(row=1,column=0)
Entry(root,width=20,textvariable=v).grid(row=1,column=1)

def choose():
    print(path.get())
    filename=askopenfilename(filetypes=[("Excel","*.xls?")])
    #path.set(filename)
    path.set(filename)

def update1():
    filepath=path.get()
    try:
        if filepath !="":
            where=[{"category":"G"}]
            slist=['fd1','fd3','fd7','fd10','fd20','fd26']
            host='192.168.1.3'
            database='im2006'
            m=he(slist,filepath,host,database,"reports","user","7940",where)
            v.set(m.model())
            showinfo(title="提示", message="成功")
    except Exception as e:
        showinfo(title="提示", message="出错")


Button(root,text="选择",command=choose,font=('宋体', 13,'bold')).grid(row=0,column=3)
Button(root,text="确定",command=update1,font=('宋体', 18)).grid(row=2,column=1)

root.mainloop()