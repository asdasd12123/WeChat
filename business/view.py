# coding=utf-8
import time
from dataoperation.manage import DataManage
from calculate import AuxiliaryFunction


class View(AuxiliaryFunction):

    def __init__(self):
        self.sum_filename = None
        self.detail_filename = None

    def historical_statistics(self):   # 这里的键值包括TeacherID和老师要统计的班级和次序号
        stu_info = DataManage(DataManage.target_info, args=(self.detail_filename,)).run()
        all_stu_info = self.statistics_calculation(stu_info)
        for (key, item) in all_stu_info['checkin'].items():
            if item['Type'] == 'Submitted':
                self.take_leave_absence({'StuID': key})
        return True

    def take_leave_absence(self, stu_id):  # 请假认定
        key = {'StuID': stu_id['StuID'], 'checkinType': 'leave'}
        stu_info = DataManage(DataManage.target_info, args=(self.detail_filename, key)).run()[0]
        print '学号：' + stu_info['StuID'] + '   该学生的请假证明路径为 : ' + stu_info['ProofPath']
        print '请假时间为 :%s' % (stu_info['checkTime'])
        stu_info['IsSucc'] = 'True'
        while True:
            num = raw_input('是否批准该学生的假条 ? yes or no \n')
            if num == 'yes':
                stu_info['checkinResult'] = 'approve'
                break
            elif num == 'no':
                stu_info['checkinResult'] = 'Absence'
                break
            else:
                print '请输入标准的选项!'
                time.sleep(1)
                continue
        return DataManage(DataManage.update,args=(self.detail_filename, 'w', [stu_info],
                                                  ['StuID', 'checkinType'])).run()

    def view_time(self, key):  # 输入教师教工号和班级号的字典　查看最近历史的一次考勤

        seq_info = DataManage(DataManage.target_info, args=('../InData/seq.csv',)).run()

        line = {}
        for seq in seq_info:
            if seq['TeacherID'] == key['TeacherID']:
                line['TeacherID'] = seq['TeacherID']
                line['ClassID'] = seq['ClassID']
                line['seqnum'] = seq['SeqID']

        if not line:
            print '您还没有完整的进行过一次考勤!'
            return False

        filename = '../InData/'+line['TeacherID']+'_'+line['ClassID']+'_'+line['seqnum']+'_Detail.csv'
        stu_info = DataManage(DataManage.target_info, args=(filename,)).run()
        return self.dis_play(stu_info)

    @staticmethod
    def class_sum_info(key):
        filename = '../InData/' + key['TeacherID'] + '_' + key['ClassID'] + '_Sum.csv'
        class_info = DataManage(DataManage.target_info, args=(filename,)).run()

        if not class_info:
            print '该班级不存在考勤信息!'
            return False

        stu_list = DataManage(DataManage.target_info, args=('../InData/studentInfo.csv',)).run()
        length = len(class_info[0].keys())
        print '班级: %-10s共被考勤%-2d次: ' %(key['ClassID'],length-1)
        stu_info = {}
        for stu in class_info:
            if not stu_info.has_key(stu['StuID']):
                info = {}
                for s in stu_list:
                    if s['StuID'] == stu['StuID']:
                        info['Name'] = s['StuName']
                        break
                info['normal'] = 0
                info['Absence'] = 0
                info['approve'] = 0
                info['leaveEarlier'] = 0
                info['Late'] = 0
                stu_info[stu['StuID']] = info

            for index in range(1, length):
                stu_info[stu['StuID']][stu['checkin'+str(index)]] += 1

        for (key, item) in stu_info.items():
            print '学号 :%-15s 姓名:%-10s出勤:%-2d 缺勤:%-2d 早退:%-2d 迟到:%-2d 请假:%-2d ' \
                  % (key, item['Name'], item['normal'], item['Absence'], item['leaveEarlier'], item['Late'],
                     item['approve'])

        return True

    def dis_all_sum(self, key):
        self.create_all_sum(key)
        seq_info = DataManage(DataManage.target_info, args=('../InData/seq.csv',)).run()
        class_info = []
        for seq in seq_info:
            if seq['TeacherID'] == key['TeacherID']:
                if seq['ClassID'] not in class_info:
                    class_info.append(seq['ClassID'])

        for info in class_info:
            key['ClassID'] = info
            self.class_sum_info(key)
        return True

    def dis_summary_sum(self, key):  # 计算
        course_info = DataManage(DataManage.target_info, args=('../InData/courseInfo.csv',
                                                               {'TeacherID': key['TeacherID']})).run()

        if not course_info:
            print '您还没有属于您的课程信息,请联系管理员导入信息!'
            return False

        course_list = []
        for course in course_info:
            if course['CourseName'] not in course_list:
                course_list.append(course['CourseName'])

        for course in course_list:
            print '您的%-10s课程的汇总考勤信息如下: ' %(course,)
            key['CourseName'] = course
            self.get_all_rate(key)

    def get_att_rate(self, key):  # 给定教师ID和班级号以及次序号获得出勤率
        filename = '../InData/' + key['TeacherID'] + '_' + key['ClassID'] + '_' + key['seqnum'] + '_Detail.csv'
        info = DataManage(DataManage.target_info, args=(filename,)).run()
        info = self.statistics_calculation(info)
        return info['grade']

    def get_all_rate(self, key):

        class_info = DataManage(DataManage.target_info, args=('../InData/courseInfo.csv',
                                                              {'TeacherID': key['TeacherID'],
                                                               'CourseName': key['CourseName']})).run()

        if not class_info:
            print '课程信息不存在请检查您的输入!'
            return False

        class_list = []
        for line in class_info:
            if line['ClassName'] not in class_list:
                class_list.append(line['ClassName'])  # 得到所有的班级名称

        seq_info = DataManage(DataManage.target_info, args=('../InData/seq.csv',)).run()

        count = 0
        for seq in seq_info:
            if seq['TeacherID'] == key["TeacherID"]:
                if seq['ClassID'] in class_list:
                    count = count + 1

        if count == 0:
            print '该门课程还没有完成的进行过一次考勤!'
            return False

        result = 0.0
        for index in range(1, count+1):
            grade = self.get_count_rate(key, index)
            if type(grade) == float:
                result = result + grade
            else:
                return False
        print '%-10s课平均考勤出勤率为:%-3.2f %%' %(key['CourseName'], 1.0 * result / count)
        return True

    def get_count_rate(self, key, num):  # 给定教师ID和课程返回平均出勤率 若给定num显示哪一次的

        try:
            num = int(num)
        except TypeError and ValueError:
                print '数据无效,请您输入正整数！'
                return False

        class_info = DataManage(DataManage.target_info, args=('../InData/courseInfo.csv',
                                                              {'TeacherID': key['TeacherID'],
                                                               'CourseName': key['CourseName']})).run()

        if not class_info:
            print '课程信息不存在请检查您的输入!'
            return False

        class_list = []
        for line in class_info:
            if line['ClassName'] not in class_list:
                class_list.append(line['ClassName'])  # 得到所有的班级名称

        seq_info = DataManage(DataManage.target_info, args=('../InData/seq.csv',)).run()

        count = 0
        for seq in seq_info:
            if seq['TeacherID'] == key["TeacherID"]:
                if seq['ClassID'] in class_list:
                    count = count+1
                    if count == num:
                        key['ClassID'] = seq['ClassID']
                        key['seqnum'] = seq['SeqID']
                        grade = self.get_att_rate(key)
                        print '%-10s课第%2d次是对班级: %-10s发起,考勤的出勤率为%-3.2f %%' \
                              % (key['CourseName'], count, key['ClassID'], grade)
                        return grade
        print '该次课程不存在第%d次考勤，请检查您的输入!' % (num,)
        return False

    def create_all_sum(self, key):

        seq_info = DataManage(DataManage.target_info, args=('../InData/seq.csv',)).run()
        line = {}
        for seq in seq_info:
            if seq['TeacherID'] == key['TeacherID']:
                if not line. has_key(seq['ClassID']):
                    line[seq['ClassID']] = 1
                else:
                    line[seq['ClassID']]= line[seq['ClassID']]+1

        if not line:
            print '您最近还没有进行过一次完整的考勤!'
            return False

        for (k, item) in line.items():
            key['ClassID'] = k
            for index in range(1, item+1):
                key['SeqNum'] = str(index)
                self.create_sum(key, 'no')

    def create_sum(self, key, info=''):

        filename = '../InData/' + key['TeacherID'] + '_' + key['ClassID'] + '_' + key['SeqNum'] + '_Detail.csv'

        if not DataManage(DataManage.target_key, args=(filename,)).run():
            print '该次考勤不存在无法计算考勤的结果'
            return False

        if not self.init(key):
            print '初始化考勤汇总表失败请检查您的键值是否正确!'
            return False

        self.detail_filename = filename
        self.historical_statistics()
        stu_list = DataManage(DataManage.target_info, args=(self.detail_filename,)).run()
        stu_list = self.statistics_calculation(stu_list)
        old_data = DataManage(DataManage.target_info, args=(self.sum_filename,)).run()
        DataManage(DataManage.update, args=(self.sum_filename, 'dl', old_data)).run()

        for line in old_data:
            line['checkin'+key['SeqNum']] = 'normal'
            for (k, item) in stu_list['checkin'].items():
                if line['StuID'] == k:
                    line['checkin' + key['SeqNum']] = item['Type']
        if not info:
            print '您为班级%s创建第%s次考勤汇总表成功!' % (key['ClassID'], key['SeqNum'])
        return DataManage(DataManage.update, args=(self.sum_filename, 'w', old_data)).run()

    def init(self, key):
        self.sum_filename = '../InData/'+key['TeacherID']+'_'+key['ClassID']+'_'+'Sum.csv'
        if not DataManage(DataManage.target_key, args=(self.sum_filename,)).run():
            result = []
            stu_list = DataManage(DataManage.target_info, args=('../InData/studentInfo.csv',
                                                                {'ClassID': key['ClassID']})).run()
            for k in stu_list:
                sum_dict = dict()
                sum_dict['StuID'] = k['StuID']
                result.append(sum_dict)
            return DataManage(DataManage.update, args=(self.sum_filename, 'w', sum)).run()

        return True
