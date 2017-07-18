#coding=utf-8
from Business.Business import business
import sys
import os


class SystemRun(object):

    def stuForm(self,key,list):
        while True:
            print "*************欢迎进入学生模拟控制菜单******************"
            print "*****************1.在线请假*************************"
            print "*****************2.进行考勤*************************"
            print "*****************3.进行抽点考勤**********************"
            print "*****************4.查看当前考勤结果*******************"
            print "*****************5.查看历史考勤结果*******************"
            print "*****************6.回到上级目录**********************"
            list.tips(key)
            opNum = raw_input("请输入您想要的操作：")
            if (opNum == '1'):
                key['ProofPath']=raw_input("请输入您的请假证据：（学生）")
                key['SeqNum']=raw_input('请输入需要插入假条的考勤次序号')
                key['TeacherID']=raw_input('请输入老师的教工号')
                list.stufunct.Insert_leave_record(key)

            elif (opNum == '2'):  # 在线考勤
                key['ProofPath'] = raw_input("请输入您的考勤证据路径：（学生）")
                key['Type']='auto'
                list.autocheckin(key)

            elif (opNum == '3'):
                key['ProofPath'] = raw_input("请输入您的考勤证据路径：（学生）")
                key['Type'] = 'random'
                list.randomcheckin(key)

            elif (opNum == '4'):
                list.stufunct.real_view(key)

            elif (opNum == '5'):
                list.stufunct.history(key)

            elif (opNum == '6'):  # 回到主菜单
               break

            else:
                print "输入有误 没有对应输入的选项！"

    def att_output(self,key,list):

        while True:
            print "*************欢迎进入考勤成绩统计菜单*********************"
            print "*****************1.查看某次课程的出勤率******************"
            print "*****************2.查看某课程汇总出勤信息*****************"
            print "*****************3.显示用户总考勤概要信息****************"
            print "*****************4.显示用户总考勤详细信息****************"
            print "*****************5.回到上级目录************************"
            opNum = raw_input("请输入您想要的操作：")
            if (opNum == '1'):
                key['CourseName']=raw_input("请输入课程名称")
                num=raw_input('请输入查看课程的次序号')
                list.view.get_count_rate(key,num)

            elif (opNum == '2'):  # 在线考勤
                key['CourseName']=raw_input("请输入课程名称")
                list.view.get_all_rate(key)

            elif (opNum == '3'):
                list.view.dis_summary_sum(key)

            elif (opNum == '4'):
                list.view.dis_all_sum(key)

            elif (opNum == '5'):  # 回到主菜单
               break

            else:
                print "输入有误 没有对应输入的选项！"

    def teacherForm(self,key,list):

        while True:
            print "*************欢迎进入教师模拟控制菜单******************"
            print "*****************1.开启自动请假***********************"
            print "*****************2.开启抽点考勤************************"
            print "*****************3.开始手动考勤***********************"
            print "*****************4.设置考勤缓冲时间********************"
            print "*****************5.出勤情况随堂（实时）统计************"
            print "*****************6.生成出勤状况统计表******************"
            print "*****************7.出勤成绩统计汇总输出****************"
            print "*****************8.学生信息维护***********************"
            print "*****************9.考勤信息维护***********************"
            print "****************10.回到上级目录***********************"
            opNum = raw_input("请输入您想要的操作：")
            if (opNum == '1'):
                courseID=raw_input('请输入您要考勤的班级号!')
                key['ClassID']=courseID
                if not list.startcheckin(key):
                    print '开启考勤失败!'

            elif (opNum == '2'):  # 在线考勤
                list.startrandom(key)

            elif (opNum == '3'):
                courseID = raw_input('请输入您要考勤的课程号!')
                key['ClassID'] = courseID
                if not list.mancheckin(key):
                    print '开启考勤失败!'

            elif (opNum == '4'):
                list.maintain.rultSet(key)

            elif (opNum == '5'):
                list.view.view_time(key)

            elif (opNum == '6'):  # 回到主菜单
                if list.can_statistics(key):
                    key['ClassID']=raw_input('请输入需要计算的班级')
                    key['SeqNum']=raw_input('请输入考勤次序号')
                    list.view.creat_sum(key)

            elif (opNum == '7'):
                if list.can_statistics(key):
                    self.att_output(key,list)

            elif (opNum == '8'):
                list.maintain.mainTain_stu(key)

            elif (opNum == '9'):  # 回到主菜单
                key['ClassID']=raw_input('请输入需要维护的班级')
                list.maintain.mainTain_info(key)


            elif (opNum == '10'):
                break

            else:
                print "输入有误 没有对应输入的选项！"



    def adminForm(self,list):
        while True:
            print "*************欢迎进入管理员模拟控制菜单*****************"
            print "******************1.教师信息导入**********************"
            print "******************2.学生信息导入**********************"
            print "******************3.课程信息导入**********************"
            print "******************4.返回上一层************************"
            opNum = raw_input("请输入您想要的操作：")

            if opNum in ['1','2','3','4']:
                outfile=raw_input('请输入导入外部文件路径 :')
                if opNum=='1':
                    if list.import_file.import_teacher(outfile):
                        print '导入教师信息成功!'
                elif opNum=='2':
                    if list.import_file.import_stu(outfile):
                        print '导入学生信息成功!'
                elif opNum=='3':
                   if list.import_file.import_class(outfile):
                        print '导入课程信息成功!'
                else:
                    break
            else:
                print '错误输入,没有对应输入的选项!'

    def Form(self):
        Business=business()
        while True:
            print "****************欢迎进入模拟控制菜单******************"
            print "*****************1.教师登录*************************"
            print "*****************2.学生登录*************************"
            print "*****************3.管理员登录***********************"
            print "*****************4.退出程序*************************"
            opNum = raw_input("请输入您想要的操作：")
            if (opNum == '1'):  # 教师开启考勤
                teacherWechatID = raw_input("请输入您的微信号：（教师）")
                key=Business.teachertest(teacherWechatID)
                if key:
                    self.teacherForm(key,Business)
                else:
                    continue

            elif (opNum == '2'):  # 学生正常考勤操作
                stuWechatID = raw_input("请输入您的微信号：（学生）")
                key=Business.stuinfotest(stuWechatID)
                if key:
                    self.stuForm(key,Business)
                else:
                    continue

            elif (opNum == '3'):  #
                self.adminForm(Business)

            elif (opNum == '4'):  # 退出系统
                sys.exit(0)
            else:
                print "输入有误 没有对应输入的选项！"



if __name__ =="__main__" :

    SystemRun().Form()