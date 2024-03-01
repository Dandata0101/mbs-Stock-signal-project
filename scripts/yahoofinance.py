import yfinance as yf
import datetime
import pandas as pd
import warnings
import os

warnings.filterwarnings('ignore')

def create_dataframe(tickerSymbol='MSFT'):
    # Function to clear the console
    def clear_console():
        os.system('cls' if os.name == 'nt' else 'clear')

    # Function to fetch stock data
    def fetch_data(symbol, start_date, end_date):
        tickerData = yf.Ticker(symbol)
        df = tickerData.history(start=start_date, end=end_date)
        df.reset_index(inplace=True)
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
        if symbol == '^VIX':
            df = df[['Date', 'Close']].rename(columns={'Close': 'VIX'})
        return df

    clear_console()
    print('\n\n1.1) Starting stock data extraction')

    # Define the date range
    end_date = datetime.date.today()  # Today's date
    start_date = datetime.date(2013, 1, 1)  # Start date

    # Fetch stock data for the specified ticker
    df_stock = fetch_data(tickerSymbol, start_date, end_date)

    # Fetch VIX data
    df_vix = fetch_data('^VIX', start_date, end_date)

    # Merging the dataframes on the 'Date' column
    df_merged = pd.merge(df_stock, df_vix, on='Date', how='left')

    print('~~~~~~~~~~~~~')
    print('Data types after adjustment:')
    print(df_merged.dtypes)
    print('~~~~~~~~~~~~~')

    return df_merged

