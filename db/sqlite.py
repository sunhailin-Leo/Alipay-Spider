# -*- coding: UTF-8 -*-
"""
Created on 2017年10月10日
@author: Leo
"""

# 系统库
import json
import logging
import sqlite3


class SQLite:
    def __init__(self, logger):
        # 日志类(是否输出SQL语句)
        self.SHOW_SQL = True
        if logger is None:
            self.logger = logging
        else:
            self.logger = logger

        # sqlite 数据库基本配置(读取配置文件,并创建数据库文件以及初始化游标)
        self.conf = json.load(open("./../conf/sqlite.conf"))
        if self.conf is not None:
            self.conn = sqlite3.connect(self.conf['db_name'])
            if self.conn is not None:
                self.cursor = self.conn.cursor()
                self.logger.info("The database connect or create success!\n数据库连接成功或成功创建!")
            else:
                self.logger.info("The database can not connect success!\n数据库连接失败请重试!")
        else:
            self.logger.info("The config can not load success!\n配置文件读取失败请重试!")

    def create_db(self):
        # 获取创建数据库的语句
        sql = self.conf['db_init_sql']
        if sql is not None and sql != '':
            if self.SHOW_SQL:
                self.logger.debug('执行SQL语句:[{}]'.format(sql))
            try:
                print(sql)
                # 执行建表语句并提交事务
                self.cursor.execute(sql)
                self.conn.commit()
                self.logger.info("Table create success!\n数据库表创建成功!")
            except sqlite3.DatabaseError as err:
                err.with_traceback(err)
                self.conn.rollback()
                self.logger.info("Table create fail!\n数据库表创建失败!")
        else:
            self.logger.debug('The [{}] is empty or equal None!'.format(sql))

    def insert_data(self, transfer):
        # 构造数据
        data = []
        data.insert(0, transfer.time)
        data.insert(1, transfer.memo)
        data.insert(2, transfer.name)
        data.insert(3, transfer.seller_code)
        data.insert(4, transfer.transfer_code)
        data.insert(5, transfer.serial_num)
        data.insert(6, transfer.opposite)
        data.insert(7, transfer.money)
        data.insert(8, transfer.status)

        # 获取插入数据库的语句:
        sql = self.conf['db_insert_sql']
        if sql is not None and sql != '':
            if self.SHOW_SQL:
                self.logger.debug('执行SQL语句:[{}]'.format(sql))
            try:
                print(sql)
                # 执行建表语句并提交事务
                self.cursor.execute(sql, data)
                self.conn.commit()
                self.logger.info("Execute success!\n执行成功!")
            except sqlite3.DatabaseError as err:
                err.with_traceback(err)
                self.conn.rollback()
                self.logger.info("Execute fail!\n执行失败!")
        else:
            self.logger.debug('The [{}] is empty or equal None!'.format(sql))

    # 关闭游标
    def close_cursor(self):
        self.cursor.close()


if __name__ == '__main__':
    d = SQLite(None)
    d.create_db()
