#coding=utf-8

import csv
from Read import Read

class Write(object):

    def write(self,filename,keylist=None):
        try:
            with open(filename, 'wb') as csv_file:
                if not keylist:
                    csv_file.close()
                    return True

                FIEDLS = keylist[0].keys()  #类变量记录列名
                writer = csv.DictWriter(csv_file,restval='',fieldnames=FIEDLS)
                writer.writerow(dict(zip(FIEDLS, FIEDLS)))  # 写表头
                for key in keylist:
                    writer.writerow(key)# 写数据
                csv_file.close()
                return True

        except IOError:
            print "File open error : " + filename + "\nplease check the filename"
            return False

if __name__=='__main__':
    read=Read().read("course.csv")
    Write().write("songjian.csv",read)