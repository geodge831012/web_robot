# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import json
from sentence_similar import process_input_sentence

app = Flask(__name__)


@app.route('/zhongxin_card/', methods={"GET", "POST"})
def similarityRequest():

    input_str = request.args.get("input")

    print("input:" + input_str)

    intention_id, intention_sentence, intention_answer, similar_value = process_input_sentence(input_str)

    response = {
                    "intention_id"       : intention_id, \
                    "intention_sentence" : intention_sentence, \
                    "intention_answer"   : intention_answer, \
                    "similar_value"      : similar_value \
                }

    rsp = json.dumps(response, ensure_ascii=False)

    print("rsp:" + rsp)

    #return json.dumps(response), 200, [('Content-Type', 'application/json;charset=utf-8')]
    return rsp, 200, [('Content-Type', 'application/json;charset=utf-8')]



if __name__ == "__main__":

    print("web_robot start...")

    #app.run(debug=True)
    app.run(host="116.62.40.137", port=5000, debug=False)


