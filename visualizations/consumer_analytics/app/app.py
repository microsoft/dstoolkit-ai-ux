import json

import pandas as pd
from flask import Flask, redirect, render_template, url_for
from lifetimes import BetaGeoFitter
from lifetimes.datasets import load_cdnow_summary


app = Flask(__name__)


@app.route('/customer-analytics', methods=['GET'])
def customer_analytics():
    data = load_cdnow_summary(index_col=[0])
    bgf = BetaGeoFitter(penalizer_coef=0.0)
    bgf.fit(data['frequency'], data['recency'], data['T'])
    churn_probability = pd.DataFrame(
        bgf.conditional_probability_alive_matrix()
    ).apply(lambda x: 1 - x)
    churn_probability.index = list(range(churn_probability.index.max(), -1, -1))
    churn_probability = churn_probability.stack().reset_index()
    churn_probability.columns = ['y', 'x', 'churn_probability']
    churn_probability['churn_probability'] = round(churn_probability[
        'churn_probability'
    ] * 100, 3)
    churn_probability = churn_probability.to_dict(orient='records')
    data = {
        'churn_probability': json.dumps(churn_probability, indent=2),
        'foo': 'bar',
        'my_array': [1, 2, 3]
    }
    import pdb; pdb.set_trace()
    return render_template('customer_analytics.html', data=data)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


def main():
    app.run(host='0.0.0.0', port=5001, debug=True)


if __name__ == '__main__':
    main()
