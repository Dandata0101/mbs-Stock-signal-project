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

#Global variable to store TensorBoard's port
tensorboard_port = None

def find_tensorboard_port(log_output):
    global tensorboard_url
    for line in log_output.stdout:
        print("TensorBoard Output: ", line)
        if "TensorBoard 2" in line and "at http://localhost:" in line:
            tensorboard_url = line.split("at ")[1].split(" ")[0].strip()
            break

def start_tensorboard(logdir='logs/fit'):
    command = ['tensorboard', '--logdir', logdir, '--bind_all', '--port', '0']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, universal_newlines=True)
    threading.Thread(target=find_tensorboard_port, args=(process,)).start()

@app.route('/tensorboard')
def show_tensorboard():
    if tensorboard_url is None:
        return "TensorBoard is not running or the URL is not available.", 503
    # Adjust URL based on environment
    final_url = os.getenv('TENSORBOARD_URL', tensorboard_url)
    return render_template('tensor.html', tensorboard_url=final_url)

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
    app.debug = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']
    serve(app, host="0.0.0.0", port=int(os.getenv('PORT', 8000)))

#<!--End of Stock application------------------------------------------------------------------------------------->
