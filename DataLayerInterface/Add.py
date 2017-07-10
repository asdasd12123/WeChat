#coding=utf-8

import csv
from Read import Read

class Add(object):

    def add(self,filename,keylist=None):
        try:
            with open(filename, 'ab') as csv_file:

                if not keylist:
                    csv_file.close()
                    return True

                FIEDLS = keylist[0].keys()  #类变量记录列名
                writer = csv.DictWriter(csv_file,fieldnames=FIEDLS)
                for key in keylist:
                    writer.writerow(key)# 写数据
                csv_file.close()
                return True

        except IOError:
            print "File open error : " + filename + "\nplease check the filename"
            return False

if __name__=='__main__':
    read=Read().read('course.csv')
    Add().add('songjian123.csv',read)