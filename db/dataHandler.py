# -*- coding: UTF-8 -*-
"""
Created on 2017年10月10日
@author: Leo
"""

# 系统库
import logging
import threading

# 项目内部库
from db.mgo import *
from db.sqlite import *


class DataHandler(object):
    def __init__(self, logger):
        # 线程池
        self.threads = []

        # 初始化MongoDB对象,不初始化SQLite
        self.mgo = None
        self.sqlite = None

        # MongoDB的连接信息
        self.mgo_info = None

        # 线程等待时间
        self.timeout_sec = 2

        # 选择的数据源
        self.data_source = None

        # 日志类变量
        if logger is None:
            self.logger = logging.getLogger()
        else:
            self.logger = logger.getLogger()

        # 是否连接到MongoDB
        self.is_connect_mgo = False

    # 初始化MongoDB数据库
    def _init_mgo(self):
        self.mgo = Mgo(self.logger)
        self.logger.debug(self.mgo.client.server_info())

    # 当MongoDB数据库没有启动或者不存在时,则启动SQLite数据库
    def _init_sqlite(self):
        self.sqlite = SQLite(self.logger)

    # 选择数据源
    def choose_data_source(self):
        # 创建计时线程,当MongoDB响应时间超过上限则中断主线程,切换数据源
        t1 = threading.Thread(target=self.check_mongo_status)
        self.threads.append(t1)

        # 循环线程池,目前只有一个线程
        for self.t in self.threads:
            self.t.setDaemon(True)
            self.t.start()
            # 设置join时间2秒,2秒后执行不到则执行timeout函数
            self.t.join(self.timeout_sec)

        # 判断是否连接成功
        if self.is_connect_mgo is True:
            self.data_source = "MongoDB"
        else:
            self.data_source = "SQLite"
            self.logger.debug("MongoDB is closed!")
            self.logger.debug("Start SQLite3 database!")
            self._init_sqlite()

    # 检查MongoDB的连接状态(返回True则MongoDB已经启动并不使用SQLite数据库,返回False则写入到SQLite中)
    def check_mongo_status(self):
        if self.is_connect_mgo is False:
            self._init_mgo()
            self.logger.debug("MongoDB is running!,MongoDB数据库正在运行!")
            self.is_connect_mgo = True

    # 数据库通用方法 --- 插入
    def insert_data(self):
        if self.is_connect_mgo:
            pass
        else:
            pass

    # 数据库通用方法 --- 删除
    def delete_data(self):
        if self.is_connect_mgo:
            pass
        else:
            pass

    # 数据库通用方法 --- 更新
    def update_data(self):
        if self.is_connect_mgo:
            pass
        else:
            pass

    # 数据库通用方法 --- 查找
    def fetch_data(self):
        if self.is_connect_mgo:
            pass
        else:
            pass

    # 超时函数
    def timeout(self):
        raise TimeoutError


if __name__ == '__main__':
    d = DataHandler(None)
    d.choose_data_source()
