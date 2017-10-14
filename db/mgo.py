# -*- coding: UTF-8 -*-
"""
Created on 2017年9月26日
@author: Leo
"""

# 系统库
import json
import logging

# 第三方库
from pymongo import MongoClient


class Mgo(object):
    def __init__(self, logger):
        # 数据库基本配置
        self.mgo_conf = json.load(open("./../conf/mgo.conf"))
        self.client = MongoClient(host=self.mgo_conf['address'], port=self.mgo_conf['port'])

        # 数据库名
        self.db = self.client[self.mgo_conf['database']]

        # 集合名
        self.collection_name = "bill_info"
        self.collection = self.db[self.collection_name]

        # 日志类
        if logger is None:
            self.logger = logging
        else:
            self.logger = logger

    # 插入数据
    def insert_data(self, data):
        # 需要将Transfer对象用str强转后，在用eval方法转成字典，写入到MongoDB数据库
        try:
            self.collection.insert(eval(str(data)))
            self.logger.info("写入成功...")
        except Exception as err:
            # 出错报错
            self.logger.debug("ErrorMsg: " + str(err))
