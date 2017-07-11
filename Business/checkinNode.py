#coding=utf-8
from startcheckin import autothread,randomthread
import time
import datetime
from Auxiliaryfunction import Auxiliaryfunction
from basicattendance import baseattendance
from DataProcess.Update import Update
from DataProcess.Query import Query
import random

class checkinNode(baseattendance):


    def creatauto(self):
        if self.auto :
            print 'There are currently automatic attendance Windows that cannot be created again !'
            return False

        Time=self.getTime()
        if not Time:
            print 'At this stage can not open the check, please refer to the start of the standard of attendance!'
            #return False

        self.write_seq()
        rule=Auxiliaryfunction().read({'TeacherID':self.key['TeacherID']})
        studentlist = Query.QueryObjectInfo('../InData/studentInfo.csv', {'ClassID': self.key['ClassName']})
        while True:
            print '您采用的考勤规则为 :'+str(rule)
            print '当前课程名称 : %s 当前考勤班级 %s 当前被考勤人数 %d 当前考勤类型 %s ' %(self.key['CourseName'],self.key['ClassName'],
                    len(studentlist),'Auto')
            print '当前考勤的有效时间为 %s 分钟 当前距离考勤结束还有%d 分钟' %(rule['autolate'],10000)
            result=raw_input('确定开始考勤输入 \'yes\'  退出请输入 \'exit\' ')
            if result=='yes':
                break
            elif result=='exit':
                return False
            else:
                time.sleep(1)

        self.write_detail_head(['StuID', 'checkstartTime','checkTime', 'ProofPath', 'checkinType', 'IsSucc', 'checkinResult'])
        #self.auto=autothread(studentlist,self.filename)
        #self.auto.start(10)
        #self.auto.status=True
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
        stulist = []
        studentlist = Query.QueryObjectInfo('../InData/studentInfo.csv', {'ClassID': self.key['ClassName']})

        while True:
            num=raw_input('Please enter a percentage of the spot checks!')
            try:
                num=float(num)
            except TypeError and ValueError:
                print 'You have entered an invalid format. Please enter a floating point number!'
                continue

            if num<=0 or num>100 or int(len(studentlist) * num / 100)==0:
                print 'Number exceeds or below standard. Please re-enter!'
                time.sleep(1)
            else:
                num = int(len(studentlist) * num / 100)
                print 'You have a total of %d people selected this time!' %(num)
                break

        while len(stulist)!=num:
            index=random.randint(0,len(studentlist)-1)
            if studentlist[index] not in stulist:
                stulist.append(studentlist[index])
        return stulist


    def random_new_start(self):
        studentlist=self.randomstulist()
        self.random.new_start(studentlist,self.filename)


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


    def Realtimeresults(self):
        '''查看实时考勤结果'''
        pass


class startcheckin(object):
    def __init__(self):
        self.list=[]

    def remove(self):
        while True:
            for line in self.list:
                if line.auto and not line.auto.status or not line.auto:
                    if line.random and not line.random.status or not line.random:
                        print line.key
                        self.list.remove(line)
                        time.sleep(1)

    def append(self,argu):
        for item in self.list:
            if not (argu.key['TeacherID']!=item.key['TeacherID'] and argu.key['ClassID'] !=item.key['TeacherID']):
                print 'Attendance object is illegal or already exists！'
                return False
        self.list.append(argu)
        return True


if __name__=='__main__':
    checkinNode().creatauto()













