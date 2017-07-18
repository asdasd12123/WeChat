#coding=utf-8

import csv
import collections

from read import Read


class Write(object):

    def write(self, filename, keylist=None):
        try:
            with open(filename, 'wb') as csv_file:
                if not keylist:
                    csv_file.close()
                    return True

                def num(string):
                    count = 0
                    for n in string:
                        count = count + ord(n)
                    return count

                error = []

                for key in keylist:
                    d = collections.OrderedDict()
                    key = sorted(key.items(), key=lambda d: num(d[0]))
                    for k in key:
                        d[k[0]] = k[1]
                    error.append(d)

                keylist = error

                FIEDLS = keylist[0].keys()  # 类变量记录列名
                writer = csv.DictWriter(csv_file,restval='',fieldnames=FIEDLS)
                writer.writerow(dict(zip(FIEDLS, FIEDLS)))  # 写表头
                for key in keylist:
                    writer.writerow(key)  # 写数据
                csv_file.close()
                return True

        except IOError:
            print "File open error : " + filename + "\nplease check the filename"
            return False

