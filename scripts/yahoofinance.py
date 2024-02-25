import yfinance as yf
import datetime
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')

print('')
print('')
print('1.1) starting stock data extraction')


# Define the ticker symbol
tickerSymbol = 'AAPL'
yrs= 1

# Get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

end_date = datetime.date.today()  # Today's date
start_date = end_date - datetime.timedelta(days=yrs*365) 

# Get the historical prices for this ticker
df = tickerData.history(period='1d', start=start_date, end=end_date) 

def create_dataframe():
    data = {'Column1': [1, 2, 3], 'Column2': [4, 5, 6]}
    df=tickerData.history(period='1d', start=start_date, end=end_date)
    return df

print('~~~~~~~~~~~~~')
print(df.dtypes)
print('~~~~~~~~~~~~~')

print('')
print('1.2) Extraction completed')
print('')