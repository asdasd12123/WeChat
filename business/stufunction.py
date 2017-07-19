# coding=utf-8
import re
import datetime
from dataoperation.manage import DataManage
from calculate import AuxiliaryFunction
'''
在此模块中学生进行考勤　请假 　查看
'''


class StudentFun(object):

    @staticmethod
    def view(filename, stu_id, teacher_id, num, counter=None):

        stu_info = DataManage(DataManage.target_info, args=(filename,)).run()
        if not stu_info:
            print '该教师尚未统计此次的考勤汇总信息,所以无法查看结果'
            return False

        if num == 1:
            stu_info = AuxiliaryFunction().statistics_calculation(stu_info)

        name = DataManage(DataManage.target_info, args=('../InData/teacherInfo.csv',
                                                        {'TeacherID': teacher_id})).run()[0]['TeacherName']

        class_name = DataManage(DataManage.target_info, args=('../InData/courseInfo.csv',
                                                              {'TeacherID': teacher_id})).run()[0]['CourseName']

        if num == 1:
            for (k, item) in stu_info['checkin'].items():
                if k == stu_id:
                    print '%s老师在%s课上发起考勤,您在此次考勤状态为: %s' % (name, class_name, item['Type'])
                    return True
            print '%s老师在%s课上发起考勤,您在此次考勤状态为: normal' % (name, class_name)

        else:
            length = len(stu_info[0].keys())
            for info in stu_info:
                if info['StuID'] == stu_id:
                    for index in range(1, length):
                        print '%s老师在%s课上发起第%d次考勤,您在此次考勤状态为: %s' % (name, class_name, index,
                                                                   info['checkin'+str(index)])
                        counter[info['checkin'+str(index)]] = counter[info['checkin'+str(index)]]+1

    def history(self, key):
        seq_info = DataManage(DataManage.target_info, args=('../InData/seq.csv',)).run()
        data = []
        for seq in seq_info:
            if seq['ClassID'] == key['ClassID']:
                if seq['TeacherID'] not in data:
                    data.append(seq['TeacherID'])

        if not data:
            print '您最近还没有进行过一次完整的考勤!'
            return False

        file_list = list()
        for line in data:
            filename = '../InData/' + line + '_' + key['ClassID'] + '_Sum.csv'
            file_list.append(filename)

        if not file_list:
            print '您的任何一位教师都尚未统计考勤汇总信息,所以无法查看结果'
            return False

        for index in range(len(data)):
            num = dict()
            num['normal'] = 0
            num['Absence'] = 0
            num['approve'] = 0
            num['leaveEarlier'] = 0
            print '第%d门课考勤信息如下:' % (index + 1)
            if self.view(file_list[index], key['StuID'], data[index], 0, num):
                print '您正常考勤%d次,缺勤%d次,请假%d次,早退%d次! 出勤率%.2f %%' %(num['normal'], num['Absence'],
                            num['approve'], num['leaveEarlier'],
                            1.0 * num['normal'] / (num['normal'] + num['Absence'] + num['approve']+num['leaveEarlier']))

        return True

    def real_view(self, key):

        seq_info = DataManage(DataManage.target_info, args=('../InData/seq.csv',)).run()

        line = dict()
        for seq in seq_info:
            if seq['ClassID'] == key['ClassID']:
                line['TeacherID'] = seq['TeacherID']
                line['SeqID'] = seq['SeqID']

        if not line:
            print '您最近还没有进行过一次完整的考勤!'
            return False

        filename = '../InData/'+line['TeacherID']+'_'+key['ClassID']+'_'+line['SeqID']+'_Detail.csv'
        self.view(filename, key['StuID'], line['TeacherID'], 1)

    @staticmethod
    def insert_leave_record(key):  # 向历史记录添加请假 学生请假休息包括 学号　提交类型　请假证明　提交时间

        seq_info = DataManage(DataManage.target_info, args=('../InData/seq.csv',)).run()

        count = 0
        for seq in seq_info:
            if seq['TeacherID'] == key['TeacherID']:
                if seq['ClassID'] == seq['ClassID']:
                    count = seq['SeqID']

        if not count:
            print '满足您输入信息的考勤细节表不存在!'
            return False

        filename = '../InData/'+key['TeacherID']+'_'+key['ClassID']+'_'+count+'_Detail.csv'

        if DataManage(DataManage.target_info, args=(filename, {'StuID': key['StuID'], 'checkinType': 'leave'})).run():
            print '您在该次考勤中已经申请过请假无法再次申请!'
            return False

        data = dict()
        data['StuID'] = key['StuID']
        data['checkTime'] = str(datetime.datetime.now())[:-7]
        data['ProofPath'] = key['ProofPath']
        data['checkinType'] = 'leave'
        data['IsSucc'] = 'False'
        data['checkinResult'] = 'Submitted'
        print '提交假条成功!'
        return DataManage(DataManage.update, args=(filename, 'a', [data])).run()


