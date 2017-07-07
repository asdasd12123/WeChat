#coding=utf-8
import re
class Check(object):
    @staticmethod
    def formatcheck(data,format=None):
        ''' 格式检查 '''
        error={}
        row=1
        for line in data:
            Check().re_linecheck(line,row,error,format)
            row=row+1
        return error

    def get_Primary_item(self,keys,line):
        key= reduce((lambda x, y: str(x) + ','+str(y)), [line[key] for key in keys if line.has_key(key)], '')
        return key if key else None

    @staticmethod
    def delrepeat(outdata,indata=[],keys=[],Type='w'):
        '''可以自我去重 也可以指定外部数据后覆盖掉内部的数据或追加或删除到内部数据 可以指定主键充当判断准则'''
        if Check.getresult(Check.formatcheck(outdata)):
            return []
        if not keys:
            keys= indata[0].keys() if indata else outdata[0].keys()

        for line in outdata:
            key1=Check().get_Primary_item(keys,line)
            record = {}
            for index in indata:
                key2 =Check().get_Primary_item(keys,index)
                if not record.has_key(key2):
                    record[key2]=1
                if key1 and key1==key2:
                    if Type !='w' or not record[key2]:
                        indata.remove(index)
                    elif record[key2]:
                        indata[indata.index(index)]=line
                        record[key2]=0
                elif not key1 or not key2:
                    print 'The external data is different from the internal data key ！'
                    return []
            if Type=='w' and record.get(key1,1):
                indata.append(line)
        return indata

    def re_linecheck(self,line,row,error,format=[]):
        '''利用正则表达式对数据进行检查 '''

        if not line or type(error)!=dict:
            return True
        if not format:
            for (key,item) in line.items():
                if not item:
                    error['Error line row [' + str(row) + ']'] = 'Datakey '+key+ ': value does not exist!'
            return Check.getresult(error)

        for (key,item) in format.items():
            if not line.has_key(key):
                error['Error line row [' + str(row) + ']'] = 'Data ' + key + ' The key or value does not exist!'
            else:
                if re.findall(item,line[key]):
                    pass
                else:
                    error['Error line row ['+str(row)+']']='The line information does not conform to the standard!'

        return Check.getresult(error)


    @staticmethod
    def getresult(dictionary):
        '''判断一个字典是否为空 '''
        if type(dictionary)!=dict:
            return True
        for (key,item) in dictionary.items():
            if item:
                return True
        return False



if __name__=='__main__':
    read=[{1:2,2:3,3:5}   ,  {1:2,2:3,3:5} ]
    error={}
    #read4=Check.delrepeat(read,read2,[1,2,3])
    #print read4,error
    key = [1,3]
    read2 = [{1: 2, 2: 3, 3: 5}]
    read = [{1: 2, 2: 3, 3: 5}, {1: 2, 2: 3, 3: 1} ,{1:1,2:8,3:1}]
    read4 = Check.delrepeat(read,read2,key)
    print read4,error

    read = {1: 4, 2: 5, 3: 6}

    #print [read[key1] for key1 in key if read.has_key(key1)]
    #print reduce((lambda x,y:str(x)+str(y)),[read[key1] for key1 in key if read.has_key(key1)])