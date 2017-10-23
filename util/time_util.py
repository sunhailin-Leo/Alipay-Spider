# -*- coding: UTF-8 -*-
"""
Created on 2017年10月23日
@author: Leo
"""

# 系统内部库
import math
import time
import datetime

'''
       get_week_day: 将日期转换成周几
       get_time_gap: 计算时间差(天)
       get_max_week_num: 计算最大周数
'''


class TimeUtil:
    def __init__(self):
        # 初始化一些日期,时间和时间模板常量
        self.Monday = "周一"
        self.Tuesday = "周二"
        self.Wednesday = "周三"
        self.Thursday = "周四"
        self.Friday = "周五"
        self.Saturday = "周六"
        self.Sunday = "周日"
        
        self.Morning = "上午"
        self.Afternoon = "下午"
        self.Evening = "晚上"
        self.Midnight = "半夜"
        
        self.morning_start = "060000"
        self.afternoon_start = "120000"
        self.evening_start = "180000"
        self.evening_end = "235959"
        self.midnight_start = "000000"
        
        self.time_hms_layout = "%H%M%S"
        self.time_ymd_layout = "%Y%M%D"

    def get_week_day(self, date):
        week_day_dict = {
            0: self.Monday,
            1: self.Tuesday,
            2: self.Wednesday,
            3: self.Thursday,
            4: self.Friday,
            5: self.Saturday,
            6: self.Sunday,
        }
        day = date.weekday()
        return week_day_dict[day]

    # 计算日期时间差
    @staticmethod
    def get_time_gap(time_start, time_end):
        start_time_year = int(time_start.split("-")[0])
        start_time_month = int(time_start.split("-")[1])
        start_time_day = int(time_start.split("-")[2])

        end_time_year = int(time_end.split("-")[0])
        end_time_month = int(time_end.split("-")[1])
        end_time_day = int(time_end.split("-")[2])

        return datetime.datetime(end_time_year, end_time_month, end_time_day) - \
               datetime.datetime(start_time_year, start_time_month, start_time_day)

    # 计算最大周数
    @staticmethod
    def get_max_week_num(gap):
        if gap >= 0:
            if gap != 0:
                return math.ceil(float(gap / 7))
            else:
                return 0
        else:
            raise ValueError("No time gap or gap is error!")

    # 时间转换为上午,下午,晚上和半夜
    def divide_time_quantum(self, time_hms, first_time, second_time):
        try:
            if int(time.strftime(self.time_hms_layout, first_time)) <= \
                    int(time.strftime(self.time_hms_layout, time_hms)) < \
                    int(time.strftime(self.time_hms_layout, second_time)):
                return True
            else:
                return False
        except Exception as err:
            print(err.with_traceback(err))
    
    # 判断时间段
    def get_time_quantum(self, time_hms):
        if self.divide_time_quantum(time_hms=time.strptime(time_hms, self.time_hms_layout),
                                    first_time=time.strptime(self.morning_start, self.time_hms_layout),
                                    second_time=time.strptime(self.afternoon_start, self.time_hms_layout)) is True:
            return self.Morning

        elif self.divide_time_quantum(time_hms=time.strptime(time_hms, self.time_hms_layout),
                                      first_time=time.strptime(self.afternoon_start, self.time_hms_layout),
                                      second_time=time.strptime(self.evening_start, self.time_hms_layout)) is True:
            return self.Afternoon

        elif self.divide_time_quantum(time_hms=time.strptime(time_hms, self.time_hms_layout),
                                      first_time=time.strptime(self.evening_start, self.time_hms_layout),
                                      second_time=time.strptime(self.evening_end, self.time_hms_layout)) is True:
            return self.Evening

        elif self.divide_time_quantum(time_hms=time.strptime(time_hms, self.time_hms_layout),
                                      first_time=time.strptime(self.midnight_start, self.time_hms_layout),
                                      second_time=time.strptime(self.morning_start, self.time_hms_layout)) is True:
            return self.Midnight
        else:
            raise ValueError("Variable time_hms is illegal!")
