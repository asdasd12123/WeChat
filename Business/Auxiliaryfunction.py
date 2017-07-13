#coding=utf-8
from DataProcess.DataProcess import DataProcess
import time
'''

此模块对　出勤情况历史统计　出勤成绩输出　出勤情况随堂（实时）统计　学生信息维护　请假认定 考勤规则的指定

'''

class Auxiliaryfunction(object):

    def statistics_calculation(self,stuinfolist): #给定一定数量的学生考勤信息计算该信息内所有学生的考勤结果
        absencenum = 0  # 缺勤人数
        subnum = 0  # 提交人数
        appnum=0 #批准人数
        latenum = 0 #迟到人数
        earilynum=0 #早退人数
        normal=0 #正常人数
        absence = {}
        keys={'null':0,'normal':1,'Late':2,'leaveEarlier':3,'Absence':4,'Submitted':5,'approve':6}

        for stu in stuinfolist:
            info={}
            if absence.has_key(stu['StuID']):
                continue
            else:
                absence[stu['StuID']]=info

            if stu['checkinResult'] =='null':
                info['Type']='Absence'
            else:
                info['Type']='null'
            info['StuName']=DataProcess(target=DataProcess.QueryObjectInfo,
            args=('../InData/studentInfo.csv',{'StuID':stu['StuID']})).run()[0]['StuName']

        for stu in stuinfolist:
            info=absence[stu['StuID']]
            if keys[info['Type']]< keys[stu['checkinResult']]:
                if info['Type']=='null':
                    info['Type']=stu['checkinResult']
                elif info['Type']=='normal' or info['Type']=='Late':
                    if stu['checkinResult']=='Absence':
                        info['Type']='leaveEarlier'
                    else:
                        info['Type']=stu['checkinResult']
                elif info['Type']=='leaveEarlier' or info['Type']=='Absence':
                    if keys[stu['checkinResult']]>=5:
                        info['Type']=stu['checkinResult']
                    else:
                        continue
            else:
                continue
        allinfo = {}
        length = len(absence.keys())
        for (key, item) in absence.items():
            if item['Type'] == 'Late':
                latenum = latenum + 1
            elif item['Type'] == 'Submitted':
                subnum = subnum + 1
            elif item['Type'] =='Absence':
                absencenum=absencenum+1
            elif item['Type'] == 'normal':
                normal=normal+1
            elif item['Type']=='leaveEarlier':
                earilynum=earilynum+1
            elif item['Type']=='approve':
                appnum=appnum+1

            if item['Type']!='normal':
                allinfo[key] = item

        grade = 1.0 * normal / length * 100
        info={}
        info['checkin']=allinfo
        info['latenum']=latenum
        info['approve']=appnum
        info['subnum']=subnum
        info['length']=length
        info['leaveEarlier']=earilynum
        info['normal']=normal
        info['absence']=absencenum
        info['grade']=grade
        return info

    def dis_play(self,stuinfolist):  #自带格式化并显示考勤结果到终端
        checkinfo = self.statistics_calculation(stuinfolist)
        if not checkinfo:
            print '数据不合法无法进行计算!'
            return False
        print '最近一节课的出勤状况如下 :'
        print '考勤总人数:%d 正常考勤人数:%d 缺勤人数:%d 请假人数:%d 迟到人数:%d 早退人数:%d 出勤率%.2f %% ' % (
        checkinfo['length'],checkinfo['normal'],checkinfo['absence'], checkinfo['subnum']+checkinfo['approve'],
        checkinfo['latenum'],checkinfo['leaveEarlier'],checkinfo['grade'])
        if int(checkinfo['grade']) != 100:
            print '未出勤学生详细信息如下:'
            for (key, item) in checkinfo['checkin'].items():
                print '学号 : %-13s 姓名 : %-8s 考勤状况: %-12s ' % (key, item['StuName'], item['Type'])
        return True

    def view__time(self,key): #输入教师教工号和班级号的字典

        def operation(filename):
            if key['TeacherID'] in filename and key['ClassName'] in filename:
                return True
            return False

        filename=DataProcess(target=DataProcess.QueryNameByInfo,args=(operation,)).run()[-1]

        if not filename:
            print '您最近还没有进行过一次完整的考勤'
            return False
        stuinfo=DataProcess(target=DataProcess.QueryObjectInfo,args=(filename,)).run()
        return self.dis_play(stuinfo)


    def addset(self,key):
        info={}
        info['TeacherID']=key
        print 'Please enter the distance to start the check on how long it is to be (Company ：(0-20)minute)！'
        info['autolate']=self.getresult()
        print 'Please enter the distance to start the check on how long it is to be absence (Company :(0-20)minute)!'
        info['autoabsence']=self.getresult()

        if info['autolate']<=info['autoabsence']:
            print '缺勤的等待时间必须大于迟到的等待时间'
            return None

        print 'Please enter the distance to start the random check on how long it is to be late (Company ：(0-20)minute)！'
        info['randomlate'] = self.getresult()
        print 'Please enter the distance to start the random check on how long it is to be absence (Company :(0-20)minute)!'
        info['randomabsence'] = self.getresult()
        if info['randomlate']<=info['randomabsence']:
            print '缺勤的等待时间必须大于迟到的等待时间'
            return None

        info['Type']='False'
        return DataProcess(target=DataProcess.update,args=('../InData/set.csv','w',[info])).run()

    def read(self,key):
        rule=DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/set.csv',{'TeacherID':key,'Type':'True'})).run()
        if not rule:
            rule={'TeacherID':key,'autolate':'3','autoabsence':'3','randomlate':'3','randomabsence':'3','Type':'True'}
            print '您当前使用的是默认规则!'
        return rule

    def ruleset(self,key):
        rules = DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/set.csv', {'TeacherID': key})).run()
        if not rules:
            print '您当前没有创建自定义规则'
            return False
        print '请输入您需要选择的规则序号'
        for rule in rules:
            print rule

        index=input()
        if index<1 or index>len(rules):
            print '您输入的结果不合法'
            return False

        for rule in rules:
            if rule['TeacherID'] == rules[index-1]['TeacherID']:
                rule['Type']='True'
            else:
                rule['Type']='False'

        return DataProcess(targe=DataProcess.update,args=('../I-nData/set.csv','w',rules)).run()



    def getresult(self):
        while True:
            num=raw_input()
            try:
                num=float(num)
            except TypeError and ValueError:
                print 'You have entered an invalid format. Please enter a floating point number!'
                continue

            if num<=0 or num>20 :
                print 'Exceeded maximum accommodation !'
                time.sleep(1)
            else:
                return  num

    def historical_statistics(self,key): #这里的键值包括TeacherID和老师要统计的班级和次序号

        def operation(line):
            if key['TeacherID'] in line and key['ClassName'] in line and key['SeqNum'] in line:
                return True
            return False

        filename=DataProcess(target=DataProcess.QueryNameByInfo,args=(operation,)).run()[0]
        if not filename:
            print '无法计算该次考勤的结果'
            return False
        stuinfo=DataProcess(target=DataProcess.QueryObjectInfo,args=(filename,)).run()
        allstuinfo=self.statistics_calculation(stuinfo)
        for (key,item) in allstuinfo['checkin'].items():
            if item['Type']=='Submitted':
                self.Take_leave_absence(filename,{'StuID':key})
        return True



    def Take_leave_absence(self,filename,stuID): #请假认定
        stuinfo=DataProcess(target=DataProcess.QueryObjectInfo,args=(filename,stuID)).run()[0]
        print '学号：'+ stuinfo['StuID']+'   该学生的请假证明路径为 : '+stuinfo['ProofPath']
        while True:
            num=raw_input('是否批准该学生的假条 ? yes or no \n')
            if num=='yes':
                stuinfo['IsSucc']='True'
                stuinfo['checkinResult']='approve'
                DataProcess(target=DataProcess.update,args=(filename,'w',[stuinfo],['StuID','checkstartTime'])).run()
                break
            elif num=='no':
                stuinfo['IsSucc'] = 'True'
                stuinfo['checkinResult'] = 'Absence'
                DataProcess(target=DataProcess.update,
                            args=(filename, 'w', [stuinfo], ['StuID', 'checkstartTime'])).run()
                break
            else:
                print '请输入标准的选项!'
                time.sleep(1)
                continue






if __name__=='__main__':
    #Auxiliaryfunction().addset('asdasd')
    #Auxiliaryfunction().ruleset('asdasd')
    #print Auxiliaryfunction().read('asdasd')
    Auxiliaryfunction().view__time({'TeacherID':'2004633','ClassName':"软件工程1401"})
    Auxiliaryfunction().historical_statistics({'TeacherID':'2004633','ClassName':'软件工程1401','SeqNum':'1'})
    Auxiliaryfunction().view__time({'TeacherID':'2004633','ClassName':"软件工程1401"})
