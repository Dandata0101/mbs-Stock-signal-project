import pandas as pd
import numpy as np
import os

def calculate_profit(df):
    initial_balance = 50000
    cumulative_profit = initial_balance
    position = 0  # Tracks the number of shares owned
    df['profit'] = 0.0
    df['cumulative_profit'] = initial_balance

    for i in range(len(df)):
        # Reset profit at the start of each iteration
        df.at[i, 'profit'] = 0.0

        # Buy logic
        if df.at[i, 'Buy_Signal'] == 1:
            shares_to_buy = cumulative_profit // df.at[i, 'pricebuy']
            if shares_to_buy > 0:
                cost = shares_to_buy * df.at[i, 'pricebuy']
                cumulative_profit -= cost  # Subtract the cost from cumulative_profit
                position += shares_to_buy
                df.at[i, 'profit'] = -cost

        # Sell logic
        elif df.at[i, 'Sell_Signal'] == 1 and position > 0:
            revenue = position * df.at[i, 'pricesell']
            cumulative_profit += revenue  # Add the revenue to cumulative_profit
            position = 0
            df.at[i, 'profit'] = revenue

        # Update cumulative_profit only if there's a transaction
        df.at[i, 'cumulative_profit'] = cumulative_profit


    # Adjust for final sell-off if any shares remain unsold
    if position > 0:
        last_price = df['Close'].values[-1]
        revenue = position * last_price
        cumulative_profit += revenue
        df.at[len(df)-1, 'profit'] = revenue

    # The last row always has the final cumulative profit
    df.at[len(df)-1, 'cumulative_profit'] = cumulative_profit

    df.fillna(0, inplace=True)

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')

    # Saving the DataFrame to a CSV file
    #file_path = os.path.join(os.getcwd(), '01-data', 'ml_test_signals_prices_w_profit.csv')
    #df.to_csv(file_path, index=False)
    
    return df
