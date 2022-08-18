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

__here__ = os.path.dirname(os.path.realpath(__file__))
path_model = os.path.join(__here__, "model")
loaded_rf = joblib.load(os.path.join(path_model , "my_random_forest.joblib"))

app = Flask(__name__)
app._static_folder = os.path.join(__here__, 'static')
secret = 'secret'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/api/get_inference", methods=['GET', 'POST'])
def get_inferences():
    req_ = request.get_data()
    data2 = json.loads(req_)
    keys_ = ("exact_age", "gender", "age", "class", "title", "familySize", "embarkation", "fare", "model")
    inference_set = {key: value for key, value in data2['vals'].items() if key in keys_}
    model_id = data2["vals"]["model"]
    x_test_prediction = performMapping(inference_set)
    predictions = loaded_rf.predict(x_test_prediction)
    if predictions[0] == 0:
        str_ = "dead"
    else:
        str_= "alive"
    return json.dumps({"inference": str_})


@app.route("/api/get_insights", methods=['GET', 'POST'])
def get_insights():
    data2 = request.get_data()
    data2 = json.loads(data2)
    count,number_died, number_survived, vec_survAge, vec_diedAge = getCount(dict_=data2, x=df)
    return json.dumps({
        "count": count, 
        "rows": df.shape[0],
        "number_died": number_died, 
        "number_survived": number_survived,
        "vec_survAge":  vec_survAge, 
        "vec_diedAge":  vec_diedAge
        })


if __name__ == "__main__":
    data_path = os.path.join(__here__, "data", "titanic", "dataset.csv")
    df = pd.read_csv(data_path)
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080), debug=True)