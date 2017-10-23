# -*- coding: UTF-8 -*-
"""
Created on 2017年10月15日
@author: Leo
"""

# 系统内部库
import logging

# 工程内部库
from analyse.analyseHandler import *

# 日志基本配置
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S')
logger = logging.getLogger()


class AnalyseStarter:
    def __init__(self, username):
        # 用户名
        self.USERNAME = username

        # 初始化analyseHandler
        self.ana = Analyse(username=self.USERNAME)

    # 购物列表分析器
    def shopping_analyser(self):
        shopping_result = self.ana.shopping()
        logger.info(shopping_result)
        logger.info("############ 购物列表 ############")

        shopping_record = self.ana.calculate(data=shopping_result)
        logger.info(shopping_record)
        logger.info("############ 购物列表每周统计 ############")

        shopping_record_log = self.ana.calculate_log(data=shopping_record)
        logger.info(shopping_record_log)
        logger.info("############ 购物列表每周统计(对数) ############")

        week_result = self.ana.each_weekday_result(data=shopping_result)
        logger.debug(week_result)
        logger.info("############ 购物列表统计纵向对比周 ############")

        week_result_log = self.ana.calculate_log(week_result)
        logger.debug(week_result_log)
        logger.info("############ 购物列表统计纵向对比周(对数) ############")

        quantum_df = self.ana.count_dif_time_quantum(dataframe=self.ana.pre_shopping())
        logging.debug(quantum_df)
        logger.info("############ 购物列表统计纵向对比时间段 ############")

        quantum_df_log = self.ana.calculate_log(quantum_df)
        logging.debug(quantum_df_log)
        logger.info("############ 购物列表统计纵向对比时间段(对数) ############")

    '''
    def offline_shopping_analyser(self):
        offline_shopping_result = self.ana.offline_shopping()
        logger.info(offline_shopping_result)
        logger.info("############ 线下列表 ############")

        offline_shopping_record = self.ana.calculate(data=offline_shopping_result)
        logger.info(offline_shopping_record)

        offline_shopping_record_log = self.ana.calculate_log(data=offline_shopping_record)
        logger.info(offline_shopping_record_log)

        logger.info("############ 线下列表每周统计 ############")

    def repay_analyser(self):
        repay_result = self.ana.repay()
        logger.info(repay_result)
        logger.info("############ 还款列表 ############")

        repay_record = self.ana.calculate(data=repay_result)
        logger.info(repay_record)

        repay_record_log = self.ana.calculate_log(data=repay_record)
        logger.info(repay_record_log)

        logger.info("############ 还款列表每周统计 ############")

    def pay_analyser(self):
        pay_result = self.ana.pay()
        logger.info(pay_result)
        logger.info("############ 缴费列表 ############")

        pay_record = self.ana.calculate(data=pay_result)
        logger.info(pay_record)

        pay_record_log = self.ana.calculate_log(data=pay_record)
        logger.info(pay_record_log)

        logger.info("############ 缴费列表每周统计 ############")
    '''

    def core_analyser(self):
        # 构建处理对象以及构造一些必要的时间列
        self.ana.generate_ymd_index()
        self.ana.generate_weekday_list()

        # 购物记录的处理和计算逻辑
        self.shopping_analyser()

        # 线下记录的处理和计算逻辑
        # self.offline_shopping_analyser()

        # 还款记录的处理和计算逻辑
        # self.repay_analyser()

        # 缴费记录的处理和计算逻辑
        # self.pay_analyser()


if __name__ == '__main__':
    USERNAME = "379978424@qq.com"
    analyse = AnalyseStarter(USERNAME)
    logger.setLevel("DEBUG")
    analyse.core_analyser()
