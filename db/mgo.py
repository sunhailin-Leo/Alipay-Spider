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
        self.mgo_conf = json.load(open("./conf/mgo.conf"))
        self.client = MongoClient(host=self.mgo_conf['address'], port=self.mgo_conf['port'])

        # 数据库名
        self.db = self.client[self.mgo_conf['database']]

        # 集合名json
        self.collection_name = self.mgo_conf['collection']

        # 日志类
        if logger is None:
            self.logger = logging
        else:
            self.logger = logger

    # 插入数据(目前用来写入用户信息和修改用户信息,可以自定义扩展数据库名称)
    def insert_data(self, data, collection_name):
        if collection_name == "Bill":
            collection_name = self.collection_name['Bill']
        elif collection_name == "User":
            collection_name = self.collection_name['User']
        elif collection_name == "Analyse":
            collection_name = self.collection_name['Analyse']
        try:
            self.db[collection_name].insert(data)
        except Exception as err:
            # 报错信息
            self.logger.debug("ErrorMsg: " + str(err))

    # 查询数据
    def find_data(self, collection_name, query):
        # 获取数据
        try:
            if query is None or query == "":
                return self.db[self.collection_name[collection_name]].find({}, {"_id": 0})
            else:
                return self.db[self.collection_name[collection_name]].find(query, {"_id": 0})
        except Exception as err:
            # 报错信息
            self.logger.debug("ErrorMsg: " + str(err))

    # 查询数据 -- 1 (临时函数)
    def find_data_1(self, collection_name):
        # 获取数据
        try:
            return self.db[self.collection_name[collection_name]]
        except Exception as err:
            # 报错信息
            self.logger.debug("ErrorMsg: " + str(err))
