#coding=utf-8
from DataProcess.DataProcess import DataProcess
import re
from Auxiliaryfunction import  Auxiliaryfunction
import time

class view(Auxiliaryfunction):

    def __init__(self,key):
        self.sum_filename=None
        self.detail_filename=None
        self.key=key

    def historical_statistics(self):  # 这里的键值包括TeacherID和老师要统计的班级和次序号
        stuinfo = DataProcess(target=DataProcess.QueryObjectInfo, args=(self.detail_filename,)).run()
        allstuinfo = self.statistics_calculation(stuinfo)
        for (key, item) in allstuinfo['checkin'].items():
            if item['Type'] == 'Submitted':
                self.Take_leave_absence({'StuID': key})
        return True

    def Take_leave_absence(self,stuID):  # 请假认定
        stuinfo = DataProcess(target=DataProcess.QueryObjectInfo, args=(self.detail_filename, stuID)).run()[0]
        print '学号：' + stuinfo['StuID'] + '   该学生的请假证明路径为 : ' + stuinfo['ProofPath']
        while True:
            num = raw_input('是否批准该学生的假条 ? yes or no \n')
            if num == 'yes':
                stuinfo['IsSucc'] = 'True'
                stuinfo['checkinResult'] = 'approve'
                DataProcess(target=DataProcess.update,
                            args=(self.detail_filename, 'w', [stuinfo], ['StuID', 'checkstartTime'])).run()
                break
            elif num == 'no':
                stuinfo['IsSucc'] = 'True'
                stuinfo['checkinResult'] = 'Absence'
                DataProcess(target=DataProcess.update,
                            args=(self.detail_filename, 'w', [stuinfo], ['StuID', 'checkinType'])).run()
                break
            else:
                print '请输入标准的选项!'
                time.sleep(1)
                continue

    def view_time(self):  # 输入教师教工号和班级号的字典　查看最近历史的一次考勤

        def operation(filename):
            filename = re.split('_', filename)
            if '../InData/' + self.key['TeacherID'] in filename and \
                            self.key['ClassID'] in filename and 'Detail.csv' in filename:
                return True
            return False

        filename = DataProcess(target=DataProcess.QueryNameByInfo, args=(operation,)).run()[-1]

        if not filename:
            print '您最近还没有进行过一次完整的考勤'
            return False

        stuinfo = DataProcess(target=DataProcess.QueryObjectInfo, args=(filename,)).run()
        return self.dis_play(stuinfo)

    def creat_sum(self):

        if not self.init():
            print '初始化失败请检查您的键值是否正确!'
            return False

        def operation(line):
            line=re.split('_',line)
            if '../InData/'+self.key['TeacherID'] in line and self.key['ClassID'] in line and self.key['SeqNum'] in line:
                return True
            return False

        filename = DataProcess(target=DataProcess.QueryNameByInfo, args=(operation,)).run()
        if not filename:
            print '该次考勤不存在无法计算考勤的结果'
            return False

        self.detail_filename=filename[0]
        self.historical_statistics()
        stulist=DataProcess(target=DataProcess.QueryObjectInfo, args=(self.detail_filename,)).run()
        stulist=self.statistics_calculation(stulist)
        olddata=DataProcess(target=DataProcess.QueryObjectInfo, args=(self.sum_filename,)).run()
        DataProcess(target=DataProcess.update, args=(self.sum_filename,'dl',olddata)).run()

        for line in olddata:
            line['checkin'+self.key['SeqNum']]='normal'
            for (key,item) in stulist['checkin'].items():
                if line['StuID']==key:
                    line['checkin'+self.key['SeqNum']]=item['Type']
        return DataProcess(target=DataProcess.update,args=(self.sum_filename,'w',olddata)).run()


    def init(self):
        self.sum_filename='../InData/'+self.key['TeacherID']+'_'+self.key['ClassID']+'_'+'Sum.csv'
        if not DataProcess(target=DataProcess.QueryObjectKey,args=(self.sum_filename,)).run():
            sum=[]
            stulist=DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/studentInfo.csv',{'ClassID':self.key['ClassID']})).run()
            for key in stulist:
                sumdict = {}
                sumdict['StuID']=key['StuID']
                sum.append(sumdict)
            return DataProcess(target=DataProcess.update,args=(self.sum_filename,'w',sum)).run()

        return True



if __name__=='__main__':
    c=view({'TeacherID':'2004633','ClassID':"软件工程1401",'SeqNum':'1'})
    c.creat_sum()
    c.view_time()