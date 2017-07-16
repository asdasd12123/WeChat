#coding=utf-8
import time
import ConfigParser
import re
import threading

class basebusiness(object):


    def __init__(self):
        self.list=[]
        self.t=None

    def timeCheck(self):
        if self.list == []:
            print "考勤队列为空!"
        else:
            self.stopCheckIn()

    def startCheckTime(self):
        self.t = threading.Timer(10, self.timeCheck)
        self.t.start()

    def stopCheckIn(self):
        if self.t != None:  #计时器还未被销毁，但是教师已经从列表中踢出，或者说根本没有计时器，那么说明刚刚开始签到
            if len(self.list) >1:  # 列表中存在其他的教师班级签到或者说正在计时的时候，调用stop方法，这个时候要重新计时时间为下课时间减去上课时间
                localtime = time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
                timedev=100*60-(localtime-self.list[1].start_time)
                self.list.pop(0)  # 计算后将教师踢出队列
                self.t.cancel()
                self.t = threading.Timer(timedev, self.timeCheck)
                self.t.start()
            elif len(self.list)==1:
                self.list.pop(0)
                print "考勤队列为空!"
            else:
                print '当前队列已经没有教师'
                self.t=None
        else:
            self.t = threading.Timer(20, self.timeCheck)
            self.t.start()