# coding=utf-8
from bashcheckin import BashCheckIn
from dataoperation.manage import DataManage


class CheckInNode(BashCheckIn):

    def start_auto(self):
        if self.status:
            print ' 当前已经存在自动考勤窗口无法再次开启!'
            return False

        if not self.get_time():
            return False

        stu_list = DataManage(DataManage.target_info, args=('../InData/studentInfo.csv',
                                                            {'ClassID': self.key['ClassID']})).run()
        self.write_seq()
        stu_list = self.init_data(stu_list, 'auto')
        self.status = True
        return DataManage(DataManage.update, args=(self.filename, 'w', stu_list)).run()

    def start_random(self):
        if not self.status:
            print ' 当前没有开启自动考勤无法进行抽点考勤!'
            return False
        self.random_info = self.random_stu_list()
        if not self.random_info:
            return False
        stu_list = self.init_data(self.random_info, 'random')
        return DataManage(DataManage.update, args=(self.filename, 'a', stu_list)).run()

    def receive(self, stu_info):
        if stu_info['Type'] == 'auto':
            return self.auto_cal(stu_info)
        else:
            return self.random_cal(stu_info)

    def man_check_in(self):  # 手动考勤

        stu_info = DataManage(DataManage.target_info, args=('../InData/studentInfo.csv',
                                                            {'ClassID': self.key['ClassID']})).run()

        if not stu_info:
            print '当前班级不存在请重新输入!'
            return False

        self.write_seq()
        print '请按照以下选项输入状态 非法输入默认为缺勤!'
        print ' 1　正常　2　迟到　３　早退　４　缺勤 5　请假已批准'
        stu_list = self.init_data(stu_info, 'man')
        return DataManage(DataManage.update, args=(self.filename, 'w', stu_list)).run()