import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import plotly.graph_objects as go
import plotly.io as pio
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

def filter_date_range(df):
    """Filter the DataFrame to include data from Jan 1, 2020, to the present, retaining the 'Date' column."""
    start_date = pd.to_datetime('2020-01-01').date()  # Use a date for comparison
    
    # Ensure 'Date' column is in the correct format and filter out the epoch date if present
    if 'Date' in df.columns:
        # Convert 'Date' column to datetime and coerce errors to NaT
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.date
        # Create a mask to filter out rows with 'Date' at or before the Unix epoch
        mask = df['Date'] > pd.Timestamp('1970-01-01').date()
        # Apply the mask to filter the DataFrame
        df = df[mask]
        # Set 'Date' column as index
        filtered_df = df.set_index('Date')
        # Filter based on date range
        
        # Convert 'Close', 'pricebuy', and 'pricesell' columns to integers
        filtered_df['Close'] = filtered_df['Close'].astype(int)
        filtered_df['pricebuy'] = filtered_df['pricebuy'].astype(int).replace(0, np.nan)  # Replace 0 with NaN
        filtered_df['pricesell'] = filtered_df['pricesell'].astype(int).replace(0, np.nan)
        
    else:
        raise ValueError("DataFrame must have a 'Date' column.")
    return filtered_df



def plot_stock_signals(df=None, tickerSymbol=None, chart_directory='static/images'):
    df = filter_date_range(df)
    
    # Log data types of the dataframe
    print('3.1) load final dataframe')
    print('~~~~~~~~~~~~~')
    print(df.dtypes)
    print('~~~~~~~~~~~~~')

    print('first row')
    first_row_transposed = df.head(1).T
    print(first_row_transposed)
    current_directory = os.getcwd()

    # Plotting chart
    plt.figure(figsize=(40, 5))
    plt.plot(df.index, df['Close'].values, label=tickerSymbol)
    plt.plot(df.index, df['pricebuy'].values, color='red', label='Buy signal', marker='^', markersize=12)
    plt.plot(df.index, df['pricesell'].values, color='green', label='Sell signal', marker='v', markersize=12)

    # Setting x-axis ticks
    n = 5  # Adjust n as per your data
    plt.xticks(ticks=df.index[::n], labels=[date.strftime('%y-%m-%d') for date in df.index[::n]])
    plt.xticks(rotation=-75)

    # Adding legend, labels, and grid
    plt.legend(loc='upper left')
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('Price USD ($)', fontsize=12)
    plt.grid()

    # Exporting chart image
    chart_path = os.path.join(current_directory, chart_directory, 'chart.png')
    print('')
    print('3.1) export chart image')
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()

def interactive_plot_stock_signals(df=None, tickerSymbol=None):
    df = filter_date_range(df)

    print('3.1) load final dataframe')
    print('')
    print('~~~~~~~~~~~~~')
    print(df.dtypes)
    print('~~~~~~~~~~~~~')
    current_directory = os.getcwd()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=tickerSymbol))
    fig.add_trace(go.Scatter(x=df.index[df['pricebuy'].notnull()], y=df['pricebuy'].dropna(), mode='markers', name='Buy Signal', marker=dict(color='green', size=10, symbol='triangle-up')))
    fig.add_trace(go.Scatter(x=df.index[df['pricesell'].notnull()], y=df['pricesell'].dropna(), mode='markers', name='Sell Signal', marker=dict(color='red', size=10, symbol='triangle-down')))

    fig.update_layout(title=f"{tickerSymbol} Stock Signals Chart",
                      xaxis_title='Date',
                      yaxis_title='Price USD ($)',
                      xaxis=dict(
                          rangeslider=dict(visible=False),
                          type='date',
                          tickmode='auto',
                          tickformat='%Y-%m-%d',
                          tick0=df.index.min(),
                          dtick=86400000.0
                      ),
                      width=1400,
                      height=600)

    return pio.to_html(fig, full_html=False)

def Last_record(df=None):
    # Validate if the input is a DataFrame
    if not isinstance(df, pd.DataFrame):
        raise ValueError("The input is not a pandas DataFrame.")
    
    # Specify columns of interest
    cols = ['Open', 'High', 'Low', 'Close', 'Volume', 'cumulative_profit']
    
    # Verify all specified columns exist in the DataFrame
    missing_cols = [col for col in cols if col not in df.columns]
    if missing_cols:
        raise ValueError(f"Missing columns in DataFrame: {', '.join(missing_cols)}")
    
    last_record_filtered = df.iloc[-1][cols]

    formatted_last_record = {
        'Open': "${:,.2f}".format(last_record_filtered['Open']),
        'High': "${:,.2f}".format(last_record_filtered['High']),
        'Low': "${:,.2f}".format(last_record_filtered['Low']),
        'Close': "${:,.2f}".format(last_record_filtered['Close']),
        'Volume': "{:,}".format(int(last_record_filtered['Volume'])),
        'cumulative_profit': "${:,.2f}".format(last_record_filtered['cumulative_profit'])
    }

    print(formatted_last_record)
    return formatted_last_record
