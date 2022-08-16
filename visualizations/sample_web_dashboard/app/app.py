import os
from flask import Flask, render_template, request, jsonify
from flask import redirect, url_for
from datetime import datetime, timedelta
from functools import wraps
import numpy as np
import json
import pandas as pd
from utils import getCount, performMapping
import joblib
path_model = "model"
loaded_rf = joblib.load(os.path.join(path_model , "my_random_forest.joblib"))

app = Flask(__name__)
secret = 'secret'
app._static_folder = os.path.abspath("static/")


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/api/get_inference", methods=['GET', 'POST'])
def get_inferences():
    req_ = request.get_data()
    data2 = json.loads(req_)
    keys_ = ["exact_age", "gender", "age", "class", "title", "familySize", "embarkation", "fare", "model"]
    inference_set = {i:data2["vals"][i] for i in data2["vals"].keys() if i in keys_}
    model_id = data2["vals"]["model"]
    x_test_prediction= performMapping(inference_set)
    print("==>", inference_set, model_id)
    predictions = loaded_rf.predict(x_test_prediction)
    print("Prediction ==>",predictions[0] )
    if predictions[0] == 0:
        str_ = "dead"
    else:
        str_= "alive"
    return json.dumps({"inference": str_})


@app.route("/api/get_insights", methods=['GET', 'POST'])
def get_insights():
    data2 = request.get_data()
    data2 = json.loads(data2)
    print("==>", data2)
    count,number_died, number_survived, vec_survAge, vec_diedAge = getCount(dict_=data2, x=df)
    return json.dumps({"count": count, "rows": df.shape[0], \
        "number_died": number_died, "number_survived": number_survived,
        "vec_survAge":  vec_survAge, "vec_diedAge":  vec_diedAge})


if __name__ == "__main__":
    path_data = r"data/titanic/dataset.csv"
    df = pd.read_csv(os.path.join(os.getcwd(), path_data))
    print("-->", df.shape)
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 3000), debug=True)


