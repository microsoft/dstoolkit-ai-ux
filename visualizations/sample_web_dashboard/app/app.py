import os
from flask import Flask, render_template, request, jsonify
from flask import redirect, url_for
from datetime import datetime, timedelta
from functools import wraps
import numpy as np
import json
import pandas as pd
from utils import get_count, perform_mapping
import joblib

# Load an ML model. 
__here__ = os.path.dirname(os.path.realpath(__file__))
path_model = os.path.join(__here__, "model")
loaded_rf = joblib.load(os.path.join(path_model , "my_random_forest.joblib"))

# Load data that will be used to generate some analytics
data_path = os.path.join(__here__, "data", "titanic", "dataset.csv")
df = pd.read_csv(data_path)

# Flask app
app = Flask(__name__)
app._static_folder = os.path.join(__here__, 'static')
secret = 'secret'


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/api/get_inference", methods=['GET', 'POST'])
def get_inferences():
    req_ = request.get_data()
    req_data = json.loads(req_)
    keys_ = ("exact_age", "gender", "age", "class", "title", "familySize", "embarkation", "fare", "model")
    inference_set = {key: value for key, value in req_data['vals'].items() if key in keys_}
    # model_id = req_data["vals"]["model"] #Not being used at this stage
    df_test_prediction = perform_mapping(inference_set)
    predictions = loaded_rf.predict(df_test_prediction)
    if predictions[0] == 0:
        str_ = "dead"
    else:
        str_= "alive"
    return json.dumps({"inference": str_})


@app.route("/api/get_insights", methods=['GET', 'POST'])
def get_insights():
    req_data = request.get_data()
    req_data = json.loads(req_data)
    count,number_died, number_survived, vec_survAge, vec_diedAge = get_count(dict_=req_data, x=df)
    return json.dumps({
        "count": count, 
        "rows": df.shape[0],
        "number_died": number_died, 
        "number_survived": number_survived,
        "vec_survAge":  vec_survAge, 
        "vec_diedAge":  vec_diedAge
        })


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=os.environ.get('PORT', 8080), debug=True)
    