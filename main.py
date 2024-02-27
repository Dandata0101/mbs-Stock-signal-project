from flask import Flask, request, render_template, jsonify, session
import os
from scripts.yahoofinance import create_dataframe
from scripts.buysellfx import buysellfx
from scripts.charts_export import interactive_plot_stock_signals, Last_record
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
    # Adjust for both GET and POST methods
    stock_symbol = request.form.get('stock')
    email_address = request.form.get('email')
    email=[email_address]

    try:
        # Fetch and process stock data
        dataf = create_dataframe(stock_symbol)
        fx = buysellfx(dataf)
        last_record = Last_record(fx)  # Get the last record of the stock data as a dictionary
        chart_html = interactive_plot_stock_signals(df=fx, tickerSymbol=stock_symbol)

        # Prepare and send email
        email_body = generate_email_body(tickerSymbol=stock_symbol)
        send_email(email_body=email_body, recipient_emails=email)

        return render_template("stock.html", chart=chart_html, stock=stock_symbol, data=last_record)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.debug = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']
    serve(app, host="0.0.0.0", port=int(os.getenv('FLASK_PORT', 8000)))
