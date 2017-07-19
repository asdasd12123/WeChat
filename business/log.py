# coding=utf-8
import datetime


class Log(object):

    def add(self, info):
        file = open('../InData/log.log','a')
        file.write('Time : '+str(datetime.datetime.now())[:-7]+'\n')
        for (key, item ) in info.items():
            file.write(key+' : '+item+' \n')
