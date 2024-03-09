# MBS Stock trading signal Project
[![Author - DanRamirez](https://img.shields.io/badge/Author-DanRamirez-2ea44f?style=for-the-badge)](https://github.com/Dandata0101)
[![Author - VineethReddy](https://img.shields.io/badge/Author-VineethReddy-2ea44f?style=for-the-badge)](https://github.com/VineethReeddyBAAIML)
[![Author - BahijHaidar](https://img.shields.io/badge/Author-BahijHaidar-2ea44f?style=for-the-badge)](https://github.com/bahijh)
[![Author - LisaFanzy](https://img.shields.io/badge/Author-LisaFanzy-2ea44f?style=for-the-badge)](https://www.linkedin.com/in/lisa-fanzy)
![Python - Version][PYTHON-url]

## Table of Content
1. [Summary and Used Case](https://github.com/Dandata0101/mbs-Stock-singal-project?tab=readme-ov-file#summary-and-used-case)
2. [Application Structure](https://github.com/Dandata0101/mbs-Stock-singal-project?tab=readme-ov-file#application-structure)
3. [Interface](https://github.com/Dandata0101/mbs-Stock-singal-project?tab=readme-ov-file#interface-globe_with_meridians)
4. [Output](https://github.com/Dandata0101/mbs-Stock-singal-project?tab=readme-ov-file#output-locations)
5. [Data Retrival](https://github.com/Dandata0101/mbs-Stock-singal-project?tab=readme-ov-file#data-retrival)
6. [Model Build](https://github.com/Dandata0101/mbs-Stock-singal-project?tab=readme-ov-file#model-build)
7. [Local Testing](https://github.com/Dandata0101/mbs-Stock-singal-project?tab=readme-ov-file#local-testing)

## Summary and Used Case
We designed and implemented an algorithm trading platform that can run on any stock. This algorithm is adaptable, choosing between long or short positions and customizable hyperparameters to maximize profitability based on historical market conditions. The solution's core is a machine learning model based on a random forest classification model for grid search cross-validation using the Yahoo Finance Python Package to retrieve stock data. 

For our MBS Project assignment, we will run a stock predictor algorithm concentrated on a single trading target: **Atlassian**, a software publisher based in Australia. The algorithm will be hosted online, providing a platform for online access and interaction with the trading system. For testing purposes, we will provide steps to run individual custom Python packages for this project and how to run our Flask application locally.

### Simulation Setup
- **Training Period** :weight_lifting: Jan 2013~ Dec 2019 :spiral_calendar:
- **Test Period** :test_tube: Jan 2020 ~ Feb 2024 :spiral_calendar:

For our test period, we start with a **$50K balance**. We buy/sell :100:% of the balance based on the Sell/Buy Signal of our [Data ml_buysell.py function :robot:](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/01-data/profitCalc_export.xlsx). A ledger is created in our [Profit_calc.py :dollar:](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/scripts/ml_buysellfx.py) to track stock shares held and balance. If we retain any shares at the end of the test period, we calculate the balance as the value of the shares held.

Details for custom python Package shown in the [Python Packages :snake:](https://github.com/Dandata0101/mbs-Stock-singal-project?tab=readme-ov-file#snake-python-packages)

Final delivery our test simulation be emails/downloaded from [Our Web App :globe_with_meridians:](https://www.y-data.fr) results page or retrived from the [Final report output directory :file_folder:](https://github.com/Dandata0101/mbs-Stock-singal-project/tree/main/03-output). See **Interface** and **Output** sections for more detail.

## Application Structure
<img src="https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/04-readme-images/Appstructure.png" alt="Application" style="width:1000px;height: 600px;"> 

### :snake: Python Packages
<img src="https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/04-readme-images/Function.png" alt="Packages" style="width:2200;height:400;"> 

For our project, Python files **2.**:star2: and **3.**:star2: are our core delivery.

[Script Directory :file_folder:](https://github.com/Dandata0101/mbs-Stock-singal-project/tree/main/scripts)
1. [Yahoo Finance Dataframe :dollar:](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/scripts/yahoofinance.py)
2. :star2:[**ML Buy/Sell Signal** :robot:](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/scripts/ml_buysellfx.py) 
3. :star2:[**Profit Calculation** :robot::currency_exchange:](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/scripts/profit_calc.py)
4. [Chart and Excel export :chart_with_upwards_trend:](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/scripts/ml_chart_export.py) 
5. [Final Report :green_book:](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/scripts/excel_export.py)
6. [email body :email:](https://github.com/Dandata0101/mbs-Stock-singal-project/tree/main/EmailBody)
7. [Send email :email:](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/scripts/excel_export.py)
 

## Interface :globe_with_meridians: 

[Our Web App](https://www.y-data.fr)

Our home page where you enter your stock symbol and adjust Hyperparameters, **note**: keeping the defaults will run the fastest.
<img src="https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/04-readme-images/Home.png" alt="Home" style="width:2200;height:400;"> 

Results 1 section shows basic information the the company and charts our Buy/Sell Signals. At the top of the page, you have the option to email the report or download it to your desktop :floppy_disk: :arrow_right: :computer:.
<img src="https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/04-readme-images/results1.png" alt="Results1" style="width:2200;height:400;"> 

Results 2 section show our final profit from our simulation and provides model performance Statistics.
<img src="https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/04-readme-images/results2.png" alt="Results2" style="width:2200;height:400;"> 


## Output Locations
For our project, Export **2.** :star2: is  a key deliverable to review the performance of our ML model ouput.

[Data output :file_folder:](https://github.com/Dandata0101/mbs-Stock-singal-project/tree/main/01-data)
1. [Yahoo Finance Dataframe :dollar:](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/01-data/input_YahooFin.xlsx)
2. :star2:[**Data w Buy/Sell Signal & Profit calculation** :dollar:](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/01-data/profitCalc_export.xlsx)
3. [Model Accuracy :robot: ](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/01-data/accuracy_export.xlsx)
3. [Feature Importance :robot: ](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/01-data/feature_export.xlsx)
4. [Grid Search Best Model :robot: ](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/01-data/bestmodel_export.xlsx)

This directory has the combined output of Signal charts, full data ouput and model performance in excel

[Final Report output :file_folder::green_book:](https://github.com/Dandata0101/mbs-Stock-singal-project/tree/main/03-output)


## Data Retrival

```python:
import yfinance as yf
import datetime
import pandas as pd
import warnings
import os

........
def create_dataframe(tickerSymbol='MSFT'):
    print('1.1) Starting stock data extraction')

    end_date = datetime.date.today()
    start_date = datetime.date(2013, 1, 1)

    df_stock = fetch_data(tickerSymbol, start_date, end_date)
    df_vix = fetch_data('^VIX', start_date, end_date)
    df_dji = fetch_data('^DJI', start_date, end_date)

    # Merge stock data, VIX data, and DJI data
    df_merged = pd.merge(df_stock, df_vix, on='Date', how='left')
    df_merged = pd.merge(df_merged, df_dji, on='Date', how='left')

    current_directory = os.getcwd()
    df_merged.to_excel(current_directory + '/01-data/input_YahooFin.xlsx', index=False)

    # Fetch and return company details as well
    company_details = fetch_company_details(tickerSymbol)
    
    return df_merged, company_details

........
```

## X variables
<img src="https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/04-readme-images/xvariable.png" alt="Home" style="width:2200;height:400;"> 
<span style="color: green;">:one:</span> <strong>df['close_short']</strong> & <strong>df['close_long']</strong>: This represents a rolling average of the closing prices.<br>
<br>
<span style="color: green;">:two:</span> <strong>delta</strong>: Represents the day-to-day change in the closing price, calculated by the .diff() function which computes the difference between consecutive elements in the DataFrame. <strong>gain</strong> & <strong>loss</strong>: A series representing the gains over a 14-day rolling window. It filters the delta to consider only positive changes. <strong>rs</strong>: The relative strength, calculated as the average gain over the average loss over a rolling window of 14 days.<br>
<br>
<span style="color: green;">:three:</span> <strong>df['RSI']</strong>: The Relative Strength Index, a momentum indicator that measures the magnitude of recent price changes to evaluate overbought or oversold conditions.<br>
<br>
<span style="color: green;">:four:</span> <strong>df['EMA12']</strong> and <strong>df['EMA26']</strong>: These are Exponential Moving Averages with spans of 12 and 26 days, respectively. EMAs give more weight to recent prices and are used to identify trends.<br>
<br>
<span style="color: green;">:five:</span> <strong>df['MACD']</strong>: The Moving Average Convergence Divergence, which is calculated by subtracting the 26-day EMA from the 12-day EMA. The MACD is a trend-following momentum indicator.<br>
<br>
<span style="color: green;">:six:</span> <strong>df['Signal_Line']</strong>: A 9-day EMA of the MACD values. It acts as a trigger for buy and sell signals when it crosses the MACD line.<br>
<br>
<span style="color: green;">:seven:</span>  Volatility <strong>Index</strong> and <strong>Dow Jone index</strong> were added to account for anomalies.<br>

## Y variables
<img src="https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/04-readme-images/yvariable.png" alt="Home" style="width:2200;height:400;"> 


## Model Build

```python:
    rf = RandomForestClassifier(random_state=42)
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)
    grid_search.fit(X_train, y_train)
    print('Parms used:',param_grid)

    best_model = grid_search.best_estimator_
    predictions = best_model.predict(X_test)
    test_df.loc[X_test.index, 'Predictions'] = predictions
```

## Local Testing
From the main directory, there is a [test.py :snake:](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/test.py) where you can test data, ML model and Final export. **Note**: Send function requires a token/secret key for it work, so make sure to to "**body**" and "**send**" before running. To run the interface locally, run the [main.py :snake:](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/main.py) file, open your browser and go to **http://localhost:8000**. 

```python:
#testing area for functions

import os
from scripts.yahoofinance import create_dataframe
from scripts.ml_buysellfx import predict_trading_signals
from scripts.profit_calc import calculate_profit
from scripts.ml_chart_export import plot_stock_signals,interactive_plot_stock_signals,first_buy_record,Last_record
from scripts.excel_export import export_df_to_excel_with_chart
from EmailBody.emailbody import generate_email_body
from scripts.sendemail import send_email

stock='TEAM'
email=["dan@y-data.co"]

df,company_details=create_dataframe(tickerSymbol=stock)
company_name=company_details['longName']

test_df, accuracy, precision, recall, f1, feature_importances,importance_df,metrics_df=predict_trading_signals(df)
profit=calculate_profit(test_df)

chart = plot_stock_signals(df=profit, tickerSymbol=stock)
firstbuy=first_buy_record(df=profit)
Last_transaction=Last_record(df=profit)

#Final analysis delivered to the 03-out directory
export = export_df_to_excel_with_chart(df=profit, tickerSymbol=stock)

#requires a MSFT Secret key to run, comment out this section when testing 
Body=generate_email_body(tickerSymbol=company_name)
send=send_email(email_body=Body,recipient_emails=email)
```


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/danramirezjr
[PYTHON-url]: https://img.shields.io/badge/PYTHON-3.11-red?style=for-the-badge&logo=python&logoColor=white
