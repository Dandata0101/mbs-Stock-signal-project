import yfinance as yf
import datetime
import pandas as pd
import numpy as np
import warnings
import os

warnings.filterwarnings('ignore')

def create_dataframe(tickerSymbol='MSFT'):
    # Clear the console
    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n\n1.1) Starting stock data extraction')

    # Get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)

    # Define the date range
    end_date = datetime.date.today()  # Today's date
    start_date = datetime.date(2013, 1, 1)  # Start date

    # Fetch the historical data
    df = tickerData.history(start=start_date, end=end_date)

    # Resetting the index to make 'Date' a column, if it's not already
    df.reset_index(inplace=True)

    # Convert 'Date' column to string format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    print('~~~~~~~~~~~~~')
    print('Data types after adjustment:')
    print(df.dtypes)  # 'Date' will now show as type 'object'
    print('~~~~~~~~~~~~~')

    return df

