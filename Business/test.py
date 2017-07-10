#coding=utf-8

from checkinNode import checkinNode,startcheckin
import time
import threading
import os
import signal

def my(pid):
    time.sleep(120)
    os.kill(pid,signal.SIGKILL)

if __name__=='__main__':
    s=startcheckin()
    pid = os.getpid()
    thread = threading.Thread(target=s.remove, args=())
    thread2=threading.Thread(target=my,args=(pid,))
    thread.start()
    thread2.start()
    key={'StuID':'201416920106','ClassID':'软件工程1401','Prove':'adadadasdasdasdasd'}
    key2={'StuID':'201416920215','ClassID':'软件工程1402','Prove':'asd'}
    key3={'StuID':'201416920105','ClassID':'软件工程1401','Prove':'asdxcxz'}

    while True:
        c=checkinNode()
        c.creatauto()
        c.auto.receive()
        c.auto.receive(key2)
        c.auto.receive(key3)
        s.append(c)

    # c.creatauto()
    #d.creatauto()

