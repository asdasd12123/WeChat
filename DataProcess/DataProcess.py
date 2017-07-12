#coding=utf-8
from Query import Query
from Update import Update
from Check import Check

class DataProcess(object):

    QueryObjectKey = 1
    QueryObjectInfo =2
    QueryPermisson =3
    QueryNameByInfo =4
    formatcheck = 5
    update = 6

    def __init__(self,target=None,args=()):
        self.target=target
        self.args=args

    def run(self):
        if self.target==1:
            return Query.QueryObjectKey(*self.args)
        elif self.target==2:
            return Query.QueryObjectInfo(*self.args)
        elif self.target==3:
            return Query.QueryPermisson(*self.args)
        elif self.target==4:
            return Query.QueryNameByInfo()
        elif self.target==5:
            return Check.formatcheck(*self.args)
        elif self.target==6:
            return Update.update(*self.args)
        else:
            print '类型错误无该函数调用!'
            return None



if __name__=='__main__':
    print DataProcess(target=DataProcess.QueryObjectInfo,args=('../InData/teacherInfo.csv',{'TeacherID':'2004633'})).run()