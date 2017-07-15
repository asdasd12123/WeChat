#coding=utf-8
from DataProcess.DataProcess import DataProcess
'''
此模块对　出勤情况历史统计　出勤成绩输出　出勤情况随堂（实时）统计　学生信息维护　请假认定 考勤规则的指定
'''

class Auxiliaryfunction(object):

    def __calculation(self,absence): #子计算
        absencenum = 0  # 缺勤人数
        subnum = 0  # 请假提交人数
        appnum = 0  # 请假批准人数
        latenum = 0  # 迟到人数
        earilynum = 0  # 早退人数
        normal = 0  # 正常人数
        allinfo = {}
        length = len(absence.keys())
        for (key, item) in absence.items():
            if item['Type'] == 'Late':
                latenum = latenum + 1
            elif item['Type'] == 'Submitted':
                subnum = subnum + 1
            elif item['Type'] == 'Absence':
                absencenum = absencenum + 1
            elif item['Type'] == 'normal':
                normal = normal + 1
            elif item['Type'] == 'leaveEarlier':
                earilynum = earilynum + 1
            elif item['Type'] == 'approve':
                appnum = appnum + 1

            if item['Type'] != 'normal':
                allinfo[key] = item

        grade = 1.0 * normal / length * 100
        info = {}
        info['checkin'] = allinfo
        info['latenum'] = latenum
        info['approve'] = appnum
        info['subnum'] = subnum
        info['length'] = length
        info['leaveEarlier'] = earilynum
        info['normal'] = normal
        info['absence'] = absencenum
        info['grade'] = grade
        return info



    def statistics_calculation(self,stuinfolist): #给定一定数量的学生考勤信息计算该信息内所有学生的考勤结果
        absence = {}
        keys={'null':0,'normal':1,'Late':2,'leaveEarlier':3,'Absence':4,'Submitted':5,'approve':6}

        for stu in stuinfolist:
            info={}
            if absence.has_key(stu['StuID']):
                continue
            else:
                absence[stu['StuID']] = info
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
                    info['Type'] = stu['checkinResult']
            else:
                if info['Type']=='Absence':
                    if stu['checkinResult']=='normal' or  stu['checkinResult']=='Late':
                        info['Type']='Late'
                continue

        return self.__calculation(absence)

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









if __name__=='__main__':
    #Auxiliaryfunction().addset('asdasd')
    #Auxiliaryfunction().ruleset('asdasd')
    #print Auxiliaryfunction().read('asdasd')
    Auxiliaryfunction().view__time({'TeacherID':'2004633','ClassID':"软件工程1401"})
    #Auxiliaryfunction().historical_statistics({'TeacherID':'2004633','ClassName':'软件工程1401','SeqNum':'1'})
    #Auxiliaryfunction().view__time({'TeacherID':'2004633','ClassName':"软件工程1401"})
