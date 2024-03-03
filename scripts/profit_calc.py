import pandas as pd
import numpy as np
import os
import time

def calculate_profit(df):
    print("Starting profit calculation...")
    start_time = time.time()
    Balance=[]
    initial_Balance = 50000
    tmp_Balance = initial_Balance
    position = 0  # Tracks the number of shares owned
    positions = []  # List to track position over time
    
    for i in range(len(df)):
        df.at[i, 'profit'] = 0.0  # Reset profit
        
        # Buy logic
        if df.at[i, 'Buy_Signal'] == 1:
            shares_to_buy = tmp_Balance // df.at[i, 'Open']
            if shares_to_buy > 0:
                cost = shares_to_buy * df.at[i, 'Open']
                tmp_Balance -= cost
                position += shares_to_buy
            df.at[i, 'Balance'] = tmp_Balance
            positions.append(position)  # Update position list

        # Sell logic
        elif df.at[i, 'Sell_Signal'] == 1 and position > 0:
            revenue = position * df.at[i, 'Open']
            tmp_Balance += revenue
            position = 0  # Reset position after selling
            df.at[i, 'Balance'] = tmp_Balance
            positions.append(position)  # Update position list

        else:
            df.at[i, 'Balance'] = tmp_Balance
            positions.append(position)  # Update position list without change
            
    # Adjust for final sell-off if any shares remain unsold
    if position > 0:
        last_price = df['Close'].values[-1]
        revenue = position * last_price
        tmp_Balance += revenue
        df.at[len(df)-1, 'Balance'] = tmp_Balance

    # Insert the 'Position' column before 'Balance'
    df.insert(df.columns.get_loc('Balance'), 'Position', positions)
    df.drop('profit', axis=1, inplace=True)
    df.rename(columns={'Position': 'Shares_held'}, inplace=True)
    
    df.fillna(0, inplace=True)

    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date']).dt.strftime('%Y-%m-%d')

    elapsed_time = time.time() - start_time
    print(f"Profit calculation completed in {elapsed_time:.2f} seconds. The final profit/loss: {tmp_Balance - initial_Balance}")

    # Export to Excel
    current_directory = os.getcwd()
    df.to_excel(current_directory + '/01-data/profitCalc_export.xlsx', index=False)

    return df
