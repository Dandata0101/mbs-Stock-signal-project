from flask import Flask, request, render_template, jsonify, session, url_for, flash, redirect,send_file
import matplotlib
matplotlib.use('Agg') 
import os
from scripts_buysell.yahoofinance import create_dataframe
from scripts_buysell.ml_buysellfx import predict_trading_signals
from scripts_buysell.profit_calc import calculate_profit
from scripts_buysell.ml_chart_export import plot_stock_signals, interactive_plot_stock_signals,first_buy_record, Last_record
from scripts_buysell.excel_export import export_df_to_excel_with_chart
from EmailBody.emailbody import generate_email_body
from scripts_buysell.sendemail import send_email
from waitress import serve
import subprocess
import re
import threading
from dotenv import load_dotenv
load_dotenv()
import requests

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# Define the format_number function
def format_USD(value):
    return "${:,.0f}".format(value)

def format_number_commas(value):
    return "{:,.0f}".format(value)

# Register the filter with the app
app.template_filter('format_USD')(format_USD)
app.template_filter('format_number_commas')(format_number_commas)


'''
# Set the default TensorBoard URL for development; in production, this should be set via an environment variable
default_tensorboard_url = "http://y-data.fr/tensorboard"
# In production, the TENSORBOARD_BASE_URL environment variable should be set to "https://y-data.fr"
TENSORBOARD_BASE_URL = os.getenv("TENSORBOARD_BASE_URL", default_tensorboard_url)

url_found_event = threading.Event()
# The full TensorBoard URL includes the base path to the TensorBoard route; this might not be necessary if your reverse proxy handles it
tensorboard_url = TENSORBOARD_BASE_URL

def find_tensorboard_port(process):
    global tensorboard_url
    url_pattern = re.compile(r'http://localhost:\d+')
    while True:
        line = process.stdout.readline()
        if not line:
            break  # Process has terminated
        match = url_pattern.search(line)
        if match:
            tensorboard_url = match.group()
            url_found_event.set()  # Signal that the URL has been found
            break

def start_tensorboard(logdir='logs/fit'):
    command = ['tensorboard', '--logdir', logdir, '--port', '--bind_all']  # Removed '--bind_all' for production
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True, bufsize=1)
    threading.Thread(target=find_tensorboard_port, args=(process,)).start()

@app.route('/tensorboard')
def show_tensorboard():
    # In development, check if the TensorBoard URL is available; this may not be necessary in production if Render handles it
    if TENSORBOARD_BASE_URL == default_tensorboard_url and not url_found_event.wait(timeout=10):
        return "TensorBoard did not start in time, or the URL could not be found.", 503
    # Provide the TensorBoard URL to the template; this could be directly the Render.com URL in production
    return render_template('tensor.html', tensorboard_url=tensorboard_url)

@app.route('/healthcheck')
def healthcheck():
    try:
        # Attempt to connect to the TensorBoard service
        response = requests.get(tensorboard_url)
        if response.status_code == 200:
            return 'TensorBoard is up and running.', 200
        else:
            return f'TensorBoard check failed with status {response.status_code}.', 500
    except requests.exceptions.RequestException as e:
        # TensorBoard service is not reachable
        return f'Error connecting to TensorBoard: {e}', 500
'''

#<!--Home page------------------------------------------------------------------------------------------------------>

@app.route('/')
def home():
# Now serving home.html as the landing page
    return render_template('home.html', title='Welcome')

#<!--Start of Stock application------------------------------------------------------------------------------------->
@app.route('/stockindex')
def stockindex():

    default_params = {
        'close_short_window': 5,
        'close_long_window': 20,
    }
    return render_template('stockindex.html', title='Home - MBS Stock Analysis',default_params=default_params)

def parse_grid_search_params(request):
    """Parse grid search parameters from the request, providing defaults if necessary."""
    def parse_list(value, convert_func, default):
        """Parse a comma-separated string into a list, applying a conversion function, with a default."""
        if value:
            try:
                parsed = [convert_func(x.strip()) for x in value.split(',') if x.strip()]
                return parsed if parsed else default
            except ValueError:
                return default
        return default

    def parse_max_features(value, default):
        """Parse the max_features parameter to ensure it's a valid list of strings."""
        valid_options = ['auto', 'sqrt', 'log2']
        if value:
            parsed = [x.strip() for x in value.split(',') if x.strip() in valid_options]
            return parsed if parsed else default
        return default

    param_grid = {
        'n_estimators': parse_list(request.values.get('n_estimators'), int, [200]),
        'max_depth': parse_list(request.values.get('max_depth'), lambda x: None if x.lower() == 'none' else int(x), [20]),
        'min_samples_split': parse_list(request.values.get('min_samples_split'), int, [2]),
        'min_samples_leaf': parse_list(request.values.get('min_samples_leaf'), int, [2]),
        'max_features': parse_max_features(request.values.get('max_features'), ['sqrt'])
    }

    # Parsing additional model parameters
    close_short_window = request.values.get('close_short_window', default=5, type=int)
    close_long_window = request.values.get('close_long_window', default=20, type=int)

    return param_grid,close_short_window, close_long_window

@app.route('/stockresults', methods=['GET', 'POST'])
def stockresults():
    stock_symbol = request.values.get('stock')
    if not stock_symbol:
        flash('Missing required query parameter: stock', 'error')
        return redirect(url_for('stockindex'))

    # Adjusted to use the new parsing function
    param_grid, close_short_window, close_long_window = parse_grid_search_params(request)

    try:
        df,company_details=create_dataframe(stock_symbol)
        data=df

        # Check if the data is empty, indicating an incorrect stock symbol
        if data.empty or 'longName' not in company_details:
            flash('Incorrect stock symbol, please provide a valid symbol', 'error')
            return redirect(url_for('stockindex'))
        
        company_name=company_details['longName']
        
        test_df, accuracy, precision, recall, f1, feature_importances, importance_df, metrics_df = predict_trading_signals(data, param_grid=param_grid,close_short_window=close_short_window,close_long_window=close_long_window)
        profit = calculate_profit(test_df)
        firstbuy=first_buy_record(profit)
        lastrecord = Last_record(profit)
        chart_html = interactive_plot_stock_signals(df=profit, tickerSymbol=stock_symbol)
        export = export_df_to_excel_with_chart(df=profit, tickerSymbol=stock_symbol)

        # Set the tickerSymbol in session here
        session['tickerSymbol'] = stock_symbol  
        session['company_name'] = company_name
        
        file_name = f'{stock_symbol}_stock.xlsx'
        session['export_file_name'] = file_name

        return render_template("stockresults.html", chart=chart_html,company_name=company_name,company_details=company_details, stock=stock_symbol,firstbuy=firstbuy,lastrecord=lastrecord, accuracy=accuracy, feature_importances=importance_df.to_dict('records'))
    
    except Exception as e:
        print(e)  # For debugging
        flash(f'Error: {str(e)}', 'error')  # Flash the error message
        return redirect(url_for('stockindex'))  # Redirect to the index page

@app.route('/download')
def download_file():
    file_name = session.get('export_file_name')
    if file_name:
        base_directory = os.path.join(os.getcwd(), '03-output')
        full_path = os.path.join(base_directory, file_name)
        if os.path.exists(full_path):
            return send_file(full_path, as_attachment=True)
        else:
            return "File not found.", 404
    else:
        return "No file specified.", 400    

@app.route('/ty', methods=['GET'])
def thank_you():
    email_address = request.args.get('email')
    if not email_address:
        return render_template('error.html', error='Missing required query parameter: email')

    tickerSymbol = session.get('tickerSymbol')
    if not tickerSymbol:
        return render_template('error.html', error='Ticker symbol not found. Please initiate stock query first.')

    try:
        email_body = generate_email_body(tickerSymbol=tickerSymbol)
        send_email(email_body=email_body, recipient_emails=[email_address])
        flash('Email sent successfully!', 'success') 
        return redirect( url_for('stockindex'))   # Redirect the user where you want them to see the flash message
    except Exception as e:
        return render_template('error.html', error=str(e))

if __name__ == '__main__':
    # Start TensorBoard

    # Configure the Flask app's debug mode based on the FLASK_DEBUG environment variable
    app.debug = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']

    # Get the port number from the PORT environment variable
    port = int(os.getenv('PORT', 8000))

    # Run the app with Waitress server on the specified host and port
    serve(app, host="0.0.0.0", port=port)

#<!--End of Stock application------------------------------------------------------------------------------------->