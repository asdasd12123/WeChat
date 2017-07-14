#coding=utf-8
from abc import ABCMeta, abstractmethod
import threading
import datetime
import random
import time
from DataProcess.DataProcess  import DataProcess


'''为了简化考勤的操作 对考勤进行简化 不对数据的有效性进行分析 假设数据全是有效的 不对时间进行分析假设时间全是有效的 具体的验证放到业务校验模块
    业务校验模块是与界面层的接口
'''

class Checkin(object):
    '''
    考勤类是自动考勤和随机考勤的父类　
    '''

    __metaclass__ = ABCMeta

    def __init__(self,studentinfolist,filename,rule):
        self.counter=None
        self.info =self.Initialization(studentinfolist)
        self.count=0
        self.status=False
        self.rule=rule
        self.startTime=datetime.datetime.now()
        self.filename=filename
        self.type=None

    def Calculation(self,line,studentfio):
        '''
        通过对学生发送的信息进行计算　可以接收考勤信息和请假休息
        此函数具有局限性　只能对单次具体的考勤窗口进行计算　但是无法对所有的整体结果进行计算　所以全局性的计算放到其它窗口
        '''

        self.counter[line['StuID']]=self.counter[line['StuID']]-1
        line['checkTime'] = datetime.datetime.now()
        line['ProofPath'] =studentfio['Prove']
        if studentfio.has_key('leave'):
            line['checkinType']='leave'
            line['IsSucc']='True'
            line['checkinResult']='Submitted'
            line['checkTime'] = str(datetime.datetime.now())[:-7]
            return line

        line['checkinType']=self.type
        num=random.randint(0,1)
        if num:
            line['IsSucc'] = 'True'
            seconds=(line['checkTime'] - self.startTime).seconds
            if seconds<=int(self.rule['late'])*60:
                print 'Successful attendance'
                line['checkinResult']='normal'
            elif seconds>int(self.rule['late'])*60 and seconds <=int(self.rule['absence'])*60:
                print 'You are Late！'
                line['checkinResult'] = 'Late'
            else:
                print 'I\'m sorry, but you have been certified absent!'
                line['checkinResult'] = 'Absence'
        else:
            print 'Invalid attendance certificate！ 您还有 %d 次机会 ' %(self.counter[line['StuID']])
        line['checkTime'] = str(datetime.datetime.now())[:-7]
        return line

    def Initialization(self,studentinfolist):
        '''
        格式化初始数据　
        '''
        info=[]
        self.counter={}
        for line in studentinfolist:
            data = {}
            self.counter[line['StuID']]=5
            data['StuID'] = line['StuID']
            data['checkstartTime']=str(datetime.datetime.now())[:-7]
            data['checkTime'] = 'null'
            data['ProofPath'] = 'null'
            data['checkinType'] = 'null'
            data['IsSucc'] = 'False'
            data['checkinResult'] ='Absence'
            info.append(data)
        return info

    def receive(self,studentinfo):  #此函数会计算考勤结果 此函数待后续在写
        if not self.status:
            print 'The time window is closed and unable to receive attendance information！'
            return False

        for line in self.info:
            if line['StuID']==studentinfo['StuID']:
                if not self.counter[studentinfo['StuID']]:
                    print line['StuID']+' :您当前已经用完了考勤次数用完无法考勤'
                    return False
                if line['IsSucc']=='True':
                    print '该账户已经完成考勤!'
                    return False
                self.info[self.info.index(line)]= self.Calculation(line,studentinfo)
                return True
        print 'The information you entered does not belong to the check in window or the check in window has not been opened yet！'
        return False


    @abstractmethod
    def start(self,*args):
        pass

    @abstractmethod
    def run(self,*args):
        pass


class autothread(Checkin):

    '''
    自动考勤类
    '''

    def run(self,Time):
        time.sleep(Time)
        DataProcess(target=DataProcess.update,args=(self.filename,'a',self.info)).run()
        self.status=False

    def start(self,Time):
        t=threading.Thread(target=autothread.run,args=(self,Time,))
        t.start()


class randomthread(Checkin):

    '''该线程有个两个子线程 和一个状态变量 平时只运行第一个状态变量 当参数修改时 运行第二个状态变量'''
    def run(self,count,Time):
        time.sleep(Time)
        if self.count==count:
            DataProcess(target=DataProcess.update,args=(self.filename, 'a', self.info)).run()
            self.status = False


    def new_start(self,studentinfolist,filename,Time):
        if self.status:
            DataProcess(target=DataProcess.update, args=(self.filename, 'a', self.info)).run()
        self.count=self.count+1
        self.info=self.Initialization(studentinfolist)
        self.start(Time)


    def start(self,Time):
        t = threading.Thread(target=randomthread.run, args=(self,self.count,Time))
        t.start()





