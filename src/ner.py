# -*- coding: utf-8 -*-

import os
from acora import AcoraBuilder
import time


# 实体词管理对象
class Ner():

    # 初始化函数
    def __init__(self):
        # 所有实体词集合
        self._ner_word_list = []

        # AC模型的builder
        self._builder = AcoraBuilder()

    # 设置实体词集合
    def set_ner_word_list(self, ner_word_list):
        self._ner_word_list = ner_word_list

    # 构建模型
    def build_ner(self):
        for i in range(len(self._ner_word_list)):
            self._builder.add(self._ner_word_list[i])

        self._tree = self._builder.build()

    # 命中字符串信息
    def hit(self, content_str):
        hit_list = []
        for hit_word, pos in self._tree.finditer(content_str):
            hit_list.append([hit_word, pos])

        return hit_list



# 实体词管理对象的管理类
class NerMgr():

    # 初始化函数
    def __init__(self):
        # 所有实体词集合
        self._ner_list = []

    # 添加ner对象
    def append_ner(self, ner):
        self._ner_list.append(ner)

    # 查找命中的关键词
    def hit(self, content_str):
        hit_list = []

        for i in range(len(self._ner_list)):
            hit_list_tmp = self._ner_list.hit(content_str)
            hit_list += hit_list_tmp

        return hit_list


#########################################################################
## main 主函数 ##

if __name__ == '__main__':

    pass


