
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np
import tensorflow_text
import time

embed = hub.load('USE')


def load_intention_answer_file():

    intention_answer_dict = {}

    f = open('../data/intention_answer.txt', 'r')

    for line in f:

        line_list   = line.strip().split("\t")
        if 2 != len(line_list):
            print(line + "is not 2 sep, intention_answer")
        intention   = int(line_list[0])
        answer      = line_list[-1]

        intention_answer_dict[intention] = answer

    f.close()

    return intention_answer_dict

# 初始化 加载文件
def init():

    intention_question_list  = []

    f = open('../data/intention.txt','r')

    all_text_tensor = tf.zeros((0, 512), dtype=tf.float32, name=None)

    i = 0

    for line in f:

        line_list   = line.strip().split("\t")
        if 2 != len(line_list):
            print(line + "is not 2 sep, intention")
        intention   = int(line_list[0])
        question    = line_list[-1]

        # 意图和问法 存放list
        intention_question_list.append((intention, question))

        # 问句向量化集合
        text_tensor = embed(question)
        all_text_tensor = tf.concat([all_text_tensor, text_tensor], 0)

        i += 1

        if 0 == i%1000:
            print("proc " + str(i) + " text")

    f.close()

    return intention_question_list, all_text_tensor, load_intention_answer_file()



if __name__ == '__main__':

    print("begin init time : " + time.strftime('%Y-%m-%d %H:%M:%S'))
    begin_init_time = time.time()

    intention_question_list, all_text_tensor, intention_answer_dict = init()

    end_init_time = time.time()
    print("end init time : " + time.strftime('%Y-%m-%d %H:%M:%S'))
    print("init elapse time : " + str(round(end_init_time - begin_init_time, 2)) + " seconds")

    while True:

        input_str = input("please input sentence:")

        # input_str = "溢缴款转本行借记卡收取费用吗"

        begin_calc_time = time.time()

        input_tensor = embed(input_str)

        similar_list = np.inner(input_tensor, all_text_tensor).tolist()[0]

        max_pos = similar_list.index(max(similar_list))

        end_calc_time = time.time()

        (intention, question) = intention_question_list[max_pos]

        print("similar value : " + str(max(similar_list)))

        print("similar question : " + question)

        print("answer : " + intention_answer_dict[intention])

        print("calc elapse time : " + str(round(end_calc_time - begin_calc_time, 2)) + " seconds")

        print("=======================================================================================================")


