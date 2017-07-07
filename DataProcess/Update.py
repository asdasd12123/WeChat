#coding=utf-8
from DataLayerInterface.DataLayerInterface import DataLayerInterface
from Check import Check
from Query import Query
import os
class Update(object):

    @staticmethod
    def update(filename,Type,outdata,keys=[]):
        '''更新数据 可以覆盖 添加 和追加到文件末尾'''
        error=Check.formatcheck(outdata)
        if Check.getresult(error):
            print error
            return False

        if Type=='w' or Type =='dl':
            data=Query.QueryObjectInfo(filename,None)
            data=Check.delrepeat(outdata,data,keys,Type)
            return DataLayerInterface(filename,'w',data).run()

        elif Type=='a':
            return DataLayerInterface(filename, 'a', outdata).run()

        else:
            print 'invalid parameter : %s' %(Type)
            return False

if __name__=='__main__':
    read=Query.QueryObjectInfo('../DataProcess/course.csv')
    #read1=Query.QueryObjectInfo('a.csv')
    #print read
    #if Query.QueryFileKey('../DataLayerInterface/3.csv'):
        #print 'asdasd'
    #read1=Query.QueryObjectInfo('../DataLayerInterface/3.csv',None)
    #print read1
    #read=Update.checkformat(read,read1)
    #print read
    #print read
    '''if Update.update('a.csv','w',read):
        print 'success'
    else:
        print 'failed'  '''

    data=Query.QueryObjectInfo('../DataProcess/course.csv')
    if Update.update('a.cSV','w',data):
        print 'success'
    else:
        print 'failed'







