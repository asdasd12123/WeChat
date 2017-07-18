#coding=utf-8
import csv


class Read(object):

    def read(self, filename, keylist=None):
        # 信息通配符 一次只能接受一个原子字典

        try:
            with open(filename, "rb") as csv_file:
                reader = csv.DictReader(csv_file)
                data = []
                for info in reader:
                    if not keylist or type(keylist) !=dict:
                        data.append(info)

                    else:
                        count = 0
                        for (key, item) in keylist.items():
                            if item is '*':
                                continue
                            elif item is '?':
                                count = 2
                            elif not info.has_key(key) or info[key] != item:
                                count = 1
                                break
                        if  count % 2 is 0:
                            data.append(info)
                        if count is 2:
                            break
                csv_file.close()
                return data

        except IOError:
            return []

if __name__=='__main__':
    key={'CwourseID': '1'}
    key1={'CwourseID':'?','TweacherID': '*'}
    key2={'CourseID': '?',
         'CourseName':'\xe6\x93\x8d\xe4\xbd\x9c\xe7\xb3\xbb\xe7\xbb\x9f\xe5\x8e\x9f\xe7\x90\x86',
         'TeacherID':'2004355'}
    read2 =Read().read('course.csv')
    print read2
    print '---------------------------------------------'
    read=Read().read("..\\InData\\studentInfo.csv",read2)
    print len(read)