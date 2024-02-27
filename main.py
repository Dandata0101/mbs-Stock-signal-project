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

def safe_upper(input_string):
    """Safely convert a string to uppercase, handling None."""
    if input_string is None:
        return None
    return input_string.upper()

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

        try:
            # Fetch and process stock data
            dataf = create_dataframe(stock_symbol)
            fx = buysellfx(dataf)
            last_record = Last_record(fx)  # Get the last record of the stock data as a dictionary
            chart_html = interactive_plot_stock_signals(df=fx, tickerSymbol=stock_symbol)

            # Set session variable for tickerSymbol
            session['tickerSymbol'] = safe_upper(stock_symbol)  # Store tickerSymbol in session

            return render_template("stock.html", chart=chart_html, stock=stock_symbol, data=last_record)
        except Exception as e:
            print(e)  # Print exception to console for debugging
            return jsonify({'error': str(e)}), 500
    else:
        # Handle GET request or show a form to submit stock symbol and email
        return render_template('index.html')

@app.route('/ty', methods=['GET'])
def thank_you():
    email_address = request.args.get('email')

    if not email_address:
        return render_template('error.html', error='Missing required query parameter: email')

    tickerSymbol = session.get('tickerSymbol')  # Retrieve tickerSymbol from session
    if not tickerSymbol:
        return render_template('error.html', error='Ticker symbol not found. Please initiate stock query first.')

    try:
        email_body = generate_email_body(tickerSymbol=tickerSymbol)
        send_email(email_body=email_body, recipient_emails=[email_address])
        return render_template('ty.html', email_address=email_address)
    except Exception as e:
        return render_template('error.html', error=str(e))

@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error='Internal Server Error')
@app.errorhandler(500)
def internal_error(error):
    return render_template('error.html', error='Internal Server Error')

if __name__ == '__main__':
    app.debug = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']
    serve(app, host="0.0.0.0", port=int(os.getenv('FLASK_PORT', 8000)))
