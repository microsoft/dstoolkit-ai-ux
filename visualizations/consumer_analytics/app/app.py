import json
from collections import defaultdict

import numpy as np
import pandas as pd
from flask import Flask, redirect, render_template, url_for
from lifetimes import BetaGeoFitter, GammaGammaFitter
from lifetimes.datasets import (
    load_cdnow_summary, load_cdnow_summary_data_with_monetary_value)


app = Flask(__name__)


def get_trained_beta_geo_fitter():
    data = load_cdnow_summary(index_col=[0])
    bgf = BetaGeoFitter(penalizer_coef=0.0)
    bgf.fit(data['frequency'], data['recency'], data['T'])
    return bgf


def get_trained_gamma_gamma_fitter():
    summary_with_money_value = load_cdnow_summary_data_with_monetary_value()
    returning_customers_summary = summary_with_money_value[
        summary_with_money_value['frequency'] > 0
    ]
    ggf = GammaGammaFitter(penalizer_coef=0)
    ggf.fit(
        returning_customers_summary['frequency'],
        returning_customers_summary['monetary_value']
    )
    return ggf


def get_clv(bgf, ggf, customer_data):
    customer_data['clv'] = ggf.customer_lifetime_value(
        bgf, #the model to use to predict the number of future transactions
        customer_data['frequency'],
        customer_data['recency'],
        customer_data['T'],
        customer_data['monetary_value'],
        time=12, # months
        discount_rate=0.01 # monthly discount rate ~ 12.7% annually
    )
    return customer_data


def get_customer_data():
    frequency = np.arange(0, 51, 5)
    recency = np.arange(0, 41, 2)
    average_spend = np.arange(10, 101, 10)
    first_transaction = np.arange(0, 41, 2)
    max_recency = max(first_transaction)
    customer_data = pd.DataFrame(
        np.array(
            np.meshgrid(
                frequency, recency, average_spend, first_transaction
            )
        ).T.reshape(-1, 4),
        columns=['frequency', 'recency', 'monetary_value', 'T']
    )
    customer_data['recency_invert'] = max_recency - customer_data['recency']
    return customer_data


def format_clv_data(clv_data):
    tree = lambda: defaultdict(tree)
    clv_data_dict = tree()
    for _, row in clv_data.iterrows():
        clv_data_dict[
            int(row['frequency'])
        ][
            int(row['recency_invert'])
        ][
            int(row['T'])
        ][
            int(row['monetary_value'])
        ] = "%.2f" % row['clv']
    return clv_data_dict


@app.route('/customer-analytics', methods=['GET'])
def customer_analytics():
    bgf = get_trained_beta_geo_fitter()
    churn_probability = pd.DataFrame(
        bgf.conditional_probability_alive_matrix()
    ).apply(lambda x: 1 - x)
    churn_probability.index = list(range(churn_probability.index.max(), -1, -1))
    churn_probability = churn_probability.stack().reset_index()
    churn_probability.columns = ['y', 'x', 'churn_probability']
    churn_probability['churn_probability'] = round(churn_probability[
        'churn_probability'
    ] * 100, 3)
    customer_data = get_customer_data()
    ggf = get_trained_gamma_gamma_fitter()
    clv_data = get_clv(bgf, ggf, customer_data)
    clv_data = format_clv_data(clv_data)
    churn_probability = churn_probability.to_dict(orient='records')
    data = {
        'churn_probability': json.dumps(churn_probability, indent=2),
        'clv_data': json.dumps(clv_data)
    }

    return render_template('/customer_analytics.html', data=data)


@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')


def main():
    app.run(host='0.0.0.0', port=5001, debug=True)


if __name__ == '__main__':
    main()
