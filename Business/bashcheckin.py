#coding=utf-8
import datetime
import ConfigParser
import re
from maintain import maintain
from DataProcess.DataProcess import DataProcess
import random
import time

class bashcheckin(object):

    def __init__(self,key):
        self.counter = {'auto': {}, 'random': {}}
        self.status = False
        self.random_info = []
        self.time=int(maintain().readRult(key)['bufferTime'])*60
        self.start_time =None
        self.start=datetime.datetime.now()
        self.end_time=None
        self.key=key
        self.filename=None
        cf = ConfigParser.ConfigParser()
        cf.read('../InData/settings.ini')
        info = map((lambda x: re.split('-|:', x[1])), cf.items('sectime'))
        self.Timeinfo = map((lambda x: [int(x[0]) * 3600 + int(x[1]) * 60, int(x[2]) * 3600 + int(x[3]) * 60]), info)

    def getTime(self):
        localtime = time.localtime()[3] * 3600 + time.localtime()[4] * 60 + time.localtime()[5]
        for Time in self.Timeinfo:
            if localtime >= Time[0] - self.time -300 and localtime <= Time[1] - self.time +300:
                if localtime>=Time[0] -self.time and localtime <= Time[1]-self.time:
                    self.end_time = Time[1]
                    self.start_time = localtime
                    return True
                elif localtime >= Time[0] - self.time - 300 and localtime <Time[0]-self.time:
                    print '据可开始考勤的时间还有%d秒,你可设置考勤缓冲提前开始考勤!' % (Time[0] - self.time - localtime)
                elif localtime <= Time[1] - self.time + 300 and localtime>Time[1]-self.time:
                    print '您已超过考勤缓冲有效范围%d秒,此时给学生上传信息的时间不足所以无法开启,你可设置考勤缓冲设置调整此设置' % (localtime-Time[1] +self.time)
                return False
        print '当前不是有效时间无法开启考勤!'
        return False


    def Initialization(self, stu_info_list, type):
        '''
        格式化初始数据　
        '''
        info = []
        for line in stu_info_list:
            data = {}
            if type!='man':
                self.counter[type][line['StuID']] = 5
            data['StuID'] = line['StuID']
            data['checkTime'] = 'null'
            data['ProofPath'] = 'null'
            data['checkinType'] = type
            data['IsSucc'] = 'False'
            if type=='man':
                sel=raw_input('当前学生学号:'+data['StuID']+' 请输入您的选项!')
                keys = {'1':'normal','2':'Late','3':'leaveEarlier','4':'Absence','5':'approve'}
                if sel in list('12345'):
                    data['checkinResult'] = keys[sel]
                else:
                    print '您输入了非法选项默认该学生为缺勤!'
                    data['checkinResult'] = keys['4']
                print '学号为 : %s 的考勤状态设定完毕 为 :%s' %(data['StuID'],data['checkinResult'])
            else:
                data['checkinResult'] = 'Absence'
            info.append(data)
        return info


    def getseqnum(self):
        seqinfo=DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/seq.csv',{'TeacherID':self.key['TeacherID'],'ClassID':self.key['ClassID']})).run()
        if not seqinfo:
            return '1'
        return str(int(seqinfo[-1]['SeqID'])+1)

    def get_seqinfo(self):
        seqinfo = {'TeacherID': self.key['TeacherID'], 'ClassID': self.key['ClassID']}
        seqnum = self.getseqnum()
        self.filename = '../InData/'+self.key['TeacherID'] + '_' + self.key['ClassID'] + '_' + seqnum + '_Detail.csv'
        seqinfo['StartTime'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        seqinfo['SeqID'] = self.getseqnum()
        return seqinfo

    def write_seq(self):
        if not DataProcess(target=DataProcess.QueryObjectKey,args=('../InData/seq.csv',)).run():
            print 'The system creates the seq.csv file automatically！'
        return DataProcess(target=DataProcess.update,
        args=('../InData/seq.csv', 'a', [self.get_seqinfo()])).run()

    def randomstulist(self):
        stulist = []
        studentlist = DataProcess(target=DataProcess.QueryObjectInfo,
        args=('../InData/studentInfo.csv', {'ClassID': self.key['ClassID']})).run()
        while True:
            num=raw_input('请输入需要抽点的百分比!')
            try:
                num=float(num)
            except TypeError and ValueError:
                print '您的输入不符合规则,请重新输入!'
                continue

            if num<=0 or num>100 or int(len(studentlist) * num / 100)==0:
                print '抽点的数量大于或小于当前学生的数量请重新输入!'
                time.sleep(1)
            else:
                num = int(len(studentlist) * num / 100)
                print '抽点完成您此时共抽点了%-3d名学生!' %(num)
                break

        while len(stulist)!=num:
            index=random.randint(0,len(studentlist)-1)
            if studentlist[index] not in stulist:
                stulist.append(studentlist[index])
        return stulist

    def auto_cal(self, stu_info):

        if self.counter['auto'][stu_info['StuID']] == 0:
            print '您当前进行自动考勤次数已经用完无法考勤!'
            return False

        self.counter['auto'][stu_info['StuID']] = self.counter['auto'][stu_info['StuID']] - 1
        data = DataProcess(target=DataProcess.QueryObjectInfo,
        args=(self.filename, {'checkinType': 'auto', 'StuID': stu_info['StuID']})).run()[0]

        if data['IsSucc'] == 'True':
            print '您已经完成自动考勤无法再次考勤!'
            return False

        data['checkTime'] = datetime.datetime.now()
        data['ProofPath'] = stu_info['ProofPath']
        num = random.randint(0, 1)
        if num:
            data['IsSucc'] = 'True'
            seconds = (data['checkTime'] - self.start).seconds
            if seconds <=  self.time:
                print '考勤成功!'
                data['checkinResult'] = 'normal'
            else:
                print '考勤有效时间已过您当前为迟到!'
                data['checkinResult'] = 'Late'
        else:
            print '身份验证失败！ 您还有 %d 次机会 ' % (self.counter['auto'][stu_info['StuID']])
        data['checkTime'] = str(datetime.datetime.now())[:-7]
        return DataProcess(target=DataProcess.update,
        args=(self.filename, 'w', [data],['StuID','checkinType'])).run()

    def random_cal(self, stu_info):

        if self.counter['random'][stu_info['StuID']] == 0:
            print '您当前进行随机考勤次数已经用完无法考勤!'
            return False
        data = DataProcess(target=DataProcess.QueryObjectInfo,
        args=(self.filename, {'checkinType': 'random', 'StuID': stu_info['StuID']})).run()

        self.counter['random'][stu_info['StuID']] = self.counter['auto'][stu_info['StuID']] - 1

        if data[-1]['IsSucc'] == 'True':
            print '您已经完成随机考勤无法再次考勤'
            return False
        DataProcess(target=DataProcess.update, args=(self.filename, 'dl', data, ['StuID', 'checkinType'])).run()
        data[-1]['ProofPath'] = stu_info['ProofPath']
        num = random.randint(0, 1)
        if num:
            data[-1]['IsSucc'] = 'True'
            print '随机考勤成功!'
            data[-1]['checkinResult'] = 'normal'
        else:
            print '身份验证失败！ 您还有 %d 次机会 ' % (self.counter['random'][stu_info['StuID']])
        data[-1]['checkTime'] = str(datetime.datetime.now())[:-7]
        return DataProcess(target=DataProcess.update, args=(self.filename, 'a', data)).run()
