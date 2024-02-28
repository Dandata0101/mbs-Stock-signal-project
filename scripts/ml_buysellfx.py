import pandas as pd
import numpy as np
import os
import openpyxl
from sklearn.ensemble import RandomForestClassifier

def predict_trading_signals(df):
    # Correctly convert 'Date' column from string to datetime format
    df['Date'] = pd.to_datetime(df['Date'])  # Corrected line
    # Set the 'Date' column as the DataFrame's index
    df.set_index('Date', inplace=True)

    print('~~~~~~~~~~~~~')
    print('Data types after adjustment:')
    print(df.dtypes)  # 'Date' will now show as type 'datetime64[ns]' since it's the index
    print('~~~~~~~~~~~~~')

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
        df['Label'] = 0  # Default to 'sell'
        df.loc[df['close_short'] > df['close_long'], 'Label'] = 1  # 'buy' signal
        return df

    df = add_technical_indicators(df)

    if df.dropna().empty:
        print("DataFrame is empty after adding technical indicators.")
        return pd.DataFrame()

    if not pd.api.types.is_datetime64_any_dtype(df.index):
        df.index = pd.to_datetime(df.index, errors='coerce')

    train_df = df.loc['2013-01-01':'2019-12-31']
    test_df = df.loc['2020-01-01':]

    if train_df.empty or test_df.empty:
        print("Training or Test DataFrame is empty after date filtering.")
        return pd.DataFrame()

    train_df = label_data(train_df)
    features = ['close_short', 'close_long', 'RSI', 'MACD', 'Signal_line']
    train_df.dropna(subset=features + ['Label'], inplace=True)

    if train_df.empty:
        print("Training DataFrame is empty after dropping NaN values.")
        return pd.DataFrame()

    X_train = train_df[features]
    y_train = train_df['Label']
    X_test = test_df[features].dropna()

    if X_train.empty or y_train.empty:
        print("X_train or y_train is empty. Check your data and preprocessing steps.")
        return pd.DataFrame()

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    try:
        model.fit(X_train, y_train)
    except ValueError as e:
        print(f"Error fitting model: {e}")
        return pd.DataFrame()

    if X_test.empty:
        print("X_test is empty. No data to predict.")
        return pd.DataFrame()

    predictions = model.predict(X_test)
    test_df.loc[X_test.index, 'Predictions'] = predictions
    print('~~~~~~~~~~~~~')
    print('Data types test df:')
    print(test_df.dtypes)  # 'Date' will now show as type 'datetime64[ns]' since it's the index
    print('~~~~~~~~~~~~~')

    first_row_vertical = df.iloc[0].to_frame()

    print('Print the first row vertically')
    print(first_row_vertical)


   
    # Paths and directory
    current_directory = os.getcwd()
    print(current_directory)

    # Include the directory path in the file name
    file_path = current_directory + '/01-data/ml_test.csv'

    # Write the DataFrame to an Excel file in the specified directory
    test_df.to_csv(file_path, index=False)
    return test_df
