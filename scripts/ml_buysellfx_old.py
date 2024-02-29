import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier

def predict_trading_signals(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    def add_technical_indicators(df):
        df['close_short'] = df['Close'].rolling(window=5).mean()
        df['close_long'] = df['Close'].rolling(window=20).mean()
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal_line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        return df

    def label_data(df):
        df['Label'] = 0
        df.loc[df['close_short'] > df['close_long'], 'Label'] = 1
        return df

    df = add_technical_indicators(df)

    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = pd.to_datetime(df.index, errors='coerce')

    train_df = df.loc['2013-01-01':'2019-12-31']
    test_df = df.loc['2020-01-01':]

    train_df = label_data(train_df)
    features = ['close_short', 'close_long', 'RSI', 'MACD', 'Signal_line']
    train_df.dropna(subset=features + ['Label'], inplace=True)

    X_train = train_df[features]
    y_train = train_df['Label']
    X_test = test_df[features].dropna()

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Ensure predictions are added to test_df
    predictions = model.predict(X_test)
    test_df.loc[X_test.index, 'Predictions'] = predictions

    def add_signals_and_prices(df):
        df['Buy_Signal'] = 0
        df['Sell_Signal'] = 0
        df['pricebuy'] = np.nan
        df['pricesell'] = np.nan

        last_signal = None  # Track the last signal (buy or sell)

        for i in range(1, len(df)):
            current_signal = None
            
            if df.iloc[i]['Predictions'] == 1 and df.iloc[i]['Close'] > df.iloc[i-1]['Close']:
                current_signal = 'buy'
            elif df.iloc[i]['Predictions'] == 0 and df.iloc[i]['Close'] < df.iloc[i-1]['Close'] * 0.99: # Sell if current price is 1% less than previous price
                current_signal = 'sell'
            
            if current_signal and current_signal != last_signal:
                if current_signal == 'buy':
                    df.at[df.index[i], 'pricebuy'] = df.iloc[i]['Close']
                    last_signal = 'buy'
                elif current_signal == 'sell':
                    df.at[df.index[i], 'pricesell'] = df.iloc[i]['Close']
                    last_signal = 'sell'

        # Update signals based on prices
        df['Buy_Signal'] = df['pricebuy'].notnull().astype(int)
        df['Sell_Signal'] = df['pricesell'].notnull().astype(int)

        return df


    # Apply the function to test_df after predictions have been added
    test_df = add_signals_and_prices(test_df)
    
    # Reset index to make 'Date' a column again if necessary
    test_df.reset_index(inplace=True)

    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, '01-data', 'ml_test_signals_prices.csv')
    test_df.to_csv(file_path, index=False)
    
    return test_df
