# -*- coding: UTF-8 -*-
"""
Created on 2017年10月10日
@author: Leo
"""

# 工程内部引用
from controller.alipay_login import *


# 启动类
class Starter(object):
    def __init__(self, username, password):
        # 用户名和密码
        self.USERNAME = username
        self.PASSWORD = password

    # 启动核心方法
    def parser_spider(self):
        # 入口
        alipay = AlipayBill(HEADERS, self.USERNAME, self.PASSWORD)

        # 选择浏览器
        alipay.choose_browser()

        # 初始化结束后，开始登陆
        alipay.get_cookies()

        # 登陆后开始获取数据
        alipay.get_data()

        # 关闭浏览器
        alipay.close_browser()


if __name__ == '__main__':
    USERNAME = "379978424@qq.com"
    PASSWORD = "379978424.qq.com"
    start = Starter(USERNAME, PASSWORD)
