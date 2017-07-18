#coding=utf-8
from checkinNode import checkinNode
from basebusiness import basebusiness
from DataProcess.DataProcess import DataProcess
import time
from studentfunction import student_fun
from maintain import maintain
from view import view
from import_file import Import_file
import copy

class business(basebusiness):

    def __init__(self):
        basebusiness.__init__(self)

        self.stufunct=student_fun()

        self.maintain=maintain()

        self.view=view()

        self.import_file=Import_file()

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

    def tips(self,key):
        for list in self.list:
            if list.key['ClassID']==key['ClassID']:
                print '当前工号为:%s 的老师正在向您的班级发起自动考勤!' %(list.key['TeacherID'])
                for info in list.random_info:
                    if info['StuID']==key['StuID']:
                        print '当前存在和您有关的抽点考勤!'
                return True
        return False




    def startrandom(self,key):

        for list in self.list:
            if list.key['TeacherID'] == key['TeacherID']:
                return list.startrandom()
        print '当前您没有开启一个自动考勤窗口无法开启随机考勤!'
        return False

    def time_check(self,checknode): #判断是否下课
        localtime = time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
        if localtime>checknode.end_time:
            return False
        return True



    def startcheckin(self,key): #　教师微信号　学生班级号

        key=copy.deepcopy(key)
        teacherinfo = DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/courseInfo.csv', {'ClassName': key['ClassID']})).run()

        if not teacherinfo:
            print '班级不存在请检查您的输入信息!'
            return False

        c=checkinNode(key)
        for index in self.list:
            if index.key['TeacherID']==key['TeacherID']:
                if self.time_check(index):
                    print '您已经对班级:%s开启自动考勤无法再次开启' %(index.key['ClassID'])
                    return False
                else:
                    if self.list.index(index)==0:
                        self.stopCheckIn()
                    else:
                        self.list.remove(index)

        for index in self.list:
            if index.key['ClassID']==key['ClassID']:
                if self.time_check(index):
                    print '班级:%s正在被老师:%s考勤,无法对此班级发起考勤!' %(index.key['ClassID'],index.key['TeacherID'])
                    return False
                else:
                    if self.list.index(index)==0:
                        self.stopCheckIn()
                    else:
                        self.list.remove(index)

        if not c.startauto():
            return False

        if self.list == []:
            self.list.append(c)
            self.startCheckTime()
        else:
            self.list.append(c)

        print '发起考勤成功!'
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

        return checkinNode(key).manCheckin()


if __name__=='__main__':
   b=business()
   b.is_canStartchecnin({'WeChatID':'wonka80','ClassName':"软件工程1401"})
   b.is_canStartchecnin({'WeChatID':'wonka80','ClassName':"软件工程1401"})
   print b.is_can_autocheckin({'WeChatID':'asdasda'})
