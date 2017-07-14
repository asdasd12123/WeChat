#coding=utf-8
from DataProcess.DataProcess import DataProcess
import datetime
import re
'''
在此模块中学生进行考勤　请假 　
'''

class studentcheckin(object):

    def getstukey(self):
        stukey = {}
        stukey['StuID'] = raw_input('Please input your student number！')
        stukey['ClassID'] = raw_input('Please input your class!')
        stuinfo = DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/studentInfo.csv', stukey)).run()
        if not stuinfo:
            print 'Identity failed!'
            return None
        return stuinfo[0]


    def  Insert_leave_record(self,key): #向历史记录添加请假 #学生请假休息包括 学号　提交类型　请假证明　提交时间

        data={}

        def operation(filename):
            filename=re.split('_',filename)
            if key['SeqNum'] in filename and '../InData/'+key['TeacherID'] in filename and key['ClassName'] in filename and 'Detail.csv' in filename:
                return True
            return False

        filename=DataProcess(target=DataProcess.QueryNameByInfo,args=(operation,)).run()
        if not filename:
            print '满足您输入信息的考勤细节表不存在!'
            return False

        if DataProcess(target=DataProcess.QueryObjectInfo,args=(filename[0],{'StuID':key['StuID'],'checkinType':'leave'})).run():
            print '您在该次考勤中已经申请过请假无法再次申请!'
            return False

        data['StuID'] = key['StuID']
        data['checkstartTime'] = 'null'
        data['checkTime'] = str(datetime.datetime.now())[:-7]
        data['ProofPath'] = key['Prove']
        data['checkinType'] = 'leave'
        data['IsSucc'] = 'True'
        data['checkinResult'] = 'Submitted'
        return DataProcess(target=DataProcess.update,args=(filename[0],'a',[data])).run()


    def studealy(self):
        '''
        学生在线请假 若信息合法则返回格式化的数据　反正返回None
        '''

        stuinfo=self.getstukey()
        if not stuinfo:
            return None
        stuinfo['Type']='leave'
        stuinfo['Prove']=raw_input('Please enter your proof of leave!')
        return stuinfo


    def checkin(self):
        stuinfo = studentcheckin().getstukey()
        if not stuinfo:
            return None
        stuinfo['Prove'] = raw_input('Please enter your proof of attendance!')
        return stuinfo


if __name__=='__main__':

    #studentcheckin().getstukey()
    studentcheckin().Insert_leave_record({'Prove':'asdadad','TeacherID':'2004633','ClassName':'软件工程1401','SeqNum':'2','StuID':'201416920106'})

