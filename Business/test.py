#coding=utf-8

from checkinNode import checkinNode,startcheckin
import time
from studentfunction import studentcheckin
import threading
import os
import signal

def my(pid):
    time.sleep(60)
    signal.SIGKILL(pid)

if __name__=='__main__':
    s=startcheckin()
    pid = os.getpid()
    thread = threading.Thread(target=s.remove, args=())
    thread2 = threading.Thread(target=my, args=(pid,))
    thread.start()
    thread2.start()

    while True:
        c=checkinNode()
        c.creatauto()
        c.creatrandom()
        c.auto.receive(studentcheckin().checkinauto())
        c.random.receive(studentcheckin().checkinrandom())
        s.append(c)
        time.sleep(8)