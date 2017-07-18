# coding=utf-8
import time
from dataoperation.manage import DataManage


class Maintain(object):

    '''
    手动修改
    手动考勤
    手动设置个人考勤规则
    '''

    def is_can(self, key):
        stu_list = DataManage(DataManage.target_info,args=('../InData/studentInfo.csv', key)).run()
        if stu_list or len(stu_list) != 0:
            return False
        return True

    def main_tain_stu(self,key):  # 手动维护学生信息
        classinfo = DataManage(DataManage.target_info, args=('../InData/courseInfo.csv',
                                                             {'TeacherID':key['TeacherID']})).run()
        classlist = set()
        for line in classinfo:
            classlist.add(line['ClassName'])
        classlist = list(classlist)
        stuinfo = DataManage(DataManage.target_info, args=('../InData/studentInfo.csv',)).run()

        for stu in stuinfo:
            if stu['ClassID'] not in classlist:
                stuinfo.remove(stu)

        stuID = raw_input('请输入您需要修改学生的学号!')
        info = {}
        for stu in stuinfo:
            if stu['StuID'] == stuID:
                info = stu
                break
        if not info:
            print '该学生不在你的修改范围之内无法修改!'
            return False

        info = self.get_result(classlist, info)

        error = DataManage(DataManage.format_check,args=([info],{"StuID": '^[\d]{12}$',
                           "StuName": '^[\x80-\xff]{6,18}$', "WeChatID": '^[a-zA-Z0-9_]+$',
                                                                 "ClassID": '[\x80-\xff]+\d{4}$'})).run()

        if DataManage(DataManage.get_result, args=(error,)).run():
            print error
            print '您输入的格式错误无法修改学生信息!'
            return False

        DataManage(DataManage.update, args=('../InData/studentInfo.csv','dl', [info])).run()
        print '修改学生信息成功!'
        return DataManage(DataManage.update, args=('../InData/studentInfo.csv', 'w', [info])).run()

    def get_result(self, classlist, data):
        sel = raw_input('是否修改学号? (yes or other)')
        if sel == 'yes':
            stuID = raw_input('请输入学号!')
            if self.is_can({'StuID':stuID}):
                data['StuID'] = stuID
            else:
                print '该学号不唯一无法修改成为此学号!'

        sel = raw_input('是否修改姓名? (yes or other)')
        if sel == 'yes':
            stuName = raw_input('请输入姓名!')
            data['StuName'] = stuName

        sel = raw_input('是否修改微信号? (yes or other)')
        if sel == 'yes':
            WeChatID = raw_input('请输入微信号!')
            if self.is_can({'WeChatID': WeChatID}):
                data['WeChatID'] = WeChatID
            else:
                print '该微信号不唯一无法修改成为此微信号!'

        sel = raw_input('是否修改班级? (yes or other)')
        if sel == 'yes':
            ClassID = raw_input('请输入班级!')
            if ClassID in classlist:
                data['ClassID'] = ClassID
            else:
                print '您输入的班级不在您的维护范围之内无法修改!'

        sel = raw_input('是否修改个人信息特征? (yes or other)')
        if sel == 'yes':
            path = raw_input('请输入特征路径!')
            if self.is_can({'FeaturePath': path}):
                data['FeaturePath'] = path
            else:
                print '该特征不唯一无法修改成为此特征!'

        return data

    def main_tain_info(self, key): # 手动维护考勤信息
        seqnum = raw_input('请输入您需要修改哪一次的记录！')
        filename = '../InData/'+key['TeacherID']+'_'+key['ClassID']+'_Sum.csv'
        stuinfo = DataManage(DataManage.target_info, args=(filename,)).run()

        if not stuinfo or 'checkin' + seqnum not in stuinfo[0].keys():
            print '该次考勤汇总表不存在请检查您的输入!'
            return False

        print '该次考勤所有学生的考勤状态如下:'
        for stu in stuinfo:
            print stu['StuID'] + ' : ' + stu['checkin'+seqnum]

        stuID = raw_input("请输入你要修改学生的学号!")
        count = 0
        stu_info = {}
        for stu in stuinfo:
            if stu['StuID'] == stuID:
                stu_info = stu
                count = 1
                break
        if count == 0:
            print '该学生不存在请检查您的输入!'
            return False

        print '该学生的该次的考勤状态 : %s' %(stu_info['checkin' + seqnum])
        print '请按照以下选项输入状态 非法输入默认为缺勤!'
        print ' 1　正常　2　迟到　３　早退　４　缺勤 5　请假已批准'
        _type = raw_input('请输入你希望修改的值!')
        if _type not in ['1', '2', '3', '4', '5']:
            print '您输入了非法选项默认结果为缺勤!'
            stu_info['checkin'+seqnum] = 'Absence'
        else:
            stu_info['checkin' + seqnum] = {'1': 'normal', '2': 'Late', '3': 'leaveEarlier', '4': 'Absence',
                                            '5': 'approve'}[_type]
            print '修改成功!'
        return DataManage(DataManage.update, args=(filename, 'w', [stu_info], ['StuID'])).run()

    def rultSet(self, key):
        while True:
            buffer = raw_input('请输入您为学生设置的考勤信息上传缓冲时间!(在此时间内的考勤属于有效，该时间至少为1分钟,最长为10分钟)')
            try:
                buffer = int(buffer)
            except TypeError and ValueError:
                print '您的输入不符合规则,请重新输入!'
                continue

            if buffer < 1 or buffer > 10:
                print '缓冲时间大于或小于当前的规定范围请重新输入!'
                time.sleep(1)
            else:
                print '设置完成,下一次发起考勤时会自动采用此次的设置!'
                break

        data={'TeacherID': key['TeacherID'], 'bufferTime': buffer}
        return DataManage(DataManage.update, args=('../InData/set.csv', 'w', [data], ['TeacherID'])).run()

    def read_rule(self, key):
        rule=DataManage(DataManage.target_info, args=('../InData/set.csv',
                                                          {'TeacherID': key['TeacherID']})).run()

        if not rule:
            return {'TeacherID': key['TeacherID'], 'bufferTime': '3'}

        else:
            return rule[0]
