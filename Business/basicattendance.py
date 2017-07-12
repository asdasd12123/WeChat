#coding=utf-8
from abc import ABCMeta, abstractmethod
import ConfigParser
import re
from DataProcess.DataProcess import DataProcess
import time
import datetime

class baseattendance(object):

    __metaclass__ = ABCMeta

    def __init__(self):  # 主键就是课程号加上班级号　若不存在则无法签到
        self.auto = None
        self.random = None
        self.key =self.getkey()
        self.filename = None
        cf = ConfigParser.ConfigParser()
        cf.read('../InData/settings.ini')
        info = map((lambda x: re.split('-|:', x[1])), cf.items('sectime'))
        self.Timeinfo = map((lambda x: [int(x[0]) * 3600 + int(x[1]) * 60, int(x[2]) * 3600 + int(x[3]) * 60]), info)

    def getkey(self):
        checkinkey = {}
        info={}
        info['WeChatID'] = raw_input('Please enter the WeChatID you want to check in!\n')
        if not DataProcess(target=DataProcess.QueryObjectInfo,args=('',info)).run():
            print 'The teacher does not exist. Please check your input!'
            return False
        checkinkey['TeacherID'] = DataProcess(target=DataProcess.QueryObjectInfo,args=('', info)).run()[0][0]['TeacherID']

        checkinkey['CourseName'] = raw_input('Please input your CourseName!\n')
        if not DataProcess(target=DataProcess.QueryObjectInfo,args=('', checkinkey)).run():
            print 'The Course does not exist Or in your class head. Please check your input!'
            return False

        checkinkey['ClassName'] = raw_input('Please input your className!\n')
        if not DataProcess(target=DataProcess.QueryObjectInfo,args=('', checkinkey)).run():
            print 'This class does not exist.Please check your input'
            return False


        return checkinkey

    def getseqnum(self):
        seqinfo=DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/seq.csv',{'TeacherID':'2004633','ClassName':'软件工程1401'})).run()
        if not seqinfo:
            return '1'
        return str(int(seqinfo[-1]['SeqID'])+1)


    def getTime(self):
        localtime= time.localtime()[3]*3600+time.localtime()[4]*60+time.localtime()[5]
        timeinfo={}
        for Time in self.Timeinfo:
            if localtime >= Time[0]-600 and localtime <=Time[1]-59:
                timeinfo['endclass']=Time[1]-localtime
                timeinfo['num']=self.Timeinfo.index(Time)+1
                timeinfo['nowbetweenstart']=localtime-Time[0] if (localtime -Time[0])>=0 else Time[0]-localtime
        return timeinfo

    def write_seq(self):
        if not DataProcess(target=DataProcess.QueryObjectKey,args=('../InData/seq.csv')).run():
            print 'The system creates the seq.csv file automatically！'
        return DataProcess(target=DataProcess.update,args=('../InData/seq.csv', 'a', [self.get_seqinfo()])).run()


    def get_seqinfo(self):
        seqinfo = {'TeacherID': self.key['TeacherID'], 'ClassName': self.key['ClassName']}
        seqnum = self.getseqnum()
        self.filename = '../InData/'+self.key['TeacherID'] + '_' + self.key['ClassName'] + '_' + seqnum + '.csv'
        seqinfo['StartTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        seqinfo['SeqID'] = self.getseqnum()
        return seqinfo
