from flask import Flask, request, render_template, jsonify

import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend
import matplotlib.pyplot as plt

from scripts.yahoofinance import create_dataframe
from scripts.buysellfx import buysellfx
from scripts.charts_export import plot_stock_signals
from scripts.excel_export import export_df_to_excel_with_chart
from EmailBody.emailbody import generate_email_body
from scripts.sendemail import send_email
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='MBS Stock Analysis')

@app.route('/stock')
def stock():
    stock = request.args.get('stock')
    if not stock:
        # If 'stock' parameter is missing, return an error message
        return jsonify({'error': 'Missing required query parameter: stock'}), 400
    
    try:
        data = create_dataframe(stock)
        fx = buysellfx(data)
        chart = plot_stock_signals(df=fx, tickerSymbol=stock)
        # Ensure you pass necessary data to render in your template, if needed
        return render_template("stock.html")
    except Exception as e:
        # Log the exception or handle it as needed
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)
