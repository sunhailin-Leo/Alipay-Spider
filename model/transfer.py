# -*- coding: UTF-8 -*-
"""
Created on 2017年9月26日
@author: Leo

交易记录的结构体
"""

# 系统库
import collections


class Transfer(object):
    def __init__(self):
        # 年月日 时分秒
        self._ymd = None
        self._hms = None
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

    @property
    def y_m_d(self):
        return self._ymd

    @y_m_d.setter
    def y_m_d(self, ymd):
        if isinstance(ymd, str):
            self._ymd = ymd
        else:
            raise ValueError("Year month and day are illegal!")

    @property
    def h_m_s(self):
        return self._hms

    @h_m_s.setter
    def h_m_s(self, hms):
        if isinstance(hms, str):
            self._hms = hms
        else:
            raise ValueError("Hour minutes are illegal!")

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
        return str({"transfer_ymd": self._ymd,
                    "transfer_hms": self._hms,
                    "transfer_memo": self._memo,
                    "transfer_name": self._name,
                    "transfer_seller_code": self._seller_code,
                    "transfer_code": self._transfer_code,
                    "transfer_serial_num": self._serial_num,
                    "transfer_opposite": self._opposite,
                    "transfer_money": self._money,
                    "transfer_status": self._status,
                    "username": self._user,
                    "transfer_tag": self._transfer_tag})

    # 转换成有序字典
    def get_order_dict(self):
        or_dict = collections.OrderedDict()
        or_dict['transfer_ymd'] = self._ymd
        or_dict['transfer_hms'] = self._hms
        or_dict['transfer_memo'] = self._memo
        or_dict['transfer_name'] = self._name
        or_dict['transfer_seller_code'] = self._seller_code
        or_dict['transfer_code'] = self._transfer_code
        or_dict['transfer_serial_num'] = self._serial_num
        or_dict['transfer_opposite'] = self._opposite
        or_dict['transfer_money'] = self._money
        or_dict['transfer_status'] = self._status
        or_dict['transfer_username'] = self._user
        or_dict['transfer_tag'] = self._transfer_tag
        return or_dict
