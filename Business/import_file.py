#coding=utf-8
from DataProcess.Update import Update
from DataProcess.Check import Check
from DataProcess.Query import Query
import re

class Import_file(object):
    TeacherInfo={"TeacherID":'^[\d]{7}$',
                           "TeacherName":r'^[\x80-\xff]{6,18}$',
                           "WeChatID":'^[a-zA-Z0-9_]+$'}

    CourseInfo={"CourseID":'^[\d]{8}$',
                           "CourseName":'^[\x80-\xff]{6,18}$',
                           "TeacherID":'^[\d]{7}$',
                           "ClassNums":'[\x80-\xff]+\d{4}$'}

    StudentInfo={"StuID":'^[\d]{12}$',
                           "StuName":'^[\x80-\xff]{6,18}$',
                           "WeChatID":'^[a-zA-Z0-9_]+$',
                           "ClassID":'[\x80-\xff]+\d{4}$'}

    def Stu_Operation(self,out_file,path):
        data=Query.QueryObjectInfo(out_file)
        if not data:
            return None
        for line in data:
            line['FeaturePath'] = path+'/' + line['WeChatID'] + '_face.bin(jpg)'
        return data

    def Course_operation(self,out_file,path=''):
        course_data = Query.QueryObjectInfo(out_file)
        new_data=[]
        for line in course_data:
            major = line['ClassNums']
            info = major.split(',')
            for inf in info:
                class_info = re.findall(r'\d+', inf)
                class_interval = len(class_info)
                if class_interval == 0:
                    continue
                else:
                    begin = int(class_info[0])
                    end = int(class_info[-1])

                major_info = re.findall('[^-0-9]+', inf)  # 匹配非数字和 -
                class_name = major_info[0]

                for i in range(begin, end + 1):
                    # ['CourseID', 'CourseName', 'TeacherID', 'ClassNums']
                    dict_line = {}
                    dict_line['CourseID'] = line['CourseID']
                    dict_line['CourseName'] = line['CourseName']
                    dict_line['TeacherID'] = line['TeacherID']
                    dict_line['ClassNums'] = class_name + str(i)
                    new_data.append(dict_line)
        return new_data

    def import_file(self,UserID,source_file,out_file,format=[],Primary_key=[],operation=None,Path=''):
        if Query.QueryPermisson(UserID,source_file) !=6:
            print 'You have no right to operate on this file ！'
            return False

        data=[]
        if operation:
            data=operation(out_file,Path)
        else:
            data=Query.QueryObjectInfo(out_file)
        error=Check.formatcheck(data,format)
        if Check.getresult(error):
            print error
            return False
        return Update.update(source_file,'w',data,Primary_key)


if __name__=='__main__':
    #Update.creat_file('course.csv',Import_file.CourseInfo)
    #data=Query.QueryObjectInfo('../Indata/teacherInfo.csv')
    #print data
    #print Query.QueryObjectInfo('course.csv')
    '''if Update.update('a.csv','w',data,['TeacherID']):
        print 'success'
    else:
        print 'failed' '''

    if Import_file().import_file({'root':'0'},'b.csv','../Indata/studentInfo.csv',Import_file.StudentInfo, \
                        ['CourseID','WeChatID'],Import_file().Stu_Operation,'D:/'):
        print 'success'
    else:
        print 'failed'

    #Import_file().import_file({'root':'0'},'b.csv','../Indata/studentInfo.csv',Import_file.CourseInfo, \
                        #['CourseID','ClassNums'],Import_file().Course_operation)

    #Import_file().import_file({'root':'0'},'d.csv','../Indata/teacherInfo.csv',Import_file.TeacherInfo,[])

