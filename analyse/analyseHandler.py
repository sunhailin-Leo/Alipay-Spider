# -*- coding: UTF-8 -*-
"""
Created on 2017年10月14日
"""

# 系统内部库
import math
import time
import datetime
import numpy as np
import pandas as pd
from collections import OrderedDict

# 工程内部库
from db.mgo import *


class Analyse:
    def __init__(self):
        # 数据库连接
        self.mgo = Mgo(None)

        # 构造DataFrame
        self.data = pd.DataFrame(list(self.mgo.find_data("bill_info")))

        # 初始化变量
        self.time_ymd = None
        self.time_series = pd.date_range('2017-07-14', '2017-10-14')

        # 日列表,每周数据临时List,每周List
        self.day_list = []
        self.each_week = []
        self.week_list = []

    @staticmethod
    def get_week_day(date):
        week_day_dict = {
            0: '周一',
            1: '周二',
            2: '周三',
            3: '周四',
            4: '周五',
            5: '周六',
            6: '周日',
        }
        day = date.weekday()
        return week_day_dict[day]

    # 遍历拆解嵌套的List
    def nested_list(self, list_raw, result):
        for item in list_raw:
            if isinstance(item, list):
                self.nested_list(item, result)
            else:
                result.append(item)

        return result

    # 生成时间序列List
    def generate_time_series(self):
        return self.time_series.astype(str).tolist()

    # 构造年月日列
    def generate_ymd_col(self):
        self.time_ymd = self.data['transfer_year'] + "-" + self.data['transfer_month'] + "-" + self.data['transfer_day']
        self.data['Date'] = self.time_ymd
        self.data['Date'] = pd.to_datetime(self.data['Date'])
        self.data.set_index("Date", inplace=True)

    # 构造礼拜信息
    def generate_weekday_list(self):
        # 日期List
        weekday_list = []
        for i in self.time_ymd.tolist():
            date_time = datetime.datetime.strptime(i, '%Y-%m-%d')
            weekday_list.append(self.get_week_day(date_time))
        self.data['Week'] = weekday_list

    # 每周和每日数据的处理逻辑
    def week_and_day(self, df_data):
        for each_time in self.generate_time_series():
            result = np.array([abs(float(money)) for money in df_data[each_time]['transfer_money'].tolist()]).sum()
            # 存储礼拜
            if len(list(set(df_data[each_time]['Week'].tolist()))) == 0:
                weekday = self.get_week_day(datetime.datetime.strptime(each_time, '%Y-%m-%d'))
            else:
                weekday = list(set(df_data[each_time]['Week'].tolist()))
            # 合并List
            final_result = [each_time, str(result), weekday]
            # 日详情
            day_result = self.nested_list(final_result, [])
            # 存储日详情
            self.day_list.append(day_result)
            # 处理周详情
            if "周日" in day_result:
                # 将每一个自然周的数据写入到周列表中,写入完成后再清空每周List
                self.each_week.append(day_result)
                self.week_list.append(self.each_week)
                self.each_week = []
            else:
                # 周一到周六
                self.each_week.append(day_result)

    # 后初始化变量
    def init_value(self):
        self.day_list = []
        self.each_week = []
        self.week_list = []

    '''
        四项逻辑
    '''

    def shopping(self):
        # 购物
        df_shopping = self.data[self.data['transfer_tag'].isin(['1'])]
        df_shopping = df_shopping[df_shopping['transfer_status'].isin(['交易成功', '已付款'])]

        # 处理日和周的数据
        self.init_value()
        self.week_and_day(df_shopping)

        # 输出测试
        # for v in self.week_list:
        #     print(v)

        return self.week_list

    def offline_shopping(self):
        # 线下
        df_offline = self.data[self.data['transfer_tag'].isin(['2'])]
        df_offline = df_offline[df_offline['transfer_status'].isin(['交易成功'])]

        # 处理日和周的数据
        self.init_value()
        self.week_and_day(df_offline)

        # 输出测试
        # for v in self.week_list:
        #     print(v)

        return self.week_list

    def repay(self):
        # 还款
        df_repay = self.data[self.data['transfer_tag'].isin(['3'])]

        # 处理日和周
        self.init_value()
        self.week_and_day(df_repay)

        # 输出测试
        # for v in self.week_list:
        #     print(v)

        return self.week_list

    def pay(self):
        # 缴费
        df_pay = self.data[self.data['transfer_tag'].isin(['4'])]

        try:
            # 处理日和周
            self.init_value()
            self.week_and_day(df_pay)

            # 输出测试
            # for v in self.week_list:
            #     print(v)

            return self.week_list
        except KeyError:
            print("无数据!")

    # 计算逻辑
    @staticmethod
    def calculate(data):
        each_week_sum = []
        try:
            for each_week in data:
                week_count = 0
                for each_day in each_week:
                    week_count += float(each_day[1])
                each_week_sum.append(("%.2f" % week_count))
            return each_week_sum
        except TypeError:
            print("无数据!")

    @staticmethod
    def calculate_log(data):
        log_result = []
        try:
            for each_data in data:
                if float(each_data) != 0.00:
                    log_result.append(math.log(float(each_data)))
                else:
                    log_result.append(0)
            return log_result
        except TypeError:
            print("无数据!")

    # 存储逻辑
    @staticmethod
    def generate_order_dict(username, transfer_type, week, week_log):
        # 有序字典
        od = OrderedDict()
        od['user'] = username
        od['transfer_type'] = transfer_type

        week_list = []
        if week is None:
            od['each_week'] = week_list
        else:
            for each_week_data in week:
                if float(each_week_data) != 0.00:
                    week_list.append("-" + each_week_data)
                else:
                    week_list.append(each_week_data)
            od['each_week'] = week_list

        od['each_week_log'] = week_log

        now_time = lambda: int(round(time.time() * 1000))
        od['createTime'] = now_time()

        # 返回字典
        return dict(od)

    # 写入到MongoDB
    def insert_data(self, data):
        print(data)
        self.mgo.insert_data(data, "analyse_result_test")
