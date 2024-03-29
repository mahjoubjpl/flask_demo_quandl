import requests
import pandas as pd
from flask import Flask, render_template, request, redirect
from datetime import date
from bokeh.plotting import figure, show
from bokeh.models import ColumnDataSource, DatetimeTickFormatter, \
    Range1d, HoverTool
from bokeh.embed import components
import quandl

app = Flask(__name__)

apikey = "aV6ixxytw_ZyLnA5YZyT"


def get_ticker(ticker):
    quandl.ApiConfig.api_key = 'aV6ixxytw_ZyLnA5YZyT'
    data = quandl.get_table('WIKI/PRICES', ticker = [ticker], 
                        qopts = { 'columns': ['date', 'close'] }, 
                        date = { 'gte': '2015-08-09', 'lte': '2015-09-09' }, 
                        paginate=True)
    data['date'] = pd.to_datetime(data['date'])

    return data

def plot_setter(df, ticker):

    p = figure(width=700, height=400, title="Ticker="+ticker, tools="")

    hover = HoverTool(tooltips=[
        ( 'date',   '@date{%F}'            ),
        ( 'close',  '$@close{%0.2f}' ),], formatters={
        'date'      : 'datetime', 
        'close' : 'printf'})
    hover.mode = 'vline'
    hover.line_policy = 'nearest'
    p.add_tools(hover)


    dfcds = ColumnDataSource(df)
    p.line('date', 'close', source = dfcds, color="#000000")

    p.xaxis.formatter=DatetimeTickFormatter(days=["%d %b"])
    p.x_range=Range1d(df['date'].min(), df['date'].max())
    p.toolbar.logo = None
    p.toolbar_location = None  
    p.title.text_color = "#000000"
    p.title.text_font_size = "1.5em"
    p.axis.major_label_text_color = "#000000"
    p.axis.major_label_text_font_size = "1.25em"
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_alpha = 0.5
    p.ygrid.grid_line_dash = [2, 4]
    p.outline_line_color = None
    p.yaxis.axis_label = "Close"
    
    return p

def invalid():
    error = None
    with open("static/error.html") as err:
        error = err.read()
    return render_template(
        'index.html',
        bokeh_script="",
        bokeh_div=error)

@app.route('/')
def main():
    return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html', plot_script="", plot_div="")
    else:
        tick = request.form['ticker_text']
        ticker_df = get_ticker(tick)
        if ticker_df.empty:
            return invalid()
        fig = plot_setter(ticker_df, tick)
        script, div = components(fig)
        return render_template(
            'index.html',
            plot_script=script,
            plot_div=div)

if __name__ == '__main__':
    app.run(port=33507)


