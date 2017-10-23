# -*- coding: UTF-8 -*-
"""
Created on 2017年10月23日
@author: Leo
"""

'''
    工具方法
    nested_list： 平滑化List 例: [[1, 2], [3, 4]] 调用后: [1, 2, 3, 4]
    convert_negative: 任意字符串数值转换成负数数值
'''


class Utils:
    def __init__(self):
        pass

    # 遍历拆解嵌套的List
    def nested_list(self, list_raw, result):
        for item in list_raw:
            if isinstance(item, list):
                self.nested_list(item, result)
            else:
                result.append(item)

        return result

    # 正数转负数
    @staticmethod
    def convert_negative(x):
        if x == "0.0":
            return round(float(x), 2)
        else:
            return round(-(float(x)), 2)

