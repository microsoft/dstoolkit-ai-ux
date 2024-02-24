import os
import urllib

import yaml
from flask import Flask, redirect, render_template, url_for
from opencensus.ext.azure.trace_exporter import AzureExporter
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.trace.samplers import ProbabilitySampler


app = Flask(__name__)
__here__ = os.path.dirname(__file__)
DEMO_CONFIG_PATH = os.path.join(__here__, 'demo_configs')
DEMO_CONFIG_ORDER = os.path.join(DEMO_CONFIG_PATH, '.order')
# App Insights Instrumentation Key from Env Variable
APP_INSIGHTS_CONN_STR = os.environ.get('APP_INSIGHTS_CONN_STR')
if APP_INSIGHTS_CONN_STR is not None:
    middleware = FlaskMiddleware(
        app,
        exporter=AzureExporter(connection_string=APP_INSIGHTS_CONN_STR),
        sampler=ProbabilitySampler(rate=1.0)
    )


@app.route('/', methods=['GET'])
def home():
    return redirect(url_for('gallery'))


@app.route('/gallery', methods=['GET'])
def gallery():
    with open(DEMO_CONFIG_ORDER, 'r') as f:
        demo_config_order = f.read().splitlines()
    demo_configs = []
    for demo_config_filename in demo_config_order:
        filepath = os.path.join(DEMO_CONFIG_PATH, demo_config_filename + '.yml')
        with open(filepath, 'r') as f:
            single_demo_config = yaml.safe_load(f)
            single_demo_config['filename'] = demo_config_filename
            demo_configs.append(single_demo_config)
    data = {
        'demo_configs': demo_configs,
        'app_insights_conn_str': APP_INSIGHTS_CONN_STR,
    }
    return render_template('gallery.html', data=data)


@app.route('/use-case/<use_case_name>', methods=['GET'])
def use_case(use_case_name):
    use_case_config_filename = use_case_name + '.yml'
    filepath = os.path.join(DEMO_CONFIG_PATH, use_case_config_filename)
    with open(filepath, 'r') as f:
        demo_config = yaml.safe_load(f)
    if demo_config['links'].get('arm_template'):
        demo_config['links']['arm_template'] = (
            "https://portal.azure.com/#create/Microsoft.Template/uri/"
            + urllib.parse.quote_plus(demo_config['links']['arm_template'])
        )
    data = {
        'demo_config': demo_config,
        'app_insights_conn_str': APP_INSIGHTS_CONN_STR,
    }
    return render_template('use_case.html', data=data)


def main():
    app.run(host='0.0.0.0', port=5000, debug=True)


if __name__ == '__main__':
    main()
