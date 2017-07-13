#coding=utf-8
from DataProcess.DataProcess import DataProcess
import time
'''

此模块对　出勤情况历史统计　出勤成绩输出　出勤情况随堂（实时）统计　学生信息维护　请假认定 考勤规则的指定

'''

class Auxiliaryfunction(object):

    def Historical_statistics(self,stuinfolist): #给定一定数量的学生考勤信息计算该信息内所有学生的考勤结果
        num = 0  # 缺勤人数
        leave = 0  # 请假人数
        latenum = 0
        absence = {}
        for stu in stuinfolist:
            info = {}
            if absence.has_key(stu['StuID']) and absence[stu['StuID']]['Type'] == 'leave':
                continue
            elif absence.has_key(stu['StuID']) and stu['checkinResult'] == 'Submitted':
                absence[stu['StuID']]['Type'] = 'leave'
            elif absence.has_key(stu['StuID']) and absence[stu['StuID']]['Type'] == 'Absence':
                continue
            elif absence.has_key(stu['StuID']) and absence[stu['StuID']]['Type'] == 'Late':
                continue
            else:
                absence[stu['StuID']] = info
                if stu['checkinResult'] == 'null':
                    info['Type'] = 'Absence'
                else:
                    info['Type'] = stu['checkinResult']
                info['StuName'] = DataProcess(target=DataProcess.QueryObjectInfo,
                                              args=('../InData/studentInfo.csv', {'StuID': stu['StuID']})).run()[0][
                    'StuName']
        allinfo = {}
        length = len(absence.keys())
        for (key, item) in absence.items():
            info = {}
            if item['Type'] == 'Late':
                latenum = latenum + 1
                info = item
            elif item['Type'] == 'leave':
                leave = leave + 1
                info = item
            elif item['Type'] == 'Absence':
                num = num + 1
                info = item
            if info:
                allinfo[key] = info

        grade = 1.0 * (length - (latenum + leave + num)) / length * 100
        return {'checkinfo':allinfo,'abnum':num,'leave':leave,'length':length,'grade':grade,'late':latenum}


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
        checkinfo=self.Historical_statistics(stuinfo)
        print '最近一节课的出勤状况如下 :'
        print '总人数:%d 缺勤人数:%d 请假人数:%d 迟到人数:%d 出勤率%.2f %% ' %(checkinfo['length'],checkinfo['abnum'],checkinfo['leave'],checkinfo['late'],checkinfo['grade'])
        if int(checkinfo['grade'])!=100:
            print '未出勤学生详细信息如下:'
            for (key,item) in checkinfo['checkinfo'].items():
                print '学号 : %-13s 姓名 : %-8s 考勤状况: %-12s ' %(key,item['StuName'],item['Type'])
        return True


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

if __name__=='__main__':
    #Auxiliaryfunction().addset('asdasd')
    #Auxiliaryfunction().ruleset('asdasd')
    #print Auxiliaryfunction().read('asdasd')
    Auxiliaryfunction().view__time({'TeacherID':'2004633','ClassName':'软件工程1401'})