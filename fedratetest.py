import requests
import json
import configparser
import sys, os
import warnings
import base64
import glob
from dotenv import load_dotenv
load_dotenv()
import datetime
from fredapi import Fred
import pandas as pd


# Define the date range
end_date = datetime.date.today()  # Today's date
start_date = datetime.date(2013, 1, 1)  # Start date
fedkey = os.getenv('fedkey')
fred = Fred(api_key=fedkey)

federal_funds_rate = fred.get_series('FEDFUNDS', observation_start=start_date, observation_end=end_date)
federal_funds_rate_df = federal_funds_rate.to_frame(name='Federal Funds Effective Rate')
fedrate_df = federal_funds_rate.to_frame(name='fedrate')
federal_funds_rate_df.reset_index(inplace=True)
federal_funds_rate_df.rename(columns={'index': 'Date'}, inplace=True)

# Print the DataFrame to check
print(federal_funds_rate_df.head())