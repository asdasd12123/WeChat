#coding=utf-8
from bashcheckin import bashcheckin
from DataProcess.DataProcess import DataProcess

class checkinNode(bashcheckin):

    def startauto(self):
        if self.status:
            print ' 当前已经存在自动考勤窗口无法再次开启!'
            return False
        if not self.getTime():
            print '当前不是有效时间无法开启考勤!'
            return False
        stu_list = DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/studentInfo.csv', {'ClassID': self.key['ClassID']})).run()
        self.write_seq()
        stu_list=self.Initialization(stu_list,'auto')
        self.status=True
        return DataProcess(target=DataProcess.update,
        args=(self.filename,'w',stu_list)).run()


    def startrandom(self):
        if not self.status:
            print ' 当前没有开启自动考勤无法进行抽点考勤!'
            return False
        self.random_info =self.randomstulist()
        stu_list=self.Initialization(self.random_info,'random')
        return DataProcess(target=DataProcess.update,
        args=(self.filename, 'a',stu_list)).run()


    def receive(self,stuinfo):
        if stuinfo['Type']=='auto':
            return self.auto_cal(stuinfo)
        else:
            return self.random_cal(stuinfo)


    def manCheckin(self):  # 手动考勤

        if self.getTime():
            print '当前是上课时间无法开启手动考勤!'
            return False

        stuinfo = DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/studentInfo.csv',{'ClassID': self.key['ClassID']})).run()

        if not stuinfo:
            print '当前班级不存在请重新输入!'
            return False

        self.write_seq()
        print '请按照以下选项输入状态 非法输入默认为缺勤!'
        print ' 1　正常　2　迟到　３　早退　４　缺勤 5　请假已批准'
        stulist=self.Initialization(stuinfo,'man')
        return DataProcess(target=DataProcess.update,
        args=(self.filename, 'w', stulist)).run()




if __name__=='__main__':
    c=checkinNode({'TeacherID':'2004633','ClassID':'软件工程1401'})
    #c.startauto()
    key = {'Type':'auto','StuID': '201416920106', 'ClassID': '软件工程1401', 'ProofPath': 'adadadasdasdasdasd'}
    key3 = {'StuID': '201416920105', 'ClassID': '软件工程1401', 'ProofPath': 'asdxcxz'}
    key2 = {'Type':'random','StuID': '201416920106', 'ClassID': '软件工程1401', 'ProofPath': 'adadadasdasdasdasd'}
    #c.startrandom()
    #print c.random_info
    '''c.receive(key)
    c.receive(key2)
    c.receive(key2)
    c.receive(key2)
    c.receive(key)
    c.startrandom()
    c.receive(key2)
    c.receive(key)
    c.receive(key2)
    c.receive(key)
    c.startrandom()
    c.receive(key2)
    c.receive(key)
    c.receive(key2)
    #c.receive(key2)'''
    #c.manCheckin()











