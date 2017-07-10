# coding=utf-8
from DataLayerInterface.DataLayerInterface import DataLayerInterface
import os
import re
class Query(object):
    '''查询目标信息通过不同的参数达到查询不同的效果 '''
    @staticmethod
    def QueryObjectKey(object):
        '''返回目标的键 也可查询含有合法信息的文件是否存在 若不存在则返回None'''
        pattern = re.compile(r'.+\.csv$', re.I)
        if not pattern.match(object):
            return []
        elif DataLayerInterface(object,'r').run():
            return sorted(DataLayerInterface(object,'r').run()[0].keys())
        return []

    @staticmethod
    def QueryObjectInfo(filename="",parameter=None):
        '''给定字典查询指定文件中满足字典的信息 可以使用通配符'''

        if Query.QueryObjectKey(filename):
            return DataLayerInterface(filename,'r',parameter).run()

        elif not filename:
            data=[]
            list=Query.QueryNameByInfo(Query.QueryObjectKey)
            for line in list:
                info = DataLayerInterface(line,'r',parameter).run()
                if info and parameter:
                    data.append(info)
            return data

        else:
            return []

    @staticmethod
    def QueryPermisson(UserID,filename):
        '''返回用户对文件的权限'''

        ID = UserID[UserID.keys()[0]]
        if not Query.QueryObjectInfo("",UserID):
            if  ID!='0':
                return 0
            else:
                return 6
        filename=filename.split('/')[-1]
        if filename.startswith(ID):
                return 6
        return 2


    @staticmethod
    def QueryNameByInfo(operation):
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


if __name__ == '__main__':
    print Query.QueryObjectInfo('../InData/coadasdasdadrse.csv')
    #print Query.QueryPermisson({'root':'0'},'a.txt')
    #print Query.QueryObjectInfo('')

    #print Query.QueryNameByInfo()
