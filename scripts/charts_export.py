import matplotlib.pyplot as plt
import os
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

# Assuming 'buysellfx' script is properly placed in your project structure.
#from scripts.buysellfx import df

def plot_stock_signals(df=None, tickerSymbol=None, chart_directory='static/images'):
   
    # Print data types of the dataframe
    print('3.1) load final dataframe')
    print('')
    print('~~~~~~~~~~~~~')
    print(df.dtypes)
    print('~~~~~~~~~~~~~')
    current_directory = os.getcwd()

    # Plotting chart
    plt.figure(figsize=(15, 5))
    plt.plot(df.index, df['Close'].values, label=tickerSymbol)
    plt.plot(df.index, df['pricebuy'].values, color='red', label='Buy signal', marker='^', markersize=12)
    plt.plot(df.index, df['pricesell'].values, color='green', label='Sell signal', marker='v', markersize=12)

    # Setting x-axis ticks
    n = 5  # Adjust n as per your data
    plt.xticks(ticks=df.index[::n], labels=df.index[::n])
    plt.xticks(rotation=-75)

    # Adding legend, labels, and grid
    plt.legend()
    plt.xlabel('Date', fontsize=12)
    plt.ylabel('price USD ($)', fontsize=12)
    plt.grid()

    # Exporting chart image
    chart_path = os.path.join(current_directory, chart_directory, 'chart.png')
    print('')
    print('3.1) export chart image')
    plt.savefig(chart_path, bbox_inches='tight')
    plt.close()

# Example usage (you'll need to define `df` and `tickerSymbol` appropriately)
# plot_stock_signals(df, tickerSymbol)

# scripts/charts_export.py
import plotly.graph_objects as go

def new_plot_stock_signals(df=None, tickerSymbol=None):
    fig = go.Figure()

    # Add traces for the stock close prices, buy signals, and sell signals
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], mode='lines', name=tickerSymbol))
    fig.add_trace(go.Scatter(x=df.index, y=df['pricebuy'], mode='markers', name='Buy signal', marker=dict(color='red', size=10, symbol='triangle-up')))
    fig.add_trace(go.Scatter(x=df.index, y=df['pricesell'], mode='markers', name='Sell signal', marker=dict(color='green', size=10, symbol='triangle-down')))

    # Update layout
    fig.update_layout(title=f"{tickerSymbol} Stock Signals", xaxis_title='Date', yaxis_title='Price USD ($)', xaxis_rangeslider_visible=True)

    # Generate HTML div string without full HTML document structure
    plot_html = fig.to_html(full_html=False)
    return plot_html
