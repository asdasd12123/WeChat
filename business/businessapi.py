# coding=utf-8
import time
import copy
from checkinnode import CheckInNode
from basebusiness import BaseBusiness
from dataoperation.manage import DataManage
from stufunction import StudentFun
from maintain import Maintain
from view import View
from importfile import ImportFile


class Business(BaseBusiness):

    def __init__(self):
        BaseBusiness.__init__(self)

        self.stufunct = StudentFun()

        self.maintain = Maintain()

        self.view = View()

        self.import_file = ImportFile()

    @staticmethod
    def stu_info_test(key):

        stu_info = DataManage(DataManage.target_info, args=('../InData/studentInfo.csv', {'WeChatID': key})).run()

        if not stu_info:
            print '学生微信不存在请检查您的输入信息!'
            return False

        return stu_info[0]

    @staticmethod
    def teacher_test(key):  # 输入微信号和班级　进行验证
        teacher_info = DataManage(DataManage.target_info, args=('../InData/teacherInfo.csv', {'WeChatID': key})).run()

        if not teacher_info:
            print '教师微信不存在请检查您的输入信息!'
            return False

        return teacher_info[0]

    def insert_leave(self, key):
        key = copy.deepcopy(key)
        for line in self.list:
            if line.key['ClassID'] == key['ClassID']:
                key['TeacherID'] = line.key['TeacherID']
                return self.stufunct.insert_leave_record(key)
        return False

    def auto_check_in(self, key):
        for line in self.list:
            if line.key['ClassID'] == key['ClassID']:
                return line.receive(key)
        print '当前没有与您有关的自动考勤窗口'
        return False

    def tips(self, key, info=''):
        count = 0
        for line in self.list:
            if line.key['ClassID'] == key['ClassID']:  # 1
                if info:
                    print '当前工号为:%s 的老师正在向您的班级发起自动考勤!' %(line.key['TeacherID'], )
                count += 1
                if not line.random_info:
                    return count
                for info in line.random_info:
                    if info['StuID'] == key['StuID']:  # 2
                        if info:
                            print '当前存在和您有关的抽点考勤!'
                        count += 2
        return count

    def start_random(self, key):

        for line in self.list:
            if line.key['TeacherID'] == key['TeacherID']:
                return line.start_random()
        print '当前您没有开启一个自动考勤窗口无法开启随机考勤!'
        return False

    @staticmethod
    def dis_info(key):
        info = DataManage(DataManage.target_info, args=('../InData/courseInfo.csv',)).run()
        class_list = list()
        for _class in info:
            if _class['TeacherID'] == key['TeacherID']:
                class_info = dict()
                class_info['CourseName'] = _class['CourseName']
                class_info['ClassName'] = _class['ClassName']
                class_list.append(class_info)

        if not class_list:
            return False
        else:
            print '您的课头列表信息如下: '
            for _class in class_list:
                print '课程名 : %s 班级名: %s ' % (_class['CourseName'], _class['ClassName'])
            return True

    @staticmethod
    def __time_check(check_node):  # 判断是否下课
        localtime = time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
        if localtime > check_node.end_time:
            return False
        return True

    def start_check_in(self, key):  # 教师微信号　学生班级号
        key = copy.deepcopy(key)
        teacher_info = DataManage(DataManage.target_info, args=('../InData/courseInfo.csv',
                                                                {'TeacherID': key['TeacherID'],
                                                                 'ClassName': key['ClassID']})).run()

        if not teacher_info:
            print '班级不存在或者该班级不在您的课头列表之中,请检查您的输入信息后重试!'
            return False

        c = CheckInNode(key)

        for index in self.list:
            if index.key['TeacherID'] == key['TeacherID']:
                if self.__time_check(index):
                    print '您已经对班级:%s开启自动考勤无法再次开启' % (index.key['ClassID'])
                    return False
                else:
                    if self.list.index(index) == 0:
                        self.stop_check_in()
                    else:
                        self.list.remove(index)

        for index in self.list:
            if index.key['ClassID'] == key['ClassID']:
                if self.__time_check(index):
                    print '班级:%s正在被老师:%s考勤,无法对此班级发起考勤!' % (index.key['ClassID'], index.key['TeacherID'])
                    return False
                else:
                    if self.list.index(index) == 0:
                        self.stop_check_in()
                    else:
                        self.list.remove(index)

        if not c.start_auto():
            return False

        if not self.list:
            self.list.append(c)
            self.start_check_time()
        else:
            self.list.append(c)

        print '发起考勤成功!'
        return True

    def random_check_in(self, key):
        for line in self.list:
            if line.key['ClassID'] == key['ClassID']:
                for info in line.random_info:
                    if info['StuID'] == key['StuID']:
                        return line.receive(key)
        print '没有与您有关的随机考勤窗口!'
        return False

    def man_check_in(self, key):
        if self.can_statistics(key):
            return CheckInNode(key).man_check_in()

    def can_statistics(self,key):
        for line in self.list:
            if line.key['TeacherID'] == key['TeacherID']:
                print '当前您开启了对班级%s的课程，无法开启统计功能!' % (line.key['ClassID'], )
                return False
        return True

