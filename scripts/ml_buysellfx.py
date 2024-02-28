import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import os

def predict_trading_signals(df):
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    def add_technical_indicators(df):
        df['close_short'] = df['Close'].rolling(window=5).mean()
        df['close_long'] = df['Close'].rolling(window=20).mean()
        delta = df['Close'].diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        df['EMA12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA12'] - df['EMA26']
        df['Signal_line'] = df['MACD'].ewm(span=9, adjust=False).mean()
        return df

    df = add_technical_indicators(df)

    def label_data(df):
        df['Label'] = 0
        df.loc[df['close_short'] > df['close_long'], 'Label'] = 1
        return df

    df = label_data(df)
    df.dropna(inplace=True)

    train_df = df.loc['2013-01-01':'2019-12-31']
    test_df = df.loc['2020-01-01':]

    features = ['close_short', 'close_long', 'RSI', 'MACD', 'Signal_line']
    X_train = train_df[features]
    y_train = train_df['Label']
    X_test = test_df[features]

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    predictions = model.predict(X_test)
    test_df.loc[X_test.index, 'Predictions'] = predictions

    def add_signals_prices_and_calculate_profit(df):
        df['Buy_Signal'] = 0
        df['Sell_Signal'] = 0
        df['Buy_Price'] = np.nan
        df['Sell_Price'] = np.nan
        df['Profit'] = 0  # Initialize with 0 for all rows
        df['First_Buy_Flag'] = 0  # Initialize column to flag the first buy
        balance = 50000  # Initial balance
        initial_buy_percentage = 0.04  # 4% for the initial buy
        shares_held = 0
        first_buy_executed = False

        for i in range(1, len(df)):
            if not first_buy_executed and df.iloc[i]['Predictions'] == 1:
                # Calculate the amount to spend on the first buy
                spend_for_first_buy = balance * initial_buy_percentage
                shares_held = spend_for_first_buy // df.iloc[i]['Close']
                balance -= shares_held * df.iloc[i]['Close']  # Update balance after first buy
                df.at[df.index[i], 'Buy_Signal'] = 1
                df.at[df.index[i], 'Buy_Price'] = df.iloc[i]['Close']
                df.at[df.index[i], 'First_Buy_Flag'] = 1
                first_buy_executed = True
            elif first_buy_executed and df.iloc[i]['Predictions'] == 1 and shares_held == 0:
                # Handle subsequent buys if any, after the first buy has been executed
                shares_held = balance // df.iloc[i]['Close']
                balance -= shares_held * df.iloc[i]['Close']
                df.at[df.index[i], 'Buy_Signal'] = 1
                df.at[df.index[i], 'Buy_Price'] = df.iloc[i]['Close']
            elif df.iloc[i]['Predictions'] == 0 and shares_held > 0:
                # Sell shares when a sell signal is encountered
                profit = (df.iloc[i]['Close'] - df.iloc[i]['Buy_Price']) * shares_held
                balance += shares_held * df.iloc[i]['Close']
                df.at[df.index[i], 'Sell_Signal'] = 1
                df.at[df.index[i], 'Sell_Price'] = df.iloc[i]['Close']
                df.at[df.index[i], 'Profit'] = profit
                shares_held = 0  # Reset shares held after selling

        # Cumulative profit is the running total of the 'Profit' column
        df['Cumulative_Profit'] = df['Profit'].cumsum()

        # Final balance calculation includes the value of any remaining shares
        last_price = df.iloc[-1]['Close']
        final_balance = balance + (shares_held * last_price)
        df['Final_Balance'] = final_balance

        return df

    test_df = add_signals_prices_and_calculate_profit(test_df)
    test_df.reset_index(inplace=True)

    # Correcting the file path assembly
    csv_file_path = os.path.join(os.getcwd(), '01-data', 'final_trading_signals.csv')

    test_df.to_csv(csv_file_path, index=False)
    print(f"Final DataFrame has been saved to {csv_file_path}")

    return test_df

