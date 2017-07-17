#coding=utf-8
from DataProcess.DataProcess import DataProcess
import re
from Auxiliaryfunction import  Auxiliaryfunction
import time


def ch( data):
    count = 0
    for s in data:
        if ord(s) > 127:
            count += 1
    return count


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

    def class_sum_info(self,key):
        filename = '../InData/' + key['TeacherID'] + '_' + key['ClassID'] + '_Sum.csv'
        classinfo=DataProcess(target=DataProcess.QueryObjectInfo,args=(filename,)).run()

        if not classinfo:
            print '该班级不存在考勤信息!'
            return False

        stulist=DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/studentInfo.csv',)).run()
        length=len(classinfo[0].keys())
        print '班级: %-10s共被考勤%-2d次: ' %(key['ClassID'],length-1)
        stuinfo={}
        for stu in classinfo:
            if not stuinfo.has_key(stu['StuID']):
                info={}
                for s in stulist:
                    if s['StuID']==stu['StuID']:
                        info['Name']=s['StuName']
                        break
                info['normal']=0
                info['Absence']=0
                info['approve']=0
                info['leaveEarlier']=0
                info['Late']=0
                stuinfo[stu['StuID']]=info

            for index in range(1,length):
                stuinfo[stu['StuID']][stu['checkin'+str(index)]]+=1

        for (key,item) in stuinfo.items():

            number=ch(item['Name'])
            print '学号 :%-15s 姓名:%-10s出勤:%-2d 缺勤:%-2d 早退:%-2d 迟到:%-2d 请假:%-2d ' \
            %(key,item['Name'],item['normal'],item['Absence'],item['leaveEarlier'],
              item['Late'],item['approve'])

        return True

    def dis_all_sum(self,key):
        self.creat_all_sum(key)
        seqinfo = DataProcess(target=DataProcess.QueryObjectInfo, args=('../InData/seq.csv',)).run()
        classinfo=[]
        for seq in seqinfo:
            if seq['TeacherID']==key['TeacherID']:
                if seq['ClassID'] not in classinfo:
                    classinfo.append(seq['ClassID'])

        for info in classinfo:
            key['ClassID']=info
            self.class_sum_info(key)
        return True


    def dis_summary_sum(self,key): #计算
        courseinfo = DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/courseInfo.csv',{'TeacherID': key['TeacherID']})).run()

        if not courseinfo:
            print '您还没有属于您的课程信息,请联系管理员导入信息!'
            return False

        courselist=[]
        for course in courseinfo:
            if course['CourseName'] not in courselist:
                courselist.append(course['CourseName'])

        for course in courselist:
            print '您的%-10s课程的汇总考勤信息如下: ' %(course)
            key['CourseName']=course
            self.get_all_rate(key)

    def get_att_rate(self,key):#给定教师ID和班级号以及次序号获得出勤率
        filename = '../InData/' + key['TeacherID'] + '_' + key['ClassID'] + '_' + key['seqnum'] + '_Detail.csv'
        info=DataProcess(target=DataProcess.QueryObjectInfo,args=(filename,)).run()
        info=self.statistics_calculation(info)
        return info['grade']

    def get_all_rate(self,key):

        classinfo = DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/courseInfo.csv',{'TeacherID': key['TeacherID'], 'CourseName': key['CourseName']})).run()

        if not classinfo:
            print '课程信息不存在请检查您的输入!'
            return False

        classlist = []
        for line in classinfo:
            if line['ClassName'] not in classlist:
                classlist.append(line['ClassName'])  # 得到所有的班级名称

        seqinfo = DataProcess(target=DataProcess.QueryObjectInfo, args=('../InData/seq.csv',)).run()

        count = 0
        for seq in seqinfo:
            if seq['TeacherID'] == key["TeacherID"]:
                if seq['ClassID'] in classlist:
                    count = count + 1

        if count==0:
            print '该门课程还没有完成的进行过一次考勤!'
            return False

        sum=0.0
        for index in range(1,count+1):
            grade=self.get_count_rate(key,index)
            if type(grade)==float:
               sum=sum+grade
            else:
                return False
        print '%-10s课平均考勤出勤率为:%-3.2f %%' %(key['CourseName'],1.0*sum/count)
        return True

    def get_count_rate(self,key,num): #给定教师ID和课程返回平均出勤率 若给定num显示哪一次的

        try:
            num=int(num)
        except TypeError and ValueError:
                print '数据无效,请您输入正整数！'
                return False


        classinfo=DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/courseInfo.csv',{'TeacherID':key['TeacherID'],'CourseName':key['CourseName']})).run()

        if not classinfo:
            print '课程信息不存在请检查您的输入!'
            return False

        classlist=[]
        for line in classinfo:
            if line['ClassName'] not in classlist:
                classlist.append(line['ClassName']) #得到所有的班级名称

        seqinfo = DataProcess(target=DataProcess.QueryObjectInfo, args=('../InData/seq.csv',)).run()

        count = 0
        for seq in seqinfo:
            if seq['TeacherID']==key["TeacherID"]:
                if seq['ClassID'] in classlist:
                    count=count+1
                    if count==num:
                        key['ClassID']=seq['ClassID']
                        key['seqnum']=seq['SeqID']
                        grade=self.get_att_rate(key)
                        print '%-10s课第%2d次是对班级: %-10s发起,考勤的出勤率为%-3.2f %%' %(key['CourseName'],count,key['ClassID'],grade)
                        return grade
        print '该次课程不存在第%d次考勤，请检查您的输入!' %(num)
        return False




    def creat_all_sum(self,key):

        seqinfo = DataProcess(target=DataProcess.QueryObjectInfo,
                              args=('../InData/seq.csv',)).run()
        line={}
        for seq in seqinfo:
            if seq['TeacherID'] == key['TeacherID']:
                if not line.has_key(seq['ClassID']):
                    line[seq['ClassID']]=1
                else:
                    line[seq['ClassID']]= line[seq['ClassID']]+1

        if not line:
            print '您最近还没有进行过一次完整的考勤!'
            return False

        for (k,item) in line.items():
           key['ClassID']=k
           for index in range(1,item+1):
               key['SeqNum']=str(index)
               self.creat_sum(key,'no')


    def creat_sum(self,key,info=''):

        filename = '../InData/' + key['TeacherID'] + '_' + key['ClassID'] + '_' + key['SeqNum'] + '_Detail.csv'

        if not DataProcess(target=DataProcess.QueryObjectKey, args=(filename,)).run():
            print '该次考勤不存在无法计算考勤的结果'
            return False

        if not self.init(key):
            print '初始化失败请检查您的键值是否正确!'
            return False

        self.detail_filename=filename
        self.historical_statistics()
        stulist=DataProcess(target=DataProcess.QueryObjectInfo, args=(self.detail_filename,)).run()
        stulist=self.statistics_calculation(stulist)
        olddata=DataProcess(target=DataProcess.QueryObjectInfo, args=(self.sum_filename,)).run()
        DataProcess(target=DataProcess.update, args=(self.sum_filename,'dl',olddata)).run()

        for line in olddata:
            line['checkin'+key['SeqNum']]='Absence'
            for (k,item) in stulist['checkin'].items():
                if line['StuID']==k:
                    line['checkin'+key['SeqNum']]=item['Type']
        if not info:
            print '您为班级%s创建第%s次考勤汇总表成功!' %(key['ClassID'],key['SeqNum'])
        return DataProcess(target=DataProcess.update,args=(self.sum_filename,'w',olddata)).run()


    def init(self,key):
        self.sum_filename='../InData/'+key['TeacherID']+'_'+key['ClassID']+'_'+'Sum.csv'
        if not DataProcess(target=DataProcess.QueryObjectKey,args=(self.sum_filename,)).run():
            sum=[]
            stulist=DataProcess(target=DataProcess.QueryObjectInfo,
            args=('../InData/studentInfo.csv',{'ClassID':key['ClassID']})).run()
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