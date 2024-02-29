import pandas as pd
import numpy as np
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV

def predict_trading_signals(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    def add_technical_indicators(df):
        # Calculate simple moving averages
        df['close_short'] = df['Close'].rolling(window=5).mean()
        df['close_long'] = df['Close'].rolling(window=15).mean()
        # Calculate the difference in closing prices
        delta = df['Close'].diff()
        # Positive gains (up) and losses (down)
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        # Calculate the Relative Strength (RS)
        rs = gain / loss
        # Calculate the Relative Strength Index (RSI)
        df['RSI'] = 100 - (100 / (1 + rs))
        # Exponential Moving Averages (EMA) for MACD
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        # Calculate the Moving Average Convergence Divergence (MACD)
        df['MACD'] = df['EMA12'] - df['EMA26']
        # Signal line
        df['Signal_line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        return df

    def label_data(df):
        # Create a binary 'Label' column for our machine learning model
        df['Label'] = 0
        df.loc[df['close_short'] > df['close_long'], 'Label'] = 1
        return df

    # Preprocessing
    df = add_technical_indicators(df)
    df = label_data(df)

    # Using a smaller subset of data for the grid search
    train_df = df.loc['2015-01-01':'2019-12-31']  # Adjust this range based on your dataset
    test_df = df.loc['2020-01-01':'2024-02-29']

    features = ['close_short', 'close_long', 'RSI', 'MACD', 'Signal_line']
    train_df.dropna(subset=features + ['Label'], inplace=True)
    X_train = train_df[features]
    y_train = train_df['Label']
    X_test = test_df[features].dropna()

    param_grid = {
        'n_estimators': [100,200.300],
        'max_depth': [None, 10, 20,30],
        'min_samples_split': [2, 5, 10],
        'min_samples_leaf': [1, 2, 4],
        'max_features': ['auto','sqrt']
    }


    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)

    # Extract the best model and make predictions
    best_model = grid_search.best_estimator_
    predictions = best_model.predict(X_test)
    test_df.loc[X_test.index, 'Predictions'] = predictions

    def add_signals_and_prices(df):
        df['Buy_Signal'] = 0
        df['Sell_Signal'] = 0
        df['pricebuy'] = np.nan
        df['pricesell'] = np.nan

        last_signal = None

        for i in range(1, len(df)):
            current_signal = None
            
            if df.iloc[i]['Predictions'] == 1 and df.iloc[i]['Close'] > df.iloc[i-1]['Close']:
                current_signal = 'buy'
            elif df.iloc[i]['Predictions'] == 0 and df.iloc[i]['Close'] < df.iloc[i-1]['Close'] * 0.99:
                current_signal = 'sell'
            
            if current_signal and current_signal != last_signal:
                if current_signal == 'buy':
                    df.at[df.index[i], 'pricebuy'] = df.iloc[i]['Close']
                    last_signal = 'buy'
                elif current_signal == 'sell':
                    df.at[df.index[i], 'pricesell'] = df.iloc[i]['Close']
                    last_signal = 'sell'

        df['Buy_Signal'] = df['pricebuy'].notnull().astype(int)
        df['Sell_Signal'] = df['pricesell'].notnull().astype(int)

        return df

    # Apply signals and prices to the test DataFrame
    test_df = add_signals_and_prices(test_df)
    test_df.reset_index(inplace=True)  # Reset index to make 'Date' a column again

    # Save the processed DataFrame to a CSV file
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, '01-data', 'ml_test_signals_prices.csv')
    test_df.to_csv(file_path, index=False)
    
    return test_df

