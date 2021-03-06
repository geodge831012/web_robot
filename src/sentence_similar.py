# -*- coding: utf-8 -*-

import os
import numpy as np
import jieba_fast
from gensim.models import Word2Vec
import pickle
import time



#########################################################################
## 矩阵相乘 ##
def matrix_dot(matrix, x):
    return matrix.dot(x)


#########################################################################
## 求X Y两个向量的cosine值
def get_cosine_value(X_list, Y_list, X_norm, Y_norm):
    # 分子 x1*y1 + x2*y2 + ... + xn*yn
    # 分母 X_norm * Y_norm

    if (X_norm <= 0.0 or Y_norm <= 0.0 or len(X_list) != len(Y_list)):
        return 0

    XY_size = len(X_list)

    X = X_list.reshape(1, XY_size)
    Y = Y_list.reshape(1, XY_size)

    return float(X.dot(Y.T) / (X_norm * Y_norm))


##################################一个聚类簇的信息#######################################
class SentenceEmbedding():
    def __init__(self):

        # 停用词文件路径
        self.stopword_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../data/all_stopword.txt")

        # 停用词集合
        self.stopword_list = []

        # 停用词加载
        self.load_stopword()

        # word2vec模型
        self.model = Word2Vec.load(os.path.join(os.path.abspath(os.path.dirname(__file__)), "../word2vec/word2vec_wx"))

        # 意图文件路径
        self.intention_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../data/intention.txt")

        # 意图对应答案的文件路径
        self.intention_answer_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../data/intention_answer.txt")

        # 意图对应答案的字典
        self.intention_answer_dict = {}

        # idf文件路径
        self.idf_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../data/idf.txt")

        # 没有的词的idf默认系数
        self.idf_default = 5.0

        # 所有句子的集合
        self.all_sentence_list = []

        # 所有句子的向量集合 用以矩阵计算得到所有向量cos值  cos(X, Y) = (x1*y1 + x2*y2) / (norm(X) + norm(Y))
        self.all_sentence_embedding_matrix = np.empty([0, 256], dtype=np.float)



    # 加载所有的停用词 到 类变量中
    def load_stopword(self):

        for line in open(self.stopword_file):
            self.stopword_list.append(line.strip())


    # 获取某个词的word2vec值 256维
    def get_word2vec(self, word):

        if(word in self.model):
            return self.model[word]
        else:
            return np.zeros(0, dtype=np.float)


    # 获取某一个句子的句向量
    def get_sentence_embedding(self, sentence):

        # 句子的向量
        sentence_embedding = np.zeros(self.model.vector_size, dtype=np.float)

        rst = jieba_fast.cut(sentence)

        for word in rst:

            if word in self.stopword_list:
                # 停用词跳过
                continue

            # word2vec某词
            w2v_vector = self.get_word2vec(word)
            if 0 == len(w2v_vector):
                continue

            sentence_embedding += w2v_vector

        sentence_norm = np.linalg.norm(sentence_embedding)

        return sentence_embedding, sentence_norm


    # 处理所有意图id对应的答案的文件
    def proc_intention_answer(self):

        for line in open(self.intention_answer_file):

            line_list        = line.strip().split("\t")
            if(2 != len(line_list)):
                continue

            intention_id     = int(line_list[0])
            intention_answer = line_list[1]

            self.intention_answer_dict[intention_id] = intention_answer




    # 处理所有的预设的句子
    def proc_intention(self):

        # 处理所有意图id对应的答案的文件
        self.proc_intention_answer()

        start_num = 1

        # 存放所有句子的向量的集合
        all_sentence_embedding_list = []

        for line in open(self.intention_file):
            line_list        = line.strip().split("\t")
            if(2 != len(line_list)):
                continue

            intention_id     = int(line_list[0])
            sentence         = line_list[1]
            intention_answer = self.intention_answer_dict.get(intention_id, "我还不知道答案哦!")

            sentence_embedding, sentence_norm = self.get_sentence_embedding(sentence)

            all_sentence_embedding_list.append(list(sentence_embedding))

            sentence_info_dict = {}
            sentence_info_dict["intention_id"]          = intention_id
            sentence_info_dict["sentence_id"]           = start_num
            sentence_info_dict["sentence"]              = sentence
            sentence_info_dict["sentence_embedding"]    = sentence_embedding
            sentence_info_dict["sentence_norm"]         = sentence_norm
            sentence_info_dict["intention_answer"]      = intention_answer

            start_num += 1

            self.all_sentence_list.append(sentence_info_dict)

        # 将句子向量集合 转化成为 句子向量矩阵
        self.all_sentence_embedding_matrix = np.array(all_sentence_embedding_list)


sentence_embedding = SentenceEmbedding()

# 处理所有的预设的句子
sentence_embedding.proc_intention()

#########################################################################
## 处理input的句子 ##
def process_input_sentence(input_sentence):

    input_sentence_embedding, input_sentence_norm = sentence_embedding.get_sentence_embedding(input_sentence)

    # # 存放结果集合
    # rst_list = []
    #
    # for i in range(len(sentence_embedding.all_sentence_list)):
    #     similar_value = get_cosine_value(input_sentence_embedding, \
    #                                      sentence_embedding.all_sentence_list[i]["sentence_embedding"], \
    #                                      input_sentence_norm, \
    #                                      sentence_embedding.all_sentence_list[i]["sentence_norm"])
    #
    #     rst_list.append((sentence_embedding.all_sentence_list[i]["intention_id"], \
    #                      sentence_embedding.all_sentence_list[i]["sentence"], \
    #                      sentence_embedding.all_sentence_list[i]["intention_answer"], \
    #                      similar_value))
    #
    # list.sort(rst_list, key=lambda rs: rs[3], reverse=True)
    # print(rst_list[0])
    #
    # return rst_list[0][0], rst_list[0][1], rst_list[0][2], rst_list[0][3]

    # 存放结果集合
    rst_list = list(matrix_dot(sentence_embedding.all_sentence_embedding_matrix, input_sentence_embedding))

    for i in range(len(rst_list)):
        fenmu_float = sentence_embedding.all_sentence_list[i]["sentence_norm"] * input_sentence_norm
        if (fenmu_float > 0):
            rst_list[i] /= fenmu_float

    pos = rst_list.index(max(rst_list))

    sentence_info_dict = sentence_embedding.all_sentence_list[pos]

    return sentence_info_dict["intention_id"], sentence_info_dict["sentence"], sentence_info_dict["intention_answer"], rst_list[pos]








#########################################################################
## main 主函数 ##

if __name__ == '__main__':

    sentence_embedding = SentenceEmbedding()


    # 处理所有的预设的句子
    sentence_embedding.proc_intention()

    print("=================print_result=======================")
    print("sentence_embedding.all_sentence_list.len=%d" % len(sentence_embedding.all_sentence_list))
    #for i in range(len(sentence_embedding.all_sentence_list)):
    #    print(sentence_embedding.all_sentence_list[i])
    print("=================print_result=======================")

    #input_sentence = "股票名称智能诊股"
    input_sentence = "范式概念股票"

    input_sentence_embedding, input_sentence_norm = sentence_embedding.get_sentence_embedding(input_sentence)

    # 存放结果集合
    rst_list = []

    for i in range(len(sentence_embedding.all_sentence_list)):

        similar_value = get_cosine_value(input_sentence_embedding, \
                                         sentence_embedding.all_sentence_list[i]["sentence_embedding"], \
                                         input_sentence_norm, \
                                         sentence_embedding.all_sentence_list[i]["sentence_norm"])

        rst_list.append((sentence_embedding.all_sentence_list[i]["sentence"], similar_value))

    sort_rst_list = list.sort(rst_list, key=lambda rs: rs[1], reverse=True)
    print(rst_list)

