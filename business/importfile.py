# coding=utf-8
import re
from dataoperation.manage import DataManage


class ImportFile(object):

    teacher_info = {"TeacherID":'^[\d]{7}$',
                            "TeacherName":r'^[\x80-\xff]{6,18}$',
                            "WeChatID":'^[a-zA-Z0-9_]+$'}

    course_info={"CourseID":'^[\d]{8}$',
                            "CourseName":'^[\x80-\xff]{6,18}$',
                            "TeacherID":'^[\d]{7}$',
                            "ClassName":'[\x80-\xff]+\d{4}$'}

    student_info={"StuID":'^[\d]{12}$',
                            "StuName":'^[\x80-\xff]{6,18}$',
                            "WeChatID":'^[a-zA-Z0-9_]+$',
                            "ClassID":'[\x80-\xff]+\d{4}$'}

    def stu_operation(self, out_file, path):
        data = DataManage(DataManage.target_info, args=(out_file,)).run()
        if not data:
            return None
        try:
            for line in data:
                line['FeaturePath'] = path+'/' + line['WeChatID'] + '_face.bin(jpg)'
        except KeyError:
            print '存在非法键值无法导入!'
            return False
        return data

    def course_operation(self, out_file, path=''):
        course_data = DataManage(DataManage.target_info, args=(out_file,)).run()

        if not course_data:
            return None

        new_data = []
        try:
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
                        dict_line = {}
                        dict_line['CourseID'] = line['CourseID']
                        dict_line['CourseName'] = line['CourseName']
                        dict_line['TeacherID'] = line['TeacherID']
                        dict_line['ClassName'] = class_name + str(i)
                        new_data.append(dict_line)
        except KeyError:
            print '存在非法键值无法导入!'
            return False
        return new_data

    def import_file(self,source_file,out_file, format={},Primary_key=[],operation=None,Path=''):
        if operation:
            data=operation(out_file,Path)
            if not data:
                print '文件不存在或与标准形式不符,请检查您的输入!'
                return False
        else:
            data = DataManage(DataManage.target_info, args=(out_file,)).run()
        error = DataManage(DataManage.format_check, args=(data, format)).run()
        if DataManage(DataManage.get_result, args=(error,)).run():
            for (key, item) in error.items():
                print key, item
            return False
        for key in Primary_key:
            DataManage(DataManage.update, args=(source_file, 'w', data, key)).run()
            data = DataManage(DataManage.target_info, args=(source_file,)).run()
        return True

    def import_stu(self, out):

        return self.import_file('../InData/studentInfo.csv', out,
                                self.student_info, [['StuID'], ['WeChatID']], self.stu_operation, 'D/:')

    def import_teacher(self, out):
        return self.import_file('../InData/teacherInfo.csv', out,
                                self.teacher_info, [['TeacherID'], ['WeChatID']])

    def import_class(self, out):
        return self.import_file('../InData/courseInfo.csv', out,
                                self.course_info, [['CourseID', 'ClassName']], self.course_operation)


if __name__=='__main__':
    #Update.creat_file('course.csv',Import_file.CourseInfo)
    #data=Query.QueryObjectInfo('../Indata/teacherInfo.csv')
    #print data
    #print Query.QueryObjectInfo('course.csv')
    #Import_file().import_stu('../InData/studentInfo.csv')
    Import_file().import_class('../InData/course.csv')