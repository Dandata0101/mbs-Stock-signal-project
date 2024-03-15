import yfinance as yf
import datetime
import pandas as pd
import warnings
import os

warnings.filterwarnings('ignore')

def fetch_data(symbol, start_date, end_date):
    tickerData = yf.Ticker(symbol)
    df = tickerData.history(start=start_date, end=end_date)
    df.reset_index(inplace=True)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')
    if symbol == '^VIX':
        df = df[['Date', 'Close']].rename(columns={'Close': 'VIX'})
    elif symbol == '^DJI':
        df = df[['Date', 'Close']].rename(columns={'Close': 'DJI'})
    return df

def fetch_company_details(tickerSymbol):
    tickerData = yf.Ticker(tickerSymbol)
    info = tickerData.info

    company_details = info
    return company_details

def create_dataframe(tickerSymbol='MSFT'):
    print('1.1) Starting stock data extraction')

    end_date = datetime.date.today()
    start_date = datetime.date(2013, 1, 1)

    df_stock = fetch_data(tickerSymbol, start_date, end_date)
    df_vix = fetch_data('^VIX', start_date, end_date)
    df_dji = fetch_data('^DJI', start_date, end_date)

    # Merge stock data, VIX data, and DJI data
    df_merged = pd.merge(df_stock, df_vix, on='Date', how='left')
    df_merged = pd.merge(df_merged, df_dji, on='Date', how='left')

    current_directory = os.getcwd()
    df_merged.to_excel(current_directory + '/01-data/input_YahooFin.xlsx', index=False)

    # Fetch and return company details as well
    company_details = fetch_company_details(tickerSymbol)
    
    return df_merged, company_details

