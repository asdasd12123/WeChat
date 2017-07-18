#coding=utf-8
import time
import threading

class basebusiness(object):

    def __init__(self):
        self.list=[]
        self.t=None

    def timeCheck(self):
        if self.list == []:
            return
        else:
            self.stopCheckIn()

    def startCheckTime(self):
        self.t = threading.Timer(50, self.timeCheck)
        self.t.start()

    def stopCheckIn(self):
        if len(self.list) >1:  # 列表中存在其他的教师班级签到或者说正在计时的时候，调用stop方法，这个时候要重新计时时间为下课时间减去上课时间
            localtime = time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
            #timedev=100*60-(localtime-self.list[1].start_time)
            timedev=50
            self.list.pop(0)  # 计算后将教师踢出队列
            print 'one pop'
            self.t.cancel()
            self.t = threading.Timer(timedev, self.timeCheck)
            self.t.start()
        else:
            self.list.pop(0)
            print 'one pop'
