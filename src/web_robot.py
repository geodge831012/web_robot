# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import json
from sentence_similar import get_cosine_value, SentenceEmbedding

app = Flask(__name__)


sentence_embedding = SentenceEmbedding()

# 处理所有的预设的句子
sentence_embedding.proc_intention()

@app.route('/bringing_up_children/', methods={"GET", "POST"})
def similarityRequest():

    input_str = request.args.get("input")

    print("input:" + input_str)

    input_sentence_embedding, input_sentence_norm = sentence_embedding.get_sentence_embedding(input_str)

    # 存放结果集合
    rst_list = []

    for i in range(len(sentence_embedding.all_sentence_list)):
        similar_value = get_cosine_value(input_sentence_embedding, \
                                         sentence_embedding.all_sentence_list[i]["sentence_embedding"], \
                                         input_sentence_norm, \
                                         sentence_embedding.all_sentence_list[i]["sentence_norm"])

        rst_list.append((sentence_embedding.all_sentence_list[i]["intention_id"], \
                         sentence_embedding.all_sentence_list[i]["sentence"], \
                         similar_value))

    #sort_rst_list = list.sort(rst_list, key=lambda rs: rs[1], reverse=True)
    list.sort(rst_list, key=lambda rs: rs[2], reverse=True)
    print(rst_list[0])

    response = {"intention_id": rst_list[0][0], "intention_sentence":rst_list[0][1], "similar_value":rst_list[0][2]}

    return json.dumps(response), 200, [('Content-Type', 'application/json;charset=utf-8')]



if __name__ == "__main__":

    print("web_robot start...")

    #app.run(debug=True)
    app.run(debug=False)


