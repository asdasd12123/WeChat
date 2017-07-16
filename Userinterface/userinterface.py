#coding=utf-8
from Business.Business import business
import sys

class SystemRun(object):

    def stuForm(self,key,list):
        print "*************欢迎进入学生模拟控制菜单******************"
        print "*****************1.在线请假*************************"
        print "*****************2.进行考勤*************************"
        print "*****************3.进行抽点考勤**********************"
        print "*****************4.查看当前考勤结果*******************"
        print "*****************5.查看历史考勤结果*******************"
        print "*****************6.回到上级目录**********************"

        while True:
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
                opNum = raw_input("您的输入有误！请重新输入:")
        self.Form()

    def teacherForm(self,key,list):
        print "*************欢迎进入教师模拟控制菜单******************"
        print "*****************1.开启自动请假**********************"
        print "*****************2.开启抽点考勤**********************"
        print "*****************3.开始手动考勤**********************"
        print "*****************4.设置默认考勤规则*******************"
        print "*****************5.出勤情况随堂（实时）统计************"
        print "*****************6.出勤情况历史统计*******************"
        print "*****************7.出勤成绩输出**********************"
        print "*****************8.学生信息维护**********************"
        print "*****************9.考勤信息维护**********************"
        print "****************10.回到上级目录**********************"
        while True:
            opNum = raw_input("请输入您想要的操作：")
            if (opNum == '1'):
                courseID=raw_input('请输入您要考勤的课程号!')
                key['ClassID']=courseID
                if not list.startcheckin(key):
                    print '开启考勤失败!'

            elif (opNum == '2'):  # 在线考勤
                list.startrandom(key)

            elif (opNum == '3'):
                pass

            elif (opNum == '4'):
                pass

            elif (opNum == '5'):
                list.view.view_time(key)

            elif (opNum == '6'):  # 回到主菜单
                key['ClassID']=raw_input('请输入需要计算的班级')
                key['SeqNum']=raw_input('请输入考勤次序号')
                list.view.creat_sum(key)

            elif (opNum == '7'):
                pass

            elif (opNum == '8'):
                list.maintain.mainTain_stu(key)

            elif (opNum == '9'):  # 回到主菜单
                key['ClassID']=raw_input('请输入需要维护的班级')
                list.maintain.mainTain_info(key)


            elif (opNum == '10'):
                break

            else:
                opNum = raw_input("您的输入有误！请重新输入:")
        self.Form()



    def adminForm(self,password):
        print "*************欢迎进入管理员模拟控制菜单******************"
        print "******************1.信息导入**************************"
        print "******************2.回到上级目录**********************"

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
                adminWechatID = raw_input("请输入您的微信号：（管理员）")
                key = Business.stuinfotest(adminWechatID)
                if key:
                    self.adminForm(key)
                else:
                    continue

            elif (opNum == '4'):  # 退出系统
                sys.exit(0)
            else:
                print "输入有误 没有对应输入的选项！"



if __name__ =="__main__" :

    SystemRun().Form()