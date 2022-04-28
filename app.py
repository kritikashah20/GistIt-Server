from flask import Flask, request, jsonify
from script import t_on_paras, points_from_para, n_sent_from_para

app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify("Hello!!! kritika")

@app.route('/abstract',methods=['POST'])
def abstract():
    data = request.get_json(force=True)
    final_summarised_seg = t_on_paras(data["text"], data["threshold"])
    return jsonify(final_summarised_seg)

@app.route('/pointwise',methods=['POST'])
def pointwise():
    data = request.get_json(force=True)
    pointwise_result = points_from_para(data["text"], data["threshold"])
    return jsonify(pointwise_result)

@app.route('/topnsent',methods=['POST'])
def topnsent():
    data = request.get_json(force=True)
    n_sents = n_sent_from_para(data["text"], data["threshold"], data["n"])
    result = []
    for i in n_sents:
        i_list = []
        for l in i:   
            i_list.append(str(l))
            print(i_list)
        result.append(i_list)
    # d={}
    # d["list"]=result
    # return d
    return jsonify(result)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
