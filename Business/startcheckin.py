#coding=utf-8
import threading
import os
import signal
import datetime
import random
import time
from    DataProcess.Update  import Update

'''为了简化自动考勤的操作 对自动考勤进行简化 不对数据的有效性进行分析 假设数据全是有效的 不对时间进行分析假设时间全是有效的 具体的验证放到业务校验模块
    业务校验模块是与界面层的接口
'''

class Checkin(object):
    def __init__(self,studentinfolist,filename):
        self.info =self.Initialization(studentinfolist)
        self.count=0
        self.status=False
        self.startTime=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.filename=filename

    def Calculation(self,studentfio,path):
        pass

    def Initialization(self,studentinfolist,):
        info=[]
        keys = ['StuID', 'checkTime', 'ProofPath', 'checkinType', 'IsSucc', 'checkinResult']
        for line in studentinfolist:
            data = {}
            data['StuID'] = line['StuID']
            data['checkTime'] = 'null'
            data['ProofPath'] = 'null'
            data['checkinType'] = 'null'
            data['IsSucc'] = 'null'
            data['checkinResukt'] =str(random.randint(0,1))
            info.append(data)
        return info

    def receive(self,studentinfo,path):  #此函数会计算考勤结果 此函数待后续在写
        for line in self.info:
            if line['StuID']==studentinfo['StuID']:
                if line['IsSucc']!='null':
                    print 'studeng '+line['StuID']+' have checkin!'
                    return False
                line['checkTime']=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                line['checkinType']='auto'
                line['ProofPath']=path
                line['IsSucc']='True'
                self.Calculation(studentinfo,path)
        return True


class autothread(Checkin):

    def run(self,Time):
        time.sleep(Time)
        Update.update(self.filename,'w',self.info)
        self.status=False

    def start(self,Time):
        t=threading.Thread(target=autothread.run,args=(self,Time,))
        t.start()

class randomthread(Checkin):

    '''该线程有个两个子线程 和一个状态变量 平时只运行第一个状态变量 当参数修改时 运行第二个状态变量'''
    def run(self,count):
        time.sleep(5)
        if self.count==count:
            Update.update(self.filename, 'w', self.info)
            self.status = False

    def new_start(self,studentinfolist,filename):
        if self.status:
            Update.update(filename,'a',self.info)
        self.count=self.count+1
        self.info=self.Initialization(studentinfolist)
        self.start()


    def start(self):
        t = threading.Thread(target=randomthread.run, args=(self,self.count,))
        t.start()



class checkinNode(object):
    def __init__(self,key):  #主键就是课程号加上班级号　若不存在则无法签到
        self.auto=None
        self.random=None
        self.key=key

    def creatauto(self,studentlist,filename,time):
        if self.auto or self.auto.status:
            print 'There are currently automatic attendance Windows that cannot be created again !'
            return False
        self.auto=autothread(studentlist,filename)
        self.auto.start(time)
        self.auto.status=True
        return True

    def creatrandom(self,studentlist,filename):
        if not self.auto or not  self.auto.status:
            print 'Currently the attendance node does not open automatic attendance is unable to open random check on work attendance !'
            return False
        if self.random:
            print 'There are currently automatic attendance Windows that cannot be created again !'
            return False
        self.random=randomthread(studentlist,filename)
        self.random.start()
        self.random.status=True
        return True

    def random_new_start(self,studentlist,filename):
        self.random.newstart(self,studentlist,filename)

    def autoreceive(self,student,path):
        self.auto.receive(student,path)

    def randomreceive(self,student,path):
        self.random.reveive(student,path)

    def creatManualAttendance(self,studentinfolist):
        pass

    def getTime(self):
        pass

class startcheckin(object):
    def __init__(self):
        self.list=[]

    def remove(self):
        while True:
            for line in self.list:
                if not line.auto.status and not line.random.status:
                    self.list.remove(line)
                    time.sleep(1)

    def append(self,argu):
        self.list.append(argu)

def my(pid):
    time.sleep(10)
    os.kill(pid,signal.SIGTERM)

if __name__=='__main__':
    s=startcheckin()
    pid = os.getpid()
    thread = threading.Thread(target=startcheckin.remove, args=(s,))
    thread2 = threading.Thread(target=my, args=(pid,))
    thread.start()
    thread2.start()
    while True:
        Stu=[]
        c=checkinNode('hhh')
        for index in range(10):
            stu={'StuID':str(index)}
            Stu.append(stu)
        c.creatauto(Stu,'a.csv')
        c.autostart(8)
        for index in range(10):
            stu={'StuID':str(random.randint(0,9))}
            c.autoreceive(stu,str(random.randint(0,1000)))
        s.append(c)
        time.sleep(8)




