# -*- coding: utf-8 -*-

from flask import Flask
from flask import request
from flask import json
from flask import make_response
from sentence_similar import process_input_sentence

app = Flask(__name__)


@app.route('/zhongxin_card/', methods={"GET", "POST"})
def similarityRequest():

    input_str = request.args.get("input")

    print("input:" + input_str)

    intention_id, intention_sentence, intention_answer, similar_value = process_input_sentence(input_str)

    response_str = {
                      "intention_id"       : intention_id, \
                      "intention_sentence" : intention_sentence, \
                      "intention_answer"   : intention_answer, \
                      "similar_value"      : similar_value \
                   }

    rsp = json.dumps(response_str, ensure_ascii=False)

    print("rsp:" + rsp)

    #return json.dumps(response), 200, [('Content-Type', 'application/json;charset=utf-8')]
    #return rsp, 200, [('Content-Type', 'application/json;charset=utf-8')]

    #决跨域问题
    #response = make_response(jsonify(response_str))
    response = make_response(rsp)
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST'
    response.headers['Access-Control-Allow-Headers'] = 'x-requested-with'

    return response



if __name__ == "__main__":

    print("web_robot start...")

    #app.run(debug=True)
    app.run(host="192.168.9.60", port=5000, debug=False)


