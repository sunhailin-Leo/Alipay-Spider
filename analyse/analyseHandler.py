# -*- coding: UTF-8 -*-
"""
Created on 2017年10月14日
@author: Leo
"""

# 系统内部库
import time
import logging
import numpy as np
import pandas as pd
from collections import OrderedDict

# 工程内部库
from db.mgo import *
from util.time_util import *
from util.utils import *


class Analyse(object):
    def __init__(self, username):
        # 用户名
        self.username = username

        # 初始化Util对象
        self.time_util = TimeUtil()
        self.utils = Utils()

        # 数据库连接
        self.mgo = Mgo(None)

        # 构造DataFrame
        self.data = pd.DataFrame(list(self.mgo.find_data(collection_name="Bill",
                                                         query={"transfer_username": self.username})))

        # 初始化开始和结束的周期
        self.start_time = '2017-07-14'
        self.end_time = '2017-10-14'

        # 计算时间差,并算出最大周数
        self.time_gap = self.time_util.get_time_gap(time_start=self.start_time, time_end=self.end_time)
        self.max_week_num = self.time_util.get_max_week_num(self.time_gap.days)

        # 通过时间周期生成时间序列的Series
        self.time_series = pd.date_range(self.start_time, self.end_time)

        # 日列表,每周数据临时List,每周List
        self.day_list = []
        self.each_week = []
        self.week_list = []

    # 生成时间序列List
    def generate_time_series(self):
        return self.time_series.astype(str).tolist()

    '''
        初始化方法
    '''
    # 后初始化变量
    def init_value(self):
        self.day_list = []
        self.each_week = []
        self.week_list = []

    '''
        DataFrame操作函数
    '''
    # 构造年月日列时间序列索引
    def generate_ymd_index(self):
        self.data['transfer_ymd'] = pd.to_datetime(self.data['transfer_ymd'])

    # 构造礼拜信息
    def generate_weekday_list(self):
        # 日期List
        weekday_list = []
        for i in self.data['transfer_ymd'].astype(str).tolist():
            date_time = datetime.datetime.strptime(i, '%Y-%m-%d')
            weekday_list.append(self.time_util.get_week_day(date_time))
        self.data['Week'] = weekday_list
        self.data.set_index(['transfer_ymd'], inplace=True)

    # 构造时间段信息
    def generate_time_quantum(self, time_hms_list):
        # 时分秒List
        result = []
        for each_time in time_hms_list:
            result.append(self.time_util.get_time_quantum(time_hms=each_time))
        return result

    # 将三层嵌套的按每周划分的统计数据转换成DataFrame
    def each_day_count_df(self, is_negative):
        result_df_list = []
        logging.debug(self.week_list)
        # 核心转换逻辑
        for first in self.week_list:
            for second in first:
                result_df_list.append(second)

        # 构建新的DataFrame
        result_df = pd.DataFrame(result_df_list, columns=['Date', 'Count', 'WeekDay', 'WeekNum'])

        if is_negative is None or is_negative is True:
            # 使用map方法把正数转成负数
            result_df['Count'] = list(map(self.utils.convert_negative, result_df['Count']))

        result_df = result_df.set_index(['Date'])

        # 返回DataFrame
        return result_df

    '''
        通用每周数据统计逻辑
    '''
    # 每周和每日数据的处理逻辑
    def week_and_day(self, df_data):
        # 初始化周数,默认值为1
        week_num = 1

        # 初始化最后周的List,默认值为空(长度为0)
        last_week = []
        for each_time in self.generate_time_series():
            result = np.array([abs(float(money)) for money in df_data[each_time]['transfer_money'].tolist()]).sum()
            # 存储礼拜
            if len(list(set(df_data[each_time]['Week'].tolist()))) == 0:
                weekday = self.time_util.get_week_day(datetime.datetime.strptime(each_time, '%Y-%m-%d'))
            else:
                weekday = list(set(df_data[each_time]['Week'].tolist()))
            # 合并List
            final_result = [each_time, str(result), weekday]
            # 日详情
            day_result = self.utils.nested_list(final_result, [])
            # 存储日详情
            self.day_list.append(day_result)
            # 处理周详情
            if self.time_util.Sunday in day_result:
                # 将每一个自然周的数据写入到周列表中,写入完成后再清空每周List
                day_result.append(week_num)
                self.each_week.append(day_result)
                self.week_list.append(self.each_week)
                self.each_week = []
                # 周日后,周数加一
                week_num += 1
            else:
                # 周一到周六
                day_result.append(week_num)
                self.each_week.append(day_result)

                '''
                    严重Bug --- 2017.10.22(已解决, 解决办法待优化, 引入一些临时变量)
                    原因: 因为最后一周不满一周所以,没有最后一周没有写入到List中.
                    解决办法:如果当前的周数等于最大周,且最后一周的数据没有包含周日即不是一个自然周,
                            并将最后的一周最后数据保留到循环结束,再写入到self.week_list中
                '''
                if week_num == self.max_week_num:
                    last_week = self.each_week

        # 如果最后一周不空,即最后一周不是一个自然周,则last_week的List长度不为0.
        if len(last_week) != 0:
            self.week_list.append(last_week)

    '''
        四类数据预处理
    '''
    def pre_shopping(self):
        # 购物
        df_shopping = self.data[self.data['transfer_tag'].isin(['1'])]
        df_shopping = df_shopping[df_shopping['transfer_status'].isin(['交易成功', '已付款'])]

        return df_shopping

    def pre_offline_shopping(self):
        # 线下
        df_offline = self.data[self.data['transfer_tag'].isin(['2'])]
        df_offline = df_offline[df_offline['transfer_status'].isin(['交易成功'])]

        return df_offline

    def pre_repay(self):
        # 还款
        return self.data[self.data['transfer_tag'].isin(['3'])]

    def pre_pay(self):
        # 缴费
        return self.data[self.data['transfer_tag'].isin(['4'])]

    '''
        四类数据的统计处理逻辑
    '''
    def shopping(self):
        # 预处理
        df_shopping = self.pre_shopping()

        # 处理日和周的数据
        self.init_value()
        self.week_and_day(df_shopping)

        result_df = self.each_day_count_df(is_negative=True)

        # 返回数据结果
        return result_df

    def offline_shopping(self):
        # 预处理
        df_offline = self.pre_offline_shopping()

        # 处理日和周的数据
        self.init_value()
        self.week_and_day(df_offline)

        # 转换DataFrame
        result_df = self.each_day_count_df(is_negative=True)

        # 返回数据结果
        return result_df

    def repay(self):
        # 预处理
        df_repay = self.pre_repay()

        # 处理日和周
        self.init_value()
        self.week_and_day(df_repay)

        # 转换DataFrame
        result_df = self.each_day_count_df(is_negative=False)

        # 返回数据结果
        return result_df

    def pay(self):
        # 缴费
        df_pay = self.pre_pay()

        try:
            # 处理日和周
            self.init_value()
            self.week_and_day(df_pay)

            # 转换DataFrame
            result_df = self.each_day_count_df(is_negative=False)

            # 返回数据结果
            return result_df
        except KeyError:
            logging.debug("无数据!")

    '''
        纵向对比上午下午晚上和半夜的消费
    '''
    def count_dif_time_quantum(self, dataframe):
        # 时间段处理
        dataframe['time_quantum'] = self.generate_time_quantum(time_hms_list=dataframe['transfer_hms'].tolist())

        # 筛选后的数据
        filter_df = dataframe.loc[:, ['transfer_money', 'transfer_hms', 'time_quantum']]
        filter_df[['transfer_money']] = filter_df[['transfer_money']].astype(float)

        # 统计每个时间段的花费
        quantum_count = pd.DataFrame(filter_df['transfer_money'].groupby(filter_df['time_quantum']).sum())
        quantum_count = quantum_count.rename(columns={'transfer_money': 'Count'})

        return quantum_count

    '''
        计算逻辑:
            1、周计算逻辑,纵向统计(即3个月的每周几之和)
            2、分组求和
            3、求和后求每周的Log值
    '''
    @staticmethod
    def each_weekday_result(data):
        # 周计算逻辑
        return pd.DataFrame(data['Count'].groupby(data['WeekDay']).sum())

    @staticmethod
    def calculate(data):
        # 分组求和(groupby, sum)
        try:
            return pd.DataFrame(data['Count'].groupby(data['WeekNum']).sum())
        except TypeError:
            logging.debug("无数据!")

    @staticmethod
    def calculate_log(data):
        # 计算Log函数的结果,并写入到List中
        log_result = []
        try:
            for each_data in data['Count'].tolist():
                if each_data != 0.0:
                    log_result.append(round(math.log(abs(each_data)), 2))
                else:
                    log_result.append(0.0)
            # 将Log计算的List转换成DataFrame返回
            del data['Count']
            data['Log_Count'] = log_result
            return data
        except TypeError:
            logging.debug("无数据!")

    '''
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
        logging.debug(data)
        try:
            self.mgo.insert_data(data, "analyse_result")
        except Exception as err:
            logging.info("写入错误!")
            logging.debug(err.with_traceback(err))
    '''
