import pandas as pd
import numpy as np
import os
import time

def calculate_profit(df):
    print("Starting profit calculation...")
    start_time = time.time()
    Balance = [] #contribution from DrChen
    initial_Balance = 50000
    tmp_Balance = initial_Balance #contribution from DrChen
    cumulative_profit = initial_Balance
    position = 0  # Tracks the number of shares owned
    
    for i in range(len(df)):
        # Reset profit at the start of each iteration
        df.at[i, 'profit'] = 0.0

        # Buy logic
        if df.at[i, 'Buy_Signal'] == 1:
            shares_to_buy = cumulative_profit // df.at[i, 'Open']
            if shares_to_buy > 0:
                cost = shares_to_buy * df.at[i, 'Open']
                tmp_Balance -= cost
                df.at[i, 'Balance'] = tmp_Balance
                position += shares_to_buy
            else:
                df.at[i, 'Balance'] = tmp_Balance
                # Balance.append(tmp_Balance)
        # Sell logic
        elif df.at[i, 'Sell_Signal'] == 1 and position > 0:
            if position>0:
                revenue = position * df.at[i, 'Open']
                tmp_Balance += revenue
                df.at[i, 'Balance'] = tmp_Balance
                position = 0
            else:
                df.at[i, 'Balance'] = tmp_Balance
        else:
            df.at[i, 'Balance'] = tmp_Balance
            
        # Update cumulative_profit only if there's a transaction
        # df.at[i, 'cumulative_profit'] = cumulative_profit
        
    # Adjust for final sell-off if any shares remain unsold
    if position > 0:
        last_price = df['Close'].values[-1]
        revenue = position * last_price
        tmp_Balance += revenue
        df.at[len(df)-1, 'Balance'] = tmp_Balance
    
    total_profit = df.at[len(df)-1, 'Balance'] - initial_Balance
    print('The final profit/loss:', total_profit)
    # The last row always has the final cumulative profit
    df.fillna(0, inplace=True)

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%Y-%m-%d')

    elapsed_time = time.time() - start_time

    print(f"Profit calculation completed in {elapsed_time:.2f} seconds.")

    current_directory = os.getcwd()
    df.to_excel(current_directory+'/01-data/test_export.xlsx')
    return df

    

