#coding=utf-8
from DataProcess.Query import Query

'''
在此模块中学生进行考勤　请假 　
'''

class studentcheckin(object):

    def getstukey(self):
        stukey = {}
        stukey['StuID'] = raw_input('Please input your student number！')
        stukey['ClassID'] = raw_input('Please input your class!')
        stuinfo = Query.QueryObjectInfo('../InData/studentInfo.csv', stukey)
        if not stuinfo:
            print 'Identity failed!'
            return None
        return stuinfo[0]


    def studealy(self):
        '''
        学生请假 若信息合法则返回格式化的数据　反正返回None
        '''

        stuinfo=self.getstukey()
        if not stuinfo:
            return None
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
    studentcheckin().checkinauto()
