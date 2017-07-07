#coding=utf8

import Read
import Write
import Add
'''
None  "" False [] {} () 0 都是布尔类型假
'''
class DataLayerInterface(object):

    def __init__(self,filename,Type,key=None):
        self.filename=filename
        self.Type=Type
        self.key=key
        self.Read=Read.Read()
        self.Write=Write.Write()
        self.Add=Add.Add()

    def run(self):

        if self.Type not in 'rwa':
            return False

        elif self.Type == 'r':
            return self.Read.read(self.filename,self.key)
        elif self.Type == 'w':
            return self.Write.write(self.filename,self.key)
        else:
            return self.Add.add(self.filename,self.key)





if __name__=='__main__':
    key=Read.Read().read('course.csv')
    print DataLayerInterface('songjian.csv','r',key).run()

