import yfinance as yf
import datetime
import pandas as pd
import numpy as np
import warnings
import os

warnings.filterwarnings('ignore')

def create_dataframe(tickerSymbol='MSFT'):
    os.system('cls' if os.name == 'nt' else 'clear')

    print('\n\n1.1) starting stock data extraction')
    yrs = 1

    # Get data on this ticker
    tickerData = yf.Ticker(tickerSymbol)

    end_date = datetime.date.today()  # Today's date
    start_date = end_date - datetime.timedelta(days=yrs * 365)
    df = tickerData.history(start=start_date, end=end_date)
    
    print('~~~~~~~~~~~~~')
    print(df.dtypes)  # Now this works because df is defined
    print('~~~~~~~~~~~~~')
    print('\n1.2) Extraction completed\n')
    return df

