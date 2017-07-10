#coding=utf-8
from DataProcess.Query import Query

'''
在此模块中学生进行考勤　请假 　
'''
class studentcheckin(object):

    def studealy(self,stukey,leaveProve):
        '''
        学生请假 若信息合法则返回格式化的数据　反正返回None
        '''
        stuinfo=Query.QueryObjectInfo("",stukey)
        if not stuinfo:
            print 'Identity failed!'
            return None

        stukey['leaveProve']=leaveProve
        return stuinfo


    def checkin(self,stukey,type,prove):
        '''
        学生响应总考勤
        '''
        if type not in ['auto','random']:
            print 'Checking attendance is wrong!'
            return False

        stuinfo = Query.QueryObjectInfo("", stukey)
        if not stuinfo:
            print 'Identity failed!'
            return None

        stukey['Prove'] = prove
        stukey['type']=type
        return stuinfo


if __name__=='__main__':
    key={'StuID':'201416920220'}
