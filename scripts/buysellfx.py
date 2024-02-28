import pandas as pd
import numpy as np
import warnings

# Assuming create_dataframe is defined elsewhere and works correctly

# Suppress warnings
warnings.filterwarnings('ignore')

def buysellfx(df):
    short, long = 5, 20
    print('2.2) adding rolling averages')
    df['close_short'] = df['Close'].rolling(window=short).mean()
    df['close_long'] = df['Close'].rolling(window=long).mean()
    df.index = pd.to_datetime(df.index)  # Convert index to datetime, keep it this way
    
    status = 0
    pricebuy, pricesell, profit, transdays = [], [], [], []
    temp_buyprice, temp_buyindex = [], []

    for i in range(len(df) - 1):
        if df['close_short'][i] > df['close_long'][i] and status != 1:
            status = 1
            pricebuy.append(df['Open'][i + 1])
            pricesell.append(np.nan)
            profit.append(np.nan)
            transdays.append(np.nan)
            temp_buyprice.append(df['Open'][i + 1])
            temp_buyindex.append(i + 1)
        elif df['close_short'][i] < df['close_long'][i] and status != 0:
            status = 0
            pricebuy.append(np.nan)
            pricesell.append(df['Open'][i + 1])
            profit.append(df['Open'][i + 1] - temp_buyprice[-1])
            transdays.append(i + 1 - temp_buyindex[-1])
        else:
            pricebuy.append(np.nan)
            pricesell.append(np.nan)
            profit.append(np.nan)
            transdays.append(np.nan)

    # Append a final set of NaNs to match the DataFrame length
    pricebuy.append(np.nan)
    pricesell.append(np.nan)
    profit.append(np.nan)
    transdays.append(np.nan)
    
    # Assigning the lists as new columns in the DataFrame
    df['pricebuy'] = pricebuy
    df['pricesell'] = pricesell
    df['profit'] = profit
    df['transdays'] = transdays
    # Calculate cumulative profit
    df['cumulative_profit'] = df['profit'].cumsum().fillna(method='ffill')
    
    print(df.dtypes)

    return df

# Usage of the function remains the same
