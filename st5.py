import asyncio
import requests
import time
import threading
import ctypes
import inspect




async def request(v):
    #url = 'https://www.baidu.com'
    #status = requests.get(url)
    await asyncio.sleep(v)
    print("OK!----------"+str(time.ctime()))

async def request3(v):
    #url = 'https://www.baidu.com'
    #status = requests.get(url)
    await asyncio.sleep(v)
    print("OK!----------"+str(time.ctime()))
   

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

async def request1(v):
    #url = 'https://www.baidu.com'
    #status = requests.get(url)
    await asyncio.sleep(v)
    print("OK11!----------"+str(time.ctime()))
    #return status
print(time.ctime())
i=0
ii=1
coroutine1=request3(2)
new_loop = asyncio.new_event_loop()
t = threading.Thread(target=start_loop,args=(new_loop,))   #通过当前线程开启新的线程去启动事件循环

#coroutine = request()
t.setDaemon(True)
t.start()
 
asyncio.run_coroutine_threadsafe(coroutine1,new_loop)
tasks = [asyncio.ensure_future(request(i)) for i in range(5)]
tasks1 = [asyncio.ensure_future(request1(ii)) for ii in range(1,7)]
 
loop = asyncio.get_event_loop()
loop1 = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))
loop1.run_until_complete(asyncio.wait(tasks1))




print(time.ctime())
print(t.isAlive())
time.sleep(1)