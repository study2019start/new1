import tkinter as tk
from  tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from quhao import mysql_model
import re
root = tk.Tk()

root.title('取号')
 
# 第3步，设定窗口的大小( 宽* 长)
root.geometry('250x250') 

v1=tk.StringVar()
v2=tk.StringVar()
v3 = tk.StringVar()
v4 =tk.StringVar()
v1.set(20)
v2.set(20)
v3.set(20)
v4.set(20)

tk.Label(root, text='王海琼:', font=('宋体', 15), width=10, height=2).grid(row=0,column=0)
tk.Label(root, text='赵晓芸:', font=('宋体', 15), width=10, height=2).grid(row=1,column=0)
tk.Label(root, text='马晓迎:', font=('宋体', 15), width=10, height=2).grid(row=2,column=0)
tk.Label(root, text='朱留清:', font=('宋体', 15), width=10, height=2).grid(row=3,column=0)
en=tk.Entry(root,width=10,textvariable=v1)
en.grid(row=0,column=1)
en=tk.Entry(root,width=10,textvariable=v2)
en.grid(row=1,column=1)
en=tk.Entry(root,width=10,textvariable=v3)
en.grid(row=2,column=1)
en=tk.Entry(root,width=10,textvariable=v4)
en.grid(row=3,column=1)
def quhao():
    name=["王海琼","赵晓芸","马晓迎","朱留清"]
    
    gl=globals()

    for i in range(1,5):
        num=gl['v'+str(i)].get()
        if num=="":
            f=mysql_model("im2006",20,name[i-1],"user","7940","192.168.1.3","gbk")
            f.quhao()
        else:
            if re.match(r"^\d{1,2}$",str(num)):
                if int(num)>40:
                    num=40
                f=mysql_model("im2006",int(num),name[i-1],"user","7940","192.168.1.3","gbk")
                f.quhao()
    showinfo(title="提示", message="成功")


tk.Button(root,text="确定",command=quhao,font=('宋体', 15)).grid(row=4,column=1)
root.mainloop()
