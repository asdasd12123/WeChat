#coding=utf-8
from DataProcess.DataProcess import DataProcess
import datetime
import re
from Auxiliaryfunction import Auxiliaryfunction
'''
在此模块中学生进行考勤　请假 　
'''

class student_fun(object):

    def view(self,filename,stuid,teacherid,num,counter={}):

        stuinfo = DataProcess(target=DataProcess.QueryObjectInfo, args=(filename,)).run()

        if num==1:
            stuinfo = Auxiliaryfunction().statistics_calculation(stuinfo)

        name = DataProcess(target=DataProcess.QueryObjectInfo,
                           args=('../InData/teacherInfo.csv', {'TeacherID': teacherid})).run()[0]['TeacherName']
        classname = DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/courseInfo.csv', {'TeacherID': teacherid})).run()[0]['CourseName']

        if num==1:
            for (k, item) in stuinfo['checkin'].items():
                if k == stuid:
                    print '%s老师在%s课上发起考勤,您在此次考勤状态为: %s' % (name, classname,item['Type'])
                    return
            print '%s老师在%s课上发起考勤,您在此次考勤状态为: normal' % (name, classname)

        else:
            length=len(stuinfo[0].keys())-1
            for info in stuinfo:
                if info['StuID']==stuid:
                    for index in range(1,length):
                        print '%s老师在%s课上发起第%d次考勤,您在此次考勤状态为: %s' % (name, classname,index,info['checkin'+str(index)])
                        counter[info['checkin'+str(index)]]=counter[info['checkin'+str(index)]]+1



    def history(self,key):
        seqinfo = DataProcess(target=DataProcess.QueryObjectInfo,
                              args=('../InData/seq.csv',)).run()
        data=[]
        for seq in seqinfo:
            if seq['ClassID'] == key['ClassID']:
                if seq['TeacherID'] not in data:
                    data.append(seq['TeacherID'])

        if not data:
            print '您最近还没有进行过一次完整的考勤!'
            return False

        filelist=[]
        for line in data:
            filename = '../InData/' + line + '_' + key['ClassID'] +'_Sum.csv'
            filelist.append(filename)

        num={}
        num['normal']=0
        num['Absence']=0
        num['approve']=0
        num['leaveEarlier']=0
        for index in range(len(data)):
            print '第%d门课考勤信息如下:' %(index+1)
            self.view(filelist[index],key['StuID'],data[index],0,num)
        print '您正常考勤%d次,缺勤%d次,请假%d次,早退%d次! 出勤率%.2f %%' %(num['normal'],num['Absence'],num['approve'],num['leaveEarlier'],
        1.0* num['normal'] /(num['normal']+ num['Absence']+ num['approve']+num['leaveEarlier']))
        return True

    def real_view(self,key):

        seqinfo=DataProcess(target=DataProcess.QueryObjectInfo,
            args=('../InData/seq.csv',)).run()

        line={}
        for seq in seqinfo:
            if seq['ClassID']==key['ClassID']:
               line['TeacherID']=seq['TeacherID']
               line['SeqID']=seq['SeqID']

        if not line:
            print '您最近还没有进行过一次完整的考勤!'
            return False

        filename='../InData/'+line['TeacherID']+'_'+key['ClassID']+'_'+line['SeqID']+'_Detail.csv'
        self.view(filename,key['StuID'],line['TeacherID'])




    def  Insert_leave_record(self,key): #向历史记录添加请假 #学生请假休息包括 学号　提交类型　请假证明　提交时间
        data={}

        def operation(filename):
            filename=re.split('_',filename)
            if key['SeqNum'] in filename and '../InData/'+key['TeacherID'] in filename and key['ClassID'] in filename and 'Detail.csv' in filename:
                return True
            return False

        filename=DataProcess(target=DataProcess.QueryNameByInfo,
        args=(operation,)).run()
        if not filename:
            print '满足您输入信息的考勤细节表不存在!'
            return False

        if DataProcess(target=DataProcess.QueryObjectInfo,
        args=(filename[0],{'StuID':key['StuID'],'checkinType':'leave'})).run():

            print '您在该次考勤中已经申请过请假无法再次申请!'
            return False

        data['StuID'] = key['StuID']
        data['checkTime'] = str(datetime.datetime.now())[:-7]
        data['ProofPath'] = key['ProofPath']
        data['checkinType'] = 'leave'
        data['IsSucc'] = 'True'
        data['checkinResult'] = 'Submitted'
        print '提交假条成功!'
        return DataProcess(target=DataProcess.update,args=(filename[0],'a',[data])).run()


