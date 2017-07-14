#coding=utf-8
from DataProcess.DataProcess import DataProcess
import re
from Auxiliaryfunction import  Auxiliaryfunction

class sum_table(object):

    def __init__(self,key):
        self.filename=None
        self.key=key #包括老师ID 班级号 统计次数

    def creat_sum(self):
        if not self.init():
            print '初始化失败请检查您的键值是否正确!'
            return False

        filename = '../InData/' + self.key['TeacherID'] + '_' + self.key['ClassName'] + '_' + self.key['SeqNum']+'_Detail.csv'
        stulist=DataProcess(target=DataProcess.QueryObjectInfo,args=('..\InData\studentInfo',)).run()
        print stulist
        if not stulist:
            print '该次的考勤信息不存在!请检查您的键值'
            return False
        olddata=DataProcess(target=DataProcess.QueryObjectInfo,args=(self.filename,)).run()
        DataProcess(target=DataProcess.update,args=(self.filename,'dl',olddata,['StuID'])).run()
        stulist=Auxiliaryfunction().historical_statistics(self.key)
        print stulist
        for line in olddata:
            line['check'+self.key['SeqNum']]='normal'
            for (key,item) in stulist['checkin'].items():
                if line['StuID']==key:
                    line['check'+self.key['SeqNum']]=item['Type']

        return DataProcess(target=DataProcess.update,args=(self.filename,'w',olddata)).run()



    def init(self):
        filename='../InData/'+self.key['TeacherID']+'_'+self.key['ClassName']+'_'+'Sum.csv'
        if not DataProcess(target=DataProcess.QueryObjectKey,args=(filename,)).run():
            sum=[]
            stulist=DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/studentInfo.csv',{'ClassID':self.key['ClassName']})).run()
            for key in stulist:
                sumdict = {}
                sumdict['StuID']=key['StuID']
                sum.append(sumdict)
            return DataProcess(target=DataProcess.update,args=(filename,'w',sum)).run()

        return True


if __name__=='__main__':
    sum_table({'TeacherID':'2004633','ClassName':"软件工程1401",'SeqNum':'2'}).creat_sum()
