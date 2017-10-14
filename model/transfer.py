# -*- coding: UTF-8 -*-
"""
Created on 2017年9月26日
@author: Leo

交易记录的结构体
"""

# 系统库
import time


class Transfer(object):
    def __init__(self):
        # 年月日时分秒
        self._year = None
        self._month = None
        self._day = None
        self._hour = None
        self._minutes = None
        # 交易备注
        self._memo = None
        # 交易名称
        self._name = None
        # 交易商户订单号
        self._seller_code = None
        # 交易号
        self._transfer_code = None
        # 流水号
        self._serial_num = None
        # 对方(有可能是收款方也有可能是付款方)
        self._opposite = None
        # 金额
        self._money = None
        # 状态
        self._status = None
        # 用户名
        self._user = None
        # 交易标签
        self._transfer_tag = None

    # @property
    # def time(self):
    #     return self._time
    #
    # @time.setter
    # def time(self, transfer_time):
    #     if isinstance(transfer_time, str) and transfer_time is not None:
    #         # 转换时间戳
    #         # if transfer_time != "":
    #         #     timeArray = time.strptime(transfer_time, "%Y.%m.%d %H:%M")
    #         #     timeStamp_millisecond = int(time.mktime(timeArray)) * 1000
    #         #     self._time = timeStamp_millisecond
    #         # else:
    #         #     self._time = ""
    #         self._time = transfer_time
    #     else:
    #         raise ValueError("Time is illegal!")

    @property
    def year(self):
        return self._year

    @year.setter
    def year(self, year):
        if isinstance(year, str) and year is not None:
            self._year = year
        else:
            raise ValueError("Year is illegal!")

    @property
    def month(self):
        return self._month

    @month.setter
    def month(self, month):
        if isinstance(month, str) and month is not None:
            self._month = month
        else:
            raise ValueError("Year is illegal!")

    @property
    def day(self):
        return self._day

    @day.setter
    def day(self, day):
        if isinstance(day, str) and day is not None:
            self._day = day
        else:
            raise ValueError("Year is illegal!")

    @property
    def hour(self):
        return self._hour

    @hour.setter
    def hour(self, hour):
        if isinstance(hour, str) and hour is not None:
            self._hour = hour
        else:
            raise ValueError("Year is illegal!")

    @property
    def minutes(self):
        return self._minutes

    @minutes.setter
    def minutes(self, minutes):
        if isinstance(minutes, str) and minutes is not None:
            self._minutes = minutes
        else:
            raise ValueError("Year is illegal!")

    @property
    def memo(self):
        return self._memo

    @memo.setter
    def memo(self, memo):
        if isinstance(memo, str):
            self._memo = memo
        else:
            raise ValueError("Memo is illegal!")

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str):
            self._name = name
        else:
            raise ValueError("Name is illegal!")

    @property
    def seller_code(self):
        return self._seller_code

    @seller_code.setter
    def seller_code(self, code):
        if isinstance(code, str):
            self._seller_code = code
        else:
            raise ValueError("Seller Code is illegal!")

    @property
    def transfer_code(self):
        return self._transfer_code

    @transfer_code.setter
    def transfer_code(self, code):
        if isinstance(code, str):
            self._transfer_code = code
        else:
            raise ValueError("Transfer Code is illegal!")

    @property
    def serial_num(self):
        return self._serial_num

    @serial_num.setter
    def serial_num(self, code):
        if isinstance(code, str):
            self._serial_num = code
        else:
            raise ValueError("Serial Number is illegal!")

    @property
    def opposite(self):
        return self._opposite

    @opposite.setter
    def opposite(self, name):
        if isinstance(name, str):
            self._opposite = name
        else:
            raise ValueError("Opposite is illegal!")

    @property
    def money(self):
        return self._money

    @money.setter
    def money(self, money):
        if isinstance(money, str):
            self._money = money
        else:
            raise ValueError("Money is illegal!")

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, status):
        if isinstance(status, str):
            self._status = status
        else:
            raise ValueError("Status is illegal!")

    @property
    def user(self):
        return self._user

    @user.setter
    def user(self, user):
        if isinstance(user, str):
            self._user = user
        else:
            raise ValueError("User is illegal!")

    @property
    def tag(self):
        return self._transfer_tag

    @tag.setter
    def tag(self, tag):
        if isinstance(tag, str):
            self._transfer_tag = tag
        else:
            raise ValueError("Tag is illegal!")

    def __str__(self):
        return str({"transfer_year": self._year,
                    "transfer_month": self._month,
                    "transfer_day": self._day,
                    "transfer_hour": self._hour,
                    "transfer_minutes": self._minutes,
                    "transfer_memo": self._memo,
                    "transfer_name": self._name,
                    "transfer_seller_code": self._seller_code,
                    "transfer_code": self._transfer_code,
                    "transfer_serial_num": self._serial_num,
                    "transfer_opposite": self._opposite,
                    "transfer_money": self._money,
                    "transfer_status": self._status,
                    "user": self._user,
                    "transfer_tag": self._transfer_tag})
