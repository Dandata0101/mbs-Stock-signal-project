import yfinance as yf
import datetime
import pandas as pd
import warnings
import os
from fredapi import Fred

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
    
    def fedrate(start_date, end_date, fedkey):        
        # Initialize Fred with the provided API key
        fred = Fred(api_key=fedkey)
        
        # Fetch the Federal Funds Effective Rate data
        federal_funds_rate = fred.get_series('FEDFUNDS', observation_start=start_date, observation_end=end_date)
        
        # Convert the Series into a DataFrame and rename the columns
        fedrate_df = federal_funds_rate.to_frame(name='fedrate')
        fedrate_df.reset_index(inplace=True)
        fedrate_df.rename(columns={'index': 'Date'}, inplace=True)
        fedrate_df['Date'] = pd.to_datetime(fedrate_df['Date']).dt.strftime('%Y-%m-%d')
        current_directory = os.getcwd()
        
        print(current_directory)
        #fedrate_df.to_excel(current_directory+'/01-data/test01_fedrate_export.xlsx')
        
        return fedrate_df
 
    clear_console()
    print('\n\n1.1) Starting stock data extraction')

    # Define the date range
    end_date = datetime.date(2024, 3, 1)  # Today's date
    start_date = datetime.date(2013, 1, 1)  # Start date



    # Fetch stock data for the specified ticker
    df_stock = fetch_data(tickerSymbol, start_date, end_date)

    # Fetch VIX data
    df_vix = fetch_data('^VIX', start_date, end_date)

    # Fetch Fed Rate data
    fedkey = os.getenv('fedkey')  
    df_fedrate = fedrate(start_date, end_date,fedkey=fedkey)

    # Merging the dataframes on the 'Date' column
    df_merged = pd.merge(df_stock, df_vix, on='Date', how='left')
    df_merged = pd.merge(df_merged, df_fedrate, on='Date', how='left')

    current_directory = os.getcwd()
    # Forward fill the 'fedrate' column to propagate the last valid observation forward
    df_merged['fedrate'] = df_merged['fedrate'].fillna(method='ffill')
    df_merged.to_excel(current_directory + '/01-data/input_YahooFin.xlsx', index=False)

    print('~~~~~~~~~~~~~')
    print('Data types after adjustment:')
    print(df_merged.dtypes)
    print('~~~~~~~~~~~~~')
    
    return df_merged
