# coding=utf-8
import os
import re

from database.database import DataAPI

class Query(object):

    '''查询目标信息通过不同的参数达到查询不同的效果 '''

    @staticmethod
    def query_target_keys(object):
        '''返回目标的键 也可查询含有合法信息的文件是否存在 若不存在则返回None'''
        pattern = re.compile(r'.+\.csv$', re.I)
        if not pattern.match(object):
            return []
        elif DataAPI(object,'r').run():
            return sorted(DataAPI(object,'r').run()[0].keys())
        return []


    @staticmethod
    def query_target_info(filename="",parameter=None):
        '''给定字典查询指定文件中满足字典的信息 可以使用通配符'''
        if Query.query_target_keys(filename):
            return DataAPI(filename,'r',parameter).run()

        elif not filename:
            data=[]
            list=Query.query_file_names(Query.query_target_keys)
            for line in list:
                info = DataLayerInterface(line,'r',parameter).run()
                if info and parameter:
                    data.append(info)
            return data

        else:
            return []


    @staticmethod
    def query_file_names(operation):
        '''查找符合对应函数的信息的文件名'''
        list=[]
        for fpathe, dirs, fs in os.walk('..'):
            for f in fs:
                list.append(os.path.join(fpathe,f))
        data=[]
        for line in list:
            if operation and operation(line):
               data.append(line)
        return data


