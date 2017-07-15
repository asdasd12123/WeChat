#coding=utf-8
from abc import ABCMeta, abstractmethod
import ConfigParser
import re
from DataProcess.DataProcess import DataProcess
import time
import datetime

class baseattendance(object):

    __metaclass__ = ABCMeta

    def __init__(self):  #主键就是课程号加上班级号　若不存在则无法签到
        self.auto = None
        self.random = None
        self.key =self.getkey()
        self.filename = None
        cf = ConfigParser.ConfigParser()
        cf.read('../InData/settings.ini')
        info = map((lambda x: re.split('-|:', x[1])), cf.items('sectime'))
        self.Timeinfo = map((lambda x: [int(x[0]) * 3600 + int(x[1]) * 60, int(x[2]) * 3600 + int(x[3]) * 60]), info)

    def getTime(self):
        localtime= time.localtime()[3]*3600+time.localtime()[4]*60+time.localtime()[5]
        timeinfo={}
        for Time in self.Timeinfo:
            if localtime >= Time[0]-600 and localtime <=Time[1]-59:
                timeinfo['endclass']=Time[1]-localtime
                timeinfo['num']=self.Timeinfo.index(Time)+1
                timeinfo['nowbetweenstart']=localtime-Time[0] if (localtime -Time[0])>=0 else Time[0]-localtime
        return timeinfo



