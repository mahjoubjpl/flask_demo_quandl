from flask import Flask, render_template, request, redirect
import requests
import pandas as pd
import quandl
from bokeh.plotting import figure, show, output_file
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, Range1d, HoverTool, CrosshairTool

app = Flask(__name__)

def data_getter(ticker):
    quandl.ApiConfig.api_key = 'aV6ixxytw_ZyLnA5YZyT'
    data = quandl.get_table('WIKI/PRICES', ticker = [ticker],
                        qopts = { 'columns': ['date', 'close'] },
                        date = { 'gte': '2015-08-09', 'lte': '2015-09-09' },
                        paginate=True)
    data['date'] = pd.to_datetime(data['date'])

    return data


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/about')
def about():
  return render_template('about.html')

if __name__ == '__main__':
  app.run(port=33507)
