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
        # 交易时间(精确到毫秒)
        self._time = None
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

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, transfer_time):
        if isinstance(transfer_time, str) and transfer_time is not None:
            if transfer_time != "":
                timeArray = time.strptime(transfer_time, "%Y.%m.%d %H:%M")
                timeStamp_millisecond = int(time.mktime(timeArray)) * 1000
                self._time = timeStamp_millisecond
            else:
                self._time = ""
        else:
            raise ValueError("Time is illegal!")

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

    def __str__(self):
        return str({"transfer_time": self._time,
                    "transfer_memo": self._memo,
                    "transfer_name": self._name,
                    "transfer_seller_code": self._seller_code,
                    "transfer_code": self._transfer_code,
                    "transfer_serial_num": self._serial_num,
                    "transfer_opposite": self._opposite,
                    "transfer_money": self._money,
                    "transfer_status": self._status})