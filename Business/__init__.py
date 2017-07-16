#conding=utf-8
import threading

def pr():
    print 'asd'

t=threading.Timer(2,pr)
t.start()
t.cancel()
print t