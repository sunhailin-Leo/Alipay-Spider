# -*- coding: UTF-8 -*-
"""
Created on 2017年9月26日
@author: Leo
"""

# 第三方库
from lxml import etree

# 项目内部库
from db.mgo import *
from db.sqlite import *
from model.transfer import *


class BillInfo:
    def __init__(self):
        # 读取测试文件
        f = open("./test.html")
        self.result = f.read()

    def parser(self):
        # Xpath
        selector = etree.HTML(self.result)

        # 选取的父标签
        trs = selector.xpath("//tbody//tr")

        # 测试环境的抓取标签方式和正式环境有点不同
        try:
            # 实体类
            transfer = Transfer()

            # 数据库连接(MongoDB和SQLite)
            # mgo = Mgo(None)
            sql = SQLite(None)
            sql.create_db()

            for tr in trs:
                # 交易时间(年月日 + 时分)
                time_tag = tr.xpath('td[@class="time"]/p/text()')
                a = str(time_tag[0]).strip() + " " + str(time_tag[1]).strip()
                # 划分年月日和时分
                time_list = a.split(" ")
                # 年月日
                y_m_d = time_list[0]
                y_element = y_m_d.split(".")[0]
                m_element = y_m_d.split(".")[1]
                d_element = y_m_d.split(".")[2]
                # 时分
                h_m = time_list[1]
                h_element = h_m.split(":")[0]
                m_element = h_m.split(":")[1]

                transfer.time = a

                # memo标签(暂时不知道是啥)
                transfer.memo = str(tr.xpath('td[@class="memo"]/text()')[0]).strip()

                # 交易名称
                try:
                    transfer.name = str(tr.xpath('td[@class="name"]/p/a/text()')[0]).strip()
                except:
                    transfer.name = str(tr.xpath('td[@class="name"]/p/text()')[0]).strip()

                # 交易订单号(商户订单号和交易号)
                code = tr.xpath('td[@class="tradeNo ft-gray"]/p/text()')
                if "流水号" in code[0]:
                    transfer.serial_num = (str(code[0]).split(":"))[-1]
                    transfer.seller_code = ""
                    transfer.transfer_code = ""
                else:
                    code_list = str(code[0]).split(" | ")
                    transfer.serial_num = ""
                    transfer.seller_code = (str(code_list[0]).split(":"))[-1]
                    transfer.transfer_code = (str(code_list[-1]).split(":"))[-1]

                # 对方
                transfer.opposite = str(tr.xpath('td[@class="other"]/p/text()')[0]).strip()

                # 金额
                transfer.money = str(tr.xpath('td[@class="amount"]/span/text()')[0]).replace(" ", "").replace("+", "")

                # 状态
                transfer.status = tr.xpath('td[@class="status"]/p[1]/text()')[0]

                # 输出
                od = OrderedDict()
                od.copy()
                print(od)
                print(eval(str(transfer)))

                # 写入到MongoDB数据库
                # mgo.insert_data(transfer)

                # 写入到Sqlite数据库
                # sql.insert_data(transfer)
                # sql.close_cursor()

        except Exception as err:
            print(err.with_traceback(err))
            print("Has something Wrong!")


if __name__ == '__main__':
    b = BillInfo()
    b.parser()