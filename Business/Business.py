#coding=utf-8
from checkinNode import checkinNode
from basebusiness import basebusiness
from DataProcess.DataProcess import DataProcess
import time
from studentfunction import student_fun
from maintain import maintain
from view import view
from Auxiliaryfunction import Auxiliaryfunction


class business(basebusiness):

    def __init__(self):

        basebusiness.__init__(self)

        self.stufunct=student_fun()

        self.maintain=maintain()

        self.view=view()


    def stuinfotest(self,key):

        stuinfo = DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/studentInfo.csv', {'WeChatID':key})).run()

        if not stuinfo:
            print '学生微信不存在请检查您的输入信息!'
            return False

        return stuinfo[0]


    def teachertest(self,key): #输入微信号和班级　进行验证
        teacherinfo = DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/teacherInfo.csv', {'WeChatID': key})).run()

        if not teacherinfo:
            print '教师微信不存在请检查您的输入信息!'
            return False

        return teacherinfo[0]


    def autocheckin(self,key):

        for list in self.list:
            if list.key['ClassID']==key['ClassID']:
                return list.receive(key)
        print '当前没有与您有关的自动考勤窗口'
        return False

    def startrandom(self,key):
        teacherinfo= self.teachertest(key)
        if not teacherinfo:
            return False

        for list in self.list:
            if list.key['TeacherID'] == teacherinfo['TeacherID']:
                return list.startrandom()
        print '当前您没有开启一个自动考勤窗口无法开启随机考勤!'
        return False


    def startcheckin(self,key): #　教师微信号　学生班级号

        teacherinfo = DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/courseInfo.csv', {'ClassName': key['ClassID']})).run()

        if not teacherinfo:
            print '班级不存在请检查您的输入信息!'
            return False

        if self.list==[]:
            c=checkinNode(key)
            if not c.startauto():
                return False
            self.list.append(c)
            print '发起考勤成功!'
            self.startCheckTime()
            return True


        for index in range(1,len(self.list)):
            if self.list[index].key['TeacherID']==key['TeacherID']:
                print '您已经对班级: %s 开启自动考勤　无法再次开启' %(self.list[index].key['ClassID'])
                return False
            if self.list[index].key['ClassID']==key['ClassID']:
                print '班级: %s 正在被老师: %s 考勤　无法对此班级发起考勤!' %(self.list[index].key['TeacherID'])
                return False

        localtime = time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
        if localtime>self.list[0].end_time:
            c = checkinNode(key)
            if not c.startauto():
                return False
            self.list.append(c)
            print '发起考勤成功!'
            self.stopCheckIn()
            return True

        else:
            if self.list[0].key['TeacherID']==key['TeacherID']:
                print '您已经对班级: %s 开启自动考勤　无法再次开启' %(self.list[0].key['ClassID'])
                return False
            if self.list[0].key['ClassID']==key['ClassID']:
                print '班级: %s 正在被老师: %s 考勤　无法对此班级发起考勤!' %(self.list[0].key['TeacherID'])
                return False
            c = checkinNode(key)
            if not c.startauto():
                return False
            print '发起考勤成功!'
            self.list.append(c)
            return True



    def randomcheckin(self,key):

        for list in self.list:
            if list.key['ClassID'] == key['ClassID']:
                for info in list.random_info:
                    if info['StuID']==key['StuID']:
                        return list.receive(key)
        print '没有与您有关的随机考勤窗口!'
        return False


    def mancheckin(self,key):
        key = self.teachertest(key)
        if not key:
            return False

        for index in range(len(self.list)):
            if self.list[index].key['TeacherID'] == key['TeacherID']:
                print '您已经对班级: %s 开启自动考勤　无法再次开启' % (self.list[index].key['ClassID'])
                return False
            if self.list[index].key['ClassID'] == key['ClassID']:
                print '班级: %s 正在被老师: %s 考勤　无法对此班级发起考勤!' %(self.list[index].key['TeacherID'])
                return False


if __name__=='__main__':
   b=business()
   b.is_canStartchecnin({'WeChatID':'wonka80','ClassName':"软件工程1401"})
   b.is_canStartchecnin({'WeChatID':'wonka80','ClassName':"软件工程1401"})
   print b.is_can_autocheckin({'WeChatID':'asdasda'})
