from flask import Flask, request, render_template, jsonify, session
import matplotlib
matplotlib.use('Agg')  # Use 'Agg' backend for non-interactive plots
import os
from scripts.yahoofinance import create_dataframe
from scripts.ml_buysellfx import predict_trading_signals
from scripts.profit_calc import calculate_profit
from scripts.ml_chart_export import plot_stock_signals, interactive_plot_stock_signals, Last_record
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
        'n_estimators': parse_list(request.values.get('n_estimators'), int, [100, 200]),
        'max_depth': parse_list(request.values.get('max_depth'), lambda x: None if x.lower() == 'none' else int(x), [None, 10, 20]),
        'min_samples_split': parse_list(request.values.get('min_samples_split'), int, [2, 5]),
        'min_samples_leaf': parse_list(request.values.get('min_samples_leaf'), int, [1, 2]),
        'max_features': parse_max_features(request.values.get('max_features'), ['auto', 'sqrt'])
    }

    return param_grid

@app.route('/stock', methods=['GET', 'POST'])
def stock():
    stock_symbol = request.values.get('stock')
    if not stock_symbol:
        return jsonify({'error': 'Missing required query parameter: stock'}), 400

    param_grid = parse_grid_search_params(request)
    
    try:
        data = create_dataframe(stock_symbol)
        test_df, accuracy, precision, recall, f1, feature_importances, importance_df = predict_trading_signals(data, param_grid=param_grid)
        profit = calculate_profit(test_df)
        last_record = Last_record(profit)
        chart_html = interactive_plot_stock_signals(df=profit, tickerSymbol=stock_symbol)
        export = export_df_to_excel_with_chart(df=profit, tickerSymbol=stock_symbol)

        return render_template("stock.html", chart=chart_html, stock=stock_symbol, data=last_record, accuracy=accuracy, feature_importances=importance_df.to_dict('records'))
    except Exception as e:
        print(e)  # For debugging
        return jsonify({'error': str(e)}), 500

# Additional routes and error handlers...

if __name__ == '__main__':
    app.debug = os.getenv('FLASK_DEBUG', 'False').lower() in ['true', '1']
    serve(app, host="0.0.0.0", port=int(os.getenv('PORT', 8000)))
