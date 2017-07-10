#coding=utf-8

from checkinNode import checkinNode,startcheckin
import time
from studentfunction import studentcheckin
import threading
import os


if __name__=='__main__':
    s=startcheckin()
    pid = os.getpid()
    thread = threading.Thread(target=s.remove, args=())
    thread.start()
    key={'StuID':'201416920106','ClassID':'软件工程1401','Prove':'adadadasdasdasdasd'}
    key2={'StuID':'201416920215','ClassID':'软件工程1402','Prove':'asd'}
    key3={'StuID':'201416920105','ClassID':'软件工程1401','Prove':'asdxcxz'}
    c=checkinNode()
    if not s.append(c):
        print 'c 已经存在'
        exit(0)
    c.creatauto()
    # c.creatauto()
    #d.creatauto()
    time.sleep(3)
    #c.auto.receive(key)
    #c.auto.receive(key2)
    #c.auto.receive(key3)
    time.sleep(10)