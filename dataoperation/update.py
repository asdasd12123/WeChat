# coding=utf-8
from database.database import DataAPI
from check import Check
from query import Query


class Update(object):

    @staticmethod
    def update(filename, _type, outdata, keys=[]):
        # 更新数据 可以覆盖 添加 和追加到文件末尾  外部数据必须是以列表为容器　元素是字典
        error = Check.format_check(outdata)
        if Check.get_result(error):
            print error
            return False

        if _type == 'w' or _type == 'dl':
            data = Query.query_target_info(filename, None)
            data = Check.del_repeat(outdata, data, keys, _type)
            return DataAPI(filename, 'w', data).run()

        elif _type == 'a':
            return DataAPI(filename, 'a', outdata).run()

        else:
            print 'invalid parameter : %s' % (_type,)
            return False


