# -*- coding: UTF-8 -*-
"""
Created on 2017年10月10日
@author: Leo
"""

# 工程内部引用
from controller.alipay_login import *
from analyse_starter import *


# 启动类
class Starter(object):
    def __init__(self):
        # 用户名和密码
        self.USERNAME = None
        self.PASSWORD = None

    # 启动核心方法
    def parser_spider(self):
        # 入口
        alipay = AlipayBill(HEADERS, self.USERNAME, self.PASSWORD)

        # 一些选项
        alipay.main()

        # 选择浏览器
        alipay.choose_browser()

        # 初始化结束后，开始登陆
        is_login = alipay.get_cookies()

        # 判断是否登录成功
        if is_login:
            # 登陆后开始获取数据
            alipay.get_data()

            # 关闭浏览器
            alipay.close_browser()

            # 成功
            return True
        else:
            # 登录失败关闭浏览器
            alipay.close_browser()

            # 失败
            return False

    # 定时任务监听数据库(临时函数)
    def listen_db(self):
        mgo = Mgo(None)
        listening = True
        while listening:
            print(listening)
            try:
                col = mgo.find_data_1("user")
                for spider in col.find({}, {"_id": 0}):
                    print(spider)
                    if spider['isFetched'] is False:
                        # 获取数据库的用户名和密码
                        self.USERNAME = spider['username']
                        self.PASSWORD = spider['password']
                        if self.parser_spider():
                            col.update({"username": self.USERNAME},
                                       {"$set": {"isFetched": True, "errMsg": ""}})

                            # 数据分析模块
                            analyse = AnalyseStarter(self.USERNAME)
                            analyse.core_analyser()

                            # 退出
                            listening = False
                            break
                        else:
                            # 爬取失败退出
                            col.update({"username": self.USERNAME, "isFetched": False, "errMsg": "抓取失败,用户名密码出错或网络出错"})
                            listening = False
                            break
            except:
                print("No DB exists!")


if __name__ == '__main__':
    project_start = Starter()
    project_start.listen_db()