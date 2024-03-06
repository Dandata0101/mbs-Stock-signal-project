# MBS Stock trading signal Project
[![Author - DanRamirez](https://img.shields.io/badge/Author-DanRamirez-2ea44f?style=for-the-badge)](https://github.com/Dandata0101)
[![Author - VineethReddy](https://img.shields.io/badge/Author-VineethReddy-2ea44f?style=for-the-badge)](https://github.com/VineethReeddyBAAIML)
[![Author - BahijHaidar](https://img.shields.io/badge/Author-BahijHaidar-2ea44f?style=for-the-badge)](https://github.com/bahijh)
[![Author - LisaFanzy](https://img.shields.io/badge/Author-LisaFanzy-2ea44f?style=for-the-badge)](https://www.linkedin.com/in/lisa-fanzy)
![Python - Version][PYTHON-url]

## Table of Content
1. [Summary and Used Case](https://github.com/Dandata0101/mbs-Stock-singal-project#Summary-and-Used-Case)
2. [Application Structure](https://github.com/Dandata0101/mbs-Stock-singal-project#Application-Structure)
3. [Data Retrival](https://github.com/Dandata0101/mbs-Stock-singal-project#Data-Retrival)
4. [Model Build](https://github.com/Dandata0101/mbs-Stock-singal-project#Model-Build)
5. [Interface and Output](https://github.com/Dandata0101/mbs-Stock-singal-project#Interface-and-Output)
5. [Local Testing](https://github.com/Dandata0101/mbs-Stock-singal-project#Local-Testing)

## Summary and Used Case
We designed and implemented an algorithm trading platform that can run on any stock. This algorithm is adaptable, choosing between long or short positions and customizable hyperparameters to maximize profitability based on historical market conditions. The solution's core is a machine learning model based on a random forest classification model for grid search cross-validation using the Yahoo Finance Python Package to retrieve stock data. 

For our MBS Project assignment, we will run a stock predictor algorithm concentrated on a single trading target: **Atlassian**, a software publisher based in Australia. The algorithm will be hosted online, providing a platform for online access and interaction with the trading system. For testing purposes, we will provide steps to run individual custom Python packages for this project and how to run our Flask application locally.

## Application Structure
<img src="https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/04-readme-images/Appstructure.png" alt="Application" style="width:600px;height: 400px;"> 

### Python Packages
<img src="https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/04-readme-images/Function.png" alt="Packages" style="width:2200;height:100;"> 

### Custom Python Packages :snake:
1.[Yahoo Finance Dataframe](https://github.com/Dandata0101/mbs-Stock-singal-project/blob/main/scripts/yahoofinance.py) :dollar: 

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

## Model Build


## Interface and Output

### Locations
  

## Local Testing


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
print('~~~~~~~~~~~~~~~~~~~~~~~~~')
print('testing py exceution')
print('~~~~~~~~~~~~~~~~~~~~~~~~~')
print('')
print('~~~~~~~~~~~~~~~~~~~~~~~~~')
print('Stock Symbol:',stock)
print('CompanyName:',company_name)
print('~~~~~~~~~~~~~~~~~~~~~~~~~')
print('')

test_df, accuracy, precision, recall, f1, feature_importances,importance_df,metrics_df=predict_trading_signals(df)
profit=calculate_profit(test_df)

chart = plot_stock_signals(df=profit, tickerSymbol=stock)
firstbuy=first_buy_record(df=profit)
Last_transaction=Last_record(df=profit)

#Final analysis delivered to the 03-out directory
export = export_df_to_excel_with_chart(df=profit, tickerSymbol=stock)

#requirs a MSFT Secret key to run, comment out this section when testing 
Body=generate_email_body(tickerSymbol=company_name)
send=send_email(email_body=Body,recipient_emails=email)
```




<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/danramirezjr
[PYTHON-url]: https://img.shields.io/badge/PYTHON-3.11-red?style=for-the-badge&logo=python&logoColor=white
