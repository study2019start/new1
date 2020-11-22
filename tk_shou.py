import tkinter as tk
from  tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from whq import he
root = tk.Tk()

root.title('王海琼')
 
# 第3步，设定窗口的大小(长 * 宽)
root.geometry('450x450') 
def choose():
    print(path.get())
    filename=askopenfilename(filetypes=[("Excel","*.xls?")])
    #path.set(filename)
    path.set(filename)

def choose2():
    print(path2.get())
    filename=askopenfilename(filetypes=[("Excel","*.xls?")])
    #path.set(filename)
    path2.set(filename)

def modelchu():
    filepath=path.get().replace("/","\\")
    if filepath: 
        #try:
        slist2=['fd1','fd26']
        where=[{"category":"G"}]
        slist=['fd1','fd3','fd7','fd10','fd20','fd26']
        host='192.168.1.3'
        database='im2006'
        m=he(slist,False,filepath,host,database,"reports","user","7940",where)
        v.set(m.model())
        showinfo(title="提示", message="成功")
        #except Exception as e:
            #showinfo(title="提示", message="出错")

def show():
    filepath=path2.get().replace("/","\\")
    if filepath:
        #try:
        where=[{"category":"G"}]
        slist2=['fd1','fd26']
        slist=['fd1','fd3','fd7','fd10','fd20','fd26']
        host='192.168.1.3'
        database='im2006'
        m=he( False,slist2,filepath,host,database,"reports","user","7940",where)
        m.model2()
            
        #except Exception as e:
            #showinfo(title="提示", message="出错")

path=tk.StringVar()
path2=tk.StringVar()
v = tk.StringVar()
tk.Label(root, text='选择文件:', font=('宋体', 15), width=10, height=4).grid(row=0,column=0)
en=tk.Entry(root,width=30,textvariable=path)
en.grid(row=0,column=1)
tk.Label(root, text='', font=('宋体', 2), width=5, height=4).grid(row=0,column=2)
en['state'] = 'readonly'
tk.Label(root, text='未找出个数:', font=('宋体', 13), width=10, height=4).grid(row=1,column=0)
tk.Entry(root,width=20,textvariable=v).grid(row=1,column=1)

tk.Label(root, text='选择数据文件:', font=('宋体', 15), height=4).grid(row=3,column=0)
en1=tk.Entry(root,width=30,textvariable=path2)
en1.grid(row=3,column=1)
en1['state'] = 'readonly'
tk.Label(root, text='', font=('宋体', 2), width=5, height=4).grid(row=3,column=2)

tk.Button(root,text="选择",command=choose,font=('宋体', 13,'bold')).grid(row=0,column=3)
tk.Button(root,text="选择",command=choose2,font=('宋体', 13,'bold')).grid(row=3,column=3)
tk.Button(root,text="确定",command=modelchu,font=('宋体', 15)).grid(row=2,column=1)
tk.Button(root,text="处理数据",command=show,font=('宋体', 15)).grid(row=5,column=1)





root.mainloop()