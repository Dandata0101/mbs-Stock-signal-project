from flask import Flask, request, render_template, jsonify, redirect, url_for
import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend
import matplotlib.pyplot as plt
import os
from scripts.yahoofinance import create_dataframe
from scripts.buysellfx import buysellfx
from scripts.charts_export import plot_stock_signals
from scripts.excel_export import export_df_to_excel_with_chart
from EmailBody.emailbody import generate_email_body
from scripts.sendemail import send_email

# Importing waitress for serving the application
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    # Home page route
    return render_template('index.html', title='Home - MBS Stock Analysis')

@app.route('/stock', methods=['GET', 'POST'])
def stock():
    # Route for handling stock data and displaying results
    if request.method == 'GET':
        stock_symbol = request.args.get('stock')
        emails = request.args.get('email')
        email=[emails]

        print("Email received:", email) 
        if not stock_symbol:
            return jsonify({'error': 'Missing required query parameter: stock'}), 400
        
        try:
            data = create_dataframe(stock_symbol)
            fx = buysellfx(data)
            chart = plot_stock_signals(df=fx, tickerSymbol=stock_symbol)
            export = export_df_to_excel_with_chart(df=fx, tickerSymbol=stock_symbol)
            body=generate_email_body(tickerSymbol=stock_symbol)
            email=send_email(email_body=body,recipient_emails=email)
            return render_template("stock.html", chart=chart, stock=stock_symbol, data=data)
        except Exception as e:
            return jsonify({'error': str(e)}), 500



@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal Server Error'}), 500

if __name__ == '__main__':
    app.debug = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']
    serve(app, host="0.0.0.0", port=int(os.getenv('FLASK_PORT', 8000)))