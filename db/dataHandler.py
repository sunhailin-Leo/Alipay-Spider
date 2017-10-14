# -*- coding: UTF-8 -*-
"""
Created on 2017年10月10日
@author: Leo
"""

# 系统库
import time
import threading

# 项目内部库
from db.mgo import *
from db.sqlite import *


class DataHandler:
    def __init__(self):
        # 线程池
        self.threads = []

        # 初始化MongoDB对象，SQLite3对象
        self.mgo = Mgo(None)
        self.sqlite = SQLite(None)

        # 初始变量
        self.info = None

    # 选择数据源
    def choose_data_source(self):
        t1 = threading.Thread(target=self.check_mongo_status)
        self.threads.append(t1)

        for self.t in self.threads:
            self.t.setDaemon(True)
            self.t.start()
            # 设置join时间4秒,4秒后执行不到则执行timeout函数
            self.t.join(4)
            print(self.info)
        # self.timeout()

    # 检查MongoDB的连接状态
    def check_mongo_status(self):
        self.info = self.mgo.client.server_info()
        return self.info

    # 超时函数
    def timeout(self):
        raise TimeoutError


if __name__ == '__main__':
    d = DataHandler()
    d.choose_data_source()
