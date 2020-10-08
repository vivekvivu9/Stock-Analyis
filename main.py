from flask import Flask, render_template, request
from alpha_vantage.timeseries import TimeSeries
import plotly.express as px
api_key = "JSQLA9LVPJMGOZOG"
ts = TimeSeries(key=api_key, output_format="pandas")
def search_company(company):
    try:
        s, meta = ts.get_symbol_search(keywords=company)
        symbols = list(s['1. symbol'])
        companys = list(s['2. name'])
        regions = list(s['4. region'])
        currency = list(s['8. currency'])
        sy = {}
        j = 0
        for i in symbols:
            sy[i] = companys[j]+" "+regions[j]+" "+currency[j]+" "+i
            j+=1
        return sy
    except :
        return str("company not found")
def create_report(SYMBOL,date):
    if date=='daily':
        data, meta = ts.get_daily(symbol=SYMBOL, outputsize="full")
        data.reset_index(inplace=True)
        data=data[:30]
        date="last 30 days analysis"
    elif date == "week":
        data, meta = ts.get_weekly(symbol=SYMBOL)
        data.reset_index(inplace=True)
        date="monthly analysis"
    elif date== "month":
        data, meta = ts.get_monthly(symbol=SYMBOL)
        data.reset_index(inplace=True)
        date="yearly analysis"
    fig = px.line(data, x='date', y='4. close', title=date)
    fig.write_html("templates/report.html")
    return str(1)
app = Flask(__name__)
@app.route('/')
def stock():
    return render_template('index.html')
@app.route('/analysis' ,methods=['POST'])
def result():
    if request.method == 'POST':
        result=request.form.to_dict()
        result = search_company(result['company'])
        if result == "company not found":
            result += '   retry'
            return result
        return render_template('result.html', web_data=result)
@app.route('/report', methods=['POST'])
def report():
    if request.method == 'POST':
        result=request.form.to_dict()
        result=create_report(result['symbol'], result['date'])
        if result=="1":
            return render_template("report.html")


if __name__ == "__main__" :
    app.run()