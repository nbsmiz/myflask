from flask import Flask, render_template, request, redirect, session
import pandas as pd
import requests
from bokeh.plotting import figure
from bokeh.embed import components
import quandl
import bokeh


# import pandas_datareader as pdr

app = Flask(__name__)

app.vars = {}


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/graph', methods=['POST'])
def graph():
    quandl.ApiConfig.api_key = "fK6eeHbvyzUgszZDrHhj"
    symbol = "GOOG"
    columns = ['ticker', 'date', 'open', 'close', 'low', 'high']

    data = quandl.get_table('WIKI/PRICES', qopts={'columns': columns},
        ticker=[symbol], date={'gte': '2019-01-01', 'lte': '2019-12-31'})

    print(data)
    df = pd.DataFrame(data)
    # print(df.head())

    df['date'] = pd.to_datetime(df['date'])

    x, y = df['date'].values, df['close'].values
    # print(x)
    # print(y)

    plot = figure(title='%s Historical Close Value Via Quandl' % symbol,
              x_axis_label='date',
              x_axis_type='datetime')

    plot.line(x, y, line_width=2, legend_label="Close")

    script, div = components(plot)

    return render_template('graph.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=5000)
