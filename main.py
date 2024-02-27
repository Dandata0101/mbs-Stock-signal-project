from flask import Flask, request, render_template, jsonify, session
import os
from scripts.yahoofinance import create_dataframe
from scripts.buysellfx import buysellfx
from scripts.charts_export import plot_stock_signals, interactive_plot_stock_signals, Last_record
from scripts.excel_export import export_df_to_excel_with_chart
from EmailBody.emailbody import generate_email_body
from scripts.sendemail import send_email
from waitress import serve

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Home - MBS Stock Analysis')

@app.route('/stock', methods=['GET', 'POST'])
def stock():
    if request.method == 'GET':
        stock_symbol = request.args.get('stock')
        if not stock_symbol:
            return jsonify({'error': 'Missing required query parameter: stock'}), 400

        session['tickerSymbol'] = stock_symbol
        try:
            dataf = create_dataframe(stock_symbol)
            fx = buysellfx(dataf)
            last = Last_record(fx)  # Get the last record of the stock data as a dictionary
            chart_html = interactive_plot_stock_signals(df=fx, tickerSymbol=stock_symbol)
            body=generate_email_body(tickerSymbol=stock_symbol)
            email=send_email(email_body=body,recipient_emails=email)

            return render_template("stock.html", chart=chart_html, stock=stock_symbol, data=last)
        except Exception as e:
            return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.debug = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']
    serve(app, host="0.0.0.0", port=int(os.getenv('FLASK_PORT', 8000)))
