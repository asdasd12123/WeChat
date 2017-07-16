#coding=utf-8
from DataProcess.DataProcess import DataProcess
import re
from Auxiliaryfunction import  Auxiliaryfunction
import time

class view(Auxiliaryfunction):

    def __init__(self):
        self.sum_filename=None
        self.detail_filename=None

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

    def view_time(self,key):  # 输入教师教工号和班级号的字典　查看最近历史的一次考勤

        seqinfo=DataProcess(target=DataProcess.QueryObjectInfo, args=('../InData/seq.csv',)).run()

        line={}
        for seq in seqinfo:
            if seq['TeacherID']==key['TeacherID']:
                line['TeacherID']=seq['TeacherID']
                line['ClassID']=seq['ClassID']
                line['seqnum']=seq['SeqID']

        if not line:
            print '您还没有完整的进行过一次考勤!'
            return False

        filename='../InData/'+line['TeacherID']+'_'+line['ClassID']+'_'+line['seqnum']+'_Detail.csv'
        stuinfo = DataProcess(target=DataProcess.QueryObjectInfo, args=(filename,)).run()
        return self.dis_play(stuinfo)


    

    def creat_sum(self,key):

        if not self.init(key):
            print '初始化失败请检查您的键值是否正确!'
            return False

        def operation(line):
            line=re.split('_',line)
            if '../InData/'+key['TeacherID'] in line and key['ClassID'] in line and key['SeqNum'] in line:
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
            line['checkin'+key['SeqNum']]='normal'
            for (k,item) in stulist['checkin'].items():
                if line['StuID']==k:
                    line['checkin'+key['SeqNum']]=item['Type']
        print '创建第%s次的考勤汇总表成功!' %(key['SeqNum'])
        return DataProcess(target=DataProcess.update,args=(self.sum_filename,'w',olddata)).run()


    def init(self,key):
        self.sum_filename='../InData/'+key['TeacherID']+'_'+key['ClassID']+'_'+'Sum.csv'
        if not DataProcess(target=DataProcess.QueryObjectKey,args=(self.sum_filename,)).run():
            sum=[]
            stulist=DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/studentInfo.csv',{'ClassID':self.key['ClassID']})).run()
            for k in stulist:
                sumdict = {}
                sumdict['StuID']=k['StuID']
                sum.append(sumdict)
            return DataProcess(target=DataProcess.update,args=(self.sum_filename,'w',sum)).run()

        return True



if __name__=='__main__':
    c=view({'TeacherID':'2004633','ClassID':"软件工程1401",'SeqNum':'3'})

    c.creat_sum()
    c.view_time()