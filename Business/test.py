#coding=utf-8

import checkinNode

from DataProcess.Query import Query
import time
import threading
import os
import signal

def my(pid):
    time.sleep(30)
    signal.SIGKILL(pid)

if __name__=='__main__':
    s=checkinNode.startcheckin()
    pid = os.getpid()
    thread = threading.Thread(target=s.remove, args=(s,))
    thread2 = threading.Thread(target=my, args=(pid,))
    thread.start()
    thread2.start()

    while True:
        c=checkinNode()

        c.creatauto()
        c.creatrandom()

        c.auto.receive()
        s.append(c)
    #time.sleep(8)