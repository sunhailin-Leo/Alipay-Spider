# -*- coding: UTF-8 -*-
"""
Created on 2017年10月15日
@author: Leo
"""

# 工程内部库
from analyse.analyseHandler import *


class AnalyseStarter:
    def __init__(self, username):
        # 用户名
        self.USERNAME = username

        # 初始化analyseHandler
        self.ana = Analyse()

    def core_analyser(self):
        # 构建处理对象以及构造一些必要的时间列
        ana = Analyse()
        ana.generate_ymd_col()
        ana.generate_weekday_list()

        # 处理逻辑
        shopping_result = ana.shopping()
        print("############ 购物列表 ############")
        offline_shopping_result = ana.offline_shopping()
        print("############ 线下列表 ############")
        repay_result = ana.repay()
        print("############ 还款列表 ############")
        pay_result = ana.pay()
        print("############ 缴费列表 ############")

        # 计算逻辑
        shopping_record = ana.calculate(shopping_result)
        print(shopping_record)
        shopping_record_log = ana.calculate_log(shopping_record)
        print(shopping_record_log)
        print("############ 购物列表每周统计 ############")

        offline_shopping_record = ana.calculate(offline_shopping_result)
        print(offline_shopping_record)
        offline_shopping_record_log = ana.calculate_log(offline_shopping_record)
        print(offline_shopping_record_log)
        print("############ 线下列表每周统计 ############")

        repay_record = ana.calculate(repay_result)
        print(repay_record)
        repay_record_log = ana.calculate_log(repay_record)
        print(repay_record_log)
        print("############ 还款列表每周统计 ############")

        pay_record = ana.calculate(pay_result)
        print(pay_record)
        pay_record_log = ana.calculate_log(pay_record)
        print(pay_record_log)
        print("############ 缴费列表每周统计 ############")

        # 存储逻辑
        try:
            self.ana.insert_data(self.ana.generate_order_dict(self.USERNAME, "1", shopping_record, shopping_record_log))
            self.ana.insert_data(self.ana.generate_order_dict(self.USERNAME, "2", offline_shopping_record, offline_shopping_record_log))
            self.ana.insert_data(self.ana.generate_order_dict(self.USERNAME, "3", repay_record, repay_record_log))
            self.ana.insert_data(self.ana.generate_order_dict(self.USERNAME, "4", pay_record, pay_record_log))
        except IOError:
            print("写入出错!")

#
# if __name__ == '__main__':
#     USERNAME = "379978424@qq.com"
#     analyse = AnalyseStarter(USERNAME)
#     analyse.core_analyser()
