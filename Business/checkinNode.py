#coding=utf-8
from startcheckin import autothread,randomthread
import time
import ConfigParser
import re
from DataProcess.Update import Update
from DataProcess.Query import Query
import datetime
import random

class checkinNode(object):
    def __init__(self):  #主键就是课程号加上班级号　若不存在则无法签到
        self.auto=None
        self.random=None
        self.key=None
        self.filename=None
        cf = ConfigParser.ConfigParser()
        cf.read('../InData/settings.ini')
        info = map((lambda x: re.split('-|:', x[1])), cf.items('sectime'))
        self.Timeinfo = map((lambda x: [int(x[0]) * 3600 + int(x[1]) * 60, int(x[2]) * 3600 + int(x[3]) * 60]), info)


    def getkey(self):
        checkinkey = {}
        checkinkey['TeacherID'] = raw_input('Please enter the TeacherID you want to check in!\n')
        if not Query.QueryObjectInfo('', checkinkey):
            print 'The teacher does not exist. Please check your input!'
            return False

        checkinkey['CourseName'] = raw_input('Please input your CourseName!\n')
        if not Query.QueryObjectInfo('', checkinkey):
            print 'The Course does not exist Or in your class head. Please check your input!'
            return False

        checkinkey['ClassName'] = raw_input('Please input your className!\n')
        if not Query.QueryObjectInfo('', checkinkey):
            print 'This class does not exist.Please check your input'
            return False

        return checkinkey


    def getseqnum(self):
        seqnum=Query.QueryObjectInfo('../InData/seq',self.key)['seqID']
        if not seqnum:
            return '1'
        return str(int(seqnum)+1)


    def creatauto(self):
        if self.auto or self.auto.status:
            print 'There are currently automatic attendance Windows that cannot be created again !'
            return False

        Time=self.getTime()
        if not Time:
            print 'At this stage can not open the check, please refer to the start of the standard of attendance!'
        return False

        seqinfo = {'TeacherID': self.key['TeacherID'], 'ClassName': self.key['ClassName']}
        seqnum = self.getseqnum(seqinfo)
        self.filename = self.key['TeacherID'] + '_' + self.key['ClassName'] + '_' + seqnum + '.csv'
        seqinfo['StartTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        seqinfo = seqnum

        Update.update(filename, 'a', seqinfo)
        studentlist=Query.QueryObjectInfo('../InData/studentInfo.csv',{'ClassID':self.key['ClassName']})
        self.auto=autothread(studentlist,self.filename)
        self.auto.start(Time)
        self.auto.status=True
        return True


    def creatrandom(self):
        if not self.auto or not  self.auto.status:
            print 'Currently the attendance node does not open automatic attendance is unable to open random check on work attendance !'
            return False
        if self.random:
            print 'There are currently automatic attendance Windows that cannot be created again !'
            return False

        studentlist =self.randomstulist()
        self.random=randomthread(studentlist,self.filename)
        self.random.start()
        self.random.status=True
        return True


    def randomstulist(self):
        num=input('Please enter a percentage of the spot checks!')
        stulist=set()
        studentlist = Query.QueryObjectInfo('../InData/studentInfo.csv', {'ClassID': self.key['ClassName']})
        if type(num)!=float or num<=0 or num > 1:
            print 'The percentage currently entered is illegal！'
            return None

        num=int(len(studentlist)*num)
        while len(stulist)==num:
            index=random.randint(0,num-1)
            stulist.add(studentlist[index])

        return list(stulist)


    def random_new_start(self):
        studentlist=self.randomstulist()
        self.random.newstart(self,studentlist,self.filename)


    def autoreceive(self,student):
        if not self.auto or not self.auto.status:
            print 'The current automatic attendance window is unable to receive information!'
            return False
        return self.auto.receive(student)


    def randomreceive(self,student):
        if not self.random or not self.random.status:
            print 'The current random window cannot receive information'
            return False
        return self.random.reveive(student)



    def creatManualAttendance(self,studentinfolist,filename):
        return Update.update(filename,'w',studentinfolist)


    def getTime(self):
        localtime= time.localtime()[3]*3600+time.localtime()[4]*60+time.localtime()[5]
        timeinfo={}
        for Time in self.Timeinfo:
            if localtime >= Time[0]-60*10 and localtime <=Time[1]-60*3:
                timeinfo['endclass']=Time[1]-localtime
        return timeinfo


    def Realtimeresults(self):
        '''查看实时考勤结果'''
        pass


class startcheckin(object):
    def __init__(self):
        self.list=[]

    def remove(self):
        while True:
            for line in self.list:
                if not line.auto.status and not line.random.status:
                    self.list.remove(line)
                    time.sleep(1)

    def append(self,argu):
        for (key,item) in self.list:
            if not (argu['TeacherID']!=self.list['TeacherID'] and argu['ClassID'] !=self.list['TeacherID']):
                print 'Attendance object is illegal or already exists！'
                return False
        self.list.append(argu)
        return True